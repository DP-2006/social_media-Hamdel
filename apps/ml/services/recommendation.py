from .base import BaseMLService
import numpy as np
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta

class RecommendationService(BaseMLService):
    def __init__(self):
        super().__init__('recommendation', 'recommendation_engine')
    
    def recommend_posts(self, user_id, limit=20, exclude_ids=None):
        ml_recommendations = self._ml_based_recommendation(user_id, limit)
        rule_based = self._rule_based_recommendation(user_id, limit // 2)
        
        all_recommendations = ml_recommendations + rule_based
        seen = set()
        unique_recs = []
        
        for rec in all_recommendations:
            if rec['post_id'] not in seen:
                seen.add(rec['post_id'])
                unique_recs.append(rec)
        
        return unique_recs[:limit]
    
    def _ml_based_recommendation(self, user_id, limit):
        if not self.model:
            return []
        
        try:
            from ..models import UserEmbedding
            user_embed = UserEmbedding.objects.filter(user_id=user_id).first()
            
            if not user_embed:
                return []
            
            return []
        except Exception as e:
            print(f"ML recommendation failed: {e}")
            return []
    
    def _rule_based_recommendation(self, user_id, limit):
        """توصیه بر اساس قوانین ساده"""
        from apps.posts.models import Post
        from apps.follows.models import Follow
        from apps.hashtags.models import PostHashtag
        
        user_interests = self._get_user_interests(user_id)
        
        recent_posts = Post.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=1)
        ).exclude(user_id=user_id)
        
        scored_posts = []
        for post in recent_posts:
            score = 0
            
            score += post.like_count * 0.5
            
            post_hashtags = PostHashtag.objects.filter(post=post).values_list('hashtag__name', flat=True)
            common_tags = len(set(post_hashtags) & set(user_interests))
            score += common_tags * 2
            
            scored_posts.append({
                'post_id': post.id,
                'score': score
            })
        
        scored_posts.sort(key=lambda x: x['score'], reverse=True)
        return scored_posts[:limit]
    
    def _get_user_interests(self, user_id):
        from apps.hashtags.models import PostHashtag
        from apps.posts.models import Like
        
        liked_posts = Like.objects.filter(user_id=user_id).values_list('post_id', flat=True)
        hashtags = PostHashtag.objects.filter(post_id__in=liked_posts).values_list('hashtag__name', flat=True)
        
        from collections import Counter
        hashtag_counts = Counter(hashtags)
        
        return [h for h, _ in hashtag_counts.most_common(10)]