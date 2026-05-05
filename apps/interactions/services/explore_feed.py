# apps/interactions/services/explore_feed.py

import logging
from collections import Counter
from datetime import datetime, timedelta
from django.db.models import Count, Q
from django.core.cache import cache

from apps.posts.models import Post, Like, Comment
from apps.hashtags.models import PostHashtag
from apps.follows.models import Follow

logger = logging.getLogger(__name__)


class ExploreFeedService:
    # 1. هشتگ‌های مورد علاقه کاربر (از لایک‌ها و کامنت‌ها)
    # 2. مرتب‌سازی بر اساس تعاملات (لایک، کامنت، ویو)
    
    def __init__(self, user):
        self.user = user
        self._ollama_client = None
    
    def _get_ollama_client(self):
        if self._ollama_client is None:
            try:
                from apps.ml.ollama_client import OllamaClient
                self._ollama_client = OllamaClient()
            except ImportError:
                logger.warning("OllamaClient not found")
        return self._ollama_client
    
    def get_explore_feed(self, limit=20, offset=0, use_ollama=True):
        cache_key = f"explore_feed_{self.user.id}_{offset}_{limit}_{use_ollama}"
        cached = cache.get(cache_key)
        
        if cached:
            return cached
        
        favorite_hashtags = self._get_favorite_hashtags(use_ollama)
        
        if not favorite_hashtags:
            posts = self._get_trending_posts(limit * 2)
        else:
            posts = self._search_posts_by_hashtags(favorite_hashtags, limit * 2)
        
        ranked_posts = self._rank_posts_by_engagement(posts, favorite_hashtags)
        
        result_posts = ranked_posts[offset:offset + limit]
        
        output = {
            'posts': [item['post'] for item in result_posts],
            'scores': [item['score'] for item in result_posts],
            'reasons': [item['reasons'] for item in result_posts],
            'used_hashtags': favorite_hashtags,
            'used_ollama': use_ollama,
            'total_count': len(ranked_posts),
            'has_next': offset + limit < len(ranked_posts)
        }
        
        cache.set(cache_key, output, 60 * 5)
        
        return output
    
    def _get_favorite_hashtags(self, use_ollama=False):
        hashtags = []
        
        liked_posts = Like.objects.filter(
            user=self.user
        ).values_list('post_id', flat=True)[:100]
        
        liked_hashtags = PostHashtag.objects.filter(
            post_id__in=liked_posts
        ).values_list('hashtag__name', flat=True)
        hashtags.extend(liked_hashtags)
        
        commented_posts = Comment.objects.filter(
            user=self.user
        ).values_list('post_id', flat=True)[:100]
        
        commented_hashtags = PostHashtag.objects.filter(
            post_id__in=commented_posts
        ).values_list('hashtag__name', flat=True)
        hashtags.extend(commented_hashtags)
        
        my_posts = Post.objects.filter(
            user=self.user
        ).values_list('id', flat=True)[:50]
        
        my_hashtags = PostHashtag.objects.filter(
            post_id__in=my_posts
        ).values_list('hashtag__name', flat=True)
        hashtags.extend(my_hashtags)
        
        hashtag_counter = Counter(hashtags)
        
        top_hashtags = [h for h, _ in hashtag_counter.most_common(10)]
        
        if use_ollama and top_hashtags:
            ai_hashtags = self._enhance_with_ollama(top_hashtags)
            if ai_hashtags:
                top_hashtags = list(set(top_hashtags + ai_hashtags))[:15]
        
        return top_hashtags
    
    def _enhance_with_ollama(self, current_hashtags):
        ollama = self._get_ollama_client()
        
        if not ollama:
            return []
        
        prompt = f"""
        کاربر به این هشتگ‌ها علاقه دارد: {', '.join(current_hashtags[:5])}
        
        5 هشتگ مرتبط و مشابه دیگر پیشنهاد بده.
        فقط لیست هشتگ‌ها را برگردان، بدون توضیح.
        
        مثال خروجی: nature, travel, photography, adventure, sunset
        """
        
        try:
            result = ollama.generate(prompt, temperature=0.5, max_tokens=100)
            
            if result.get('success'):
                response = result.get('response', '')
                import re
                hashtags = re.findall(r'[a-zA-Z0-9_\u0600-\u06FF]+', response)
                return [h.lower() for h in hashtags if len(h) > 2][:5]
            
            return []
            
        except Exception as e:
            logger.error(f"Ollama enhancement error: {e}")
            return []
    
    def _search_posts_by_hashtags(self, hashtags, limit):
        if not hashtags:
            return Post.objects.none()
        
        following_users = Follow.objects.filter(
            follower=self.user
        ).values_list('following_id', flat=True)
        
        posts = Post.objects.filter(
            post_hashtags__hashtag__name__in=hashtags,
            is_deleted=False
        ).exclude(
            user=self.user  
        ).exclude(
            user_id__in=following_users 
        ).select_related(
            'user', 'user__profile'
        ).prefetch_related(
            'likes', 'comments'
        ).annotate(
            likes_count=Count('likes'),
            comments_count=Count('comments')
        ).distinct()
        
        return posts[:limit]
    
    def _get_trending_posts(self, limit):
        following_users = Follow.objects.filter(
            follower=self.user
        ).values_list('following_id', flat=True)
        
        return Post.objects.filter(
            created_at__gte=datetime.now() - timedelta(days=3),
            is_deleted=False
        ).exclude(
            user=self.user
        ).exclude(
            user_id__in=following_users
        ).annotate(
            likes_count=Count('likes'),
            comments_count=Count('comments'),
            total_engagement=Count('likes') + Count('comments') * 2
        ).order_by('-total_engagement')[:limit]
    
    def _rank_posts_by_engagement(self, posts, target_hashtags):
        target_set = set(target_hashtags)
        scored = []
        
        for post in posts:
            likes_weight = min(post.likes_count, 100) * 0.5     
            comments_weight = min(post.comments_count, 50) * 0.6 
            
            post_hashtags = set(
                PostHashtag.objects.filter(post=post).values_list('hashtag__name', flat=True)
            )
            common_count = len(target_set & post_hashtags)
            hashtag_weight = min(common_count * 2, 20)          
            
         
            final_score = likes_weight + comments_weight + hashtag_weight
            
            reasons = self._get_display_reasons(post, common_count, target_set)
            
            scored.append({
                'post': post,
                'score': round(final_score, 2),
                'reasons': reasons,
                'metrics': {
                    'likes': post.likes_count,
                    'comments': post.comments_count,
                    'common_hashtags': common_count
                }
            })
        
        scored.sort(key=lambda x: x['score'], reverse=True)
        
        return scored
    
    def _get_display_reasons(self, post, common_count, target_hashtags):
        reasons = []
        
        if common_count > 0:
            post_hashtags = set(
                PostHashtag.objects.filter(post=post).values_list('hashtag__name', flat=True)
            )
            common = list(target_hashtags & post_hashtags)[:2]
            for tag in common:
                reasons.append(f"مشابه #{tag}")
        
        if post.likes_count > 50:
            reasons.append(f"{post.likes_count} لایک")
        
        if post.comments_count > 20:
            reasons.append(f"{post.comments_count} کامنت")
        
        if not reasons:
            reasons.append("پیشنهاد برای شما")
        
        return reasons[:3] 