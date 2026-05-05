# apps/messaging/services/personality_analyzer.py

import logging
from collections import Counter
from django.db.models import Count
from django.core.cache import cache

from apps.posts.models import Post, Like, Comment
from apps.hashtags.models import PostHashtag
from apps.follows.models import Follow

logger = logging.getLogger(__name__)


class TargetPersonalityAnalyzer:
    """
    تحلیل شخصیت فرد مقابل برای کمک به مکالمه
    """
    
    def __init__(self, target_user):
        self.target = target_user
        self._ollama_client = None
    
    def _get_ollama_client(self):
        if self._ollama_client is None:
            try:
                from apps.ml.ollama_client import OllamaClient
                self._ollama_client = OllamaClient()
            except ImportError:
                logger.warning("OllamaClient not found")
        return self._ollama_client
    
    def analyze_target(self, force_refresh=False):
        """
        تحلیل کامل فرد مقابل
        """
        cache_key = f"target_analysis_{self.target.id}"
        
        if not force_refresh:
            cached = cache.get(cache_key)
            if cached:
                return cached
        
        # جمع‌آوری داده‌ها
        data = self._collect_data()
        
        # تحلیل با AI
        analysis = self._ai_analysis(data)
        
        cache.set(cache_key, analysis, 60 * 60 * 6)  # 6 ساعت کش
        
        return analysis
    
    def _collect_data(self):
        """جمع‌آوری داده‌های عمومی از فرد مقابل"""
        
        # پست‌ها
        posts = Post.objects.filter(user=self.target, is_deleted=False)
        
        # هشتگ‌های پراستفاده
        hashtags = PostHashtag.objects.filter(
            post__user=self.target
        ).values('hashtag__name').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        
        # لایک‌هایی که کرده
        liked_posts = Like.objects.filter(user=self.target).values_list('post_id', flat=True)[:50]
        liked_hashtags = PostHashtag.objects.filter(
            post_id__in=liked_posts
        ).values_list('hashtag__name', flat=True)
        
        # بیوگرافی
        bio = ""
        if hasattr(self.target, 'profile') and self.target.profile:
            bio = self.target.profile.bio or ""
        
        # تعداد فالوور و فالوینگ
        followers_count = Follow.objects.filter(following=self.target).count()
        following_count = Follow.objects.filter(follower=self.target).count()
        
        return {
            "username": self.target.username,
            "bio": bio,
            "posts_count": posts.count(),
            "followers_count": followers_count,
            "following_count": following_count,
            "top_hashtags": [h['hashtag__name'] for h in hashtags],
            "liked_hashtags": list(set(liked_hashtags))[:10],
            "has_profile_image": hasattr(self.target, 'profile') and bool(self.target.profile.profile_image)
        }
    
    def _ai_analysis(self, data):
        """تحلیل با Ollama"""
        
        ollama = self._get_ollama_client()
        
        if not ollama:
            return self._fallback_analysis(data)
        
        prompt = f"""
        شما یک مشاور روابط و psychologie اجتماعی هستید. 
        بر اساس اطلاعات زیر، شخصیت فرد را تحلیل کن و راهکارهایی برای ارتباط با او بده:
        
        اطلاعات فرد:
        - نام کاربری: {data.get('username')}
        - بیوگرافی: {data.get('bio', 'ندارد')}
        - تعداد پست: {data.get('posts_count', 0)}
        - تعداد فالوور: {data.get('followers_count', 0)}
        - هشتگ‌های پرکاربرد: {data.get('top_hashtags', [])[:5]}
        - هشتگ‌هایی که لایک کرده: {data.get('liked_hashtags', [])[:5]}
        
        خروجی را به صورت JSON برگردان با این ساختار:
        {{
            "personality_type": "نوع شخصیت (مثلا: برون‌گرا، درون‌گرا، هنرمند، ماجراجو، حرفه‌ای)",
            "interests": ["علاقه1", "علاقه2", "علاقه3"],
            "communication_style": "سبک ارتباطی پیشنهادی (مثلا: صمیمی، رسمی، شوخ، جدی)",
            "icebreakers": ["موضوع1 برای شروع مکالمه", "موضوع2"],
            "topics_to_avoid": ["موضوعاتی که بهتر است صحبت نشود"],
            "best_time_to_message": "بهترین زمان برای پیام دادن",
            "tips": ["نکته1", "نکته2", "نکته3"]
        }}
        
        فقط JSON را برگردان.
        """
        
        try:
            result = ollama.generate(prompt, temperature=0.7, max_tokens=600)
            
            if result.get('success'):
                import json
                import re
                text = result.get('response', '')
                match = re.search(r'\{.*\}', text, re.DOTALL)
                if match:
                    return json.loads(match.group())
            
            return self._fallback_analysis(data)
            
        except Exception as e:
            logger.error(f"AI analysis error: {e}")
            return self._fallback_analysis(data)
    
    def _fallback_analysis(self, data):
        """تحلیل ساده بدون AI"""
        
        interests = data.get('top_hashtags', [])[:3]
        
        personality_type = "برون‌گرا" if data.get('posts_count', 0) > 20 else "درون‌گرا"
        
        return {
            "personality_type": personality_type,
            "interests": interests,
            "communication_style": "صمیمی و دوستانه",
            "icebreakers": [f"درباره {interests[0]}" if interests else "درباره علایق مشترک"],
            "topics_to_avoid": ["مسائل شخصی خیلی خصوصی"],
            "best_time_to_message": "عصرها",
            "tips": ["با سلام دوستانه شروع کن", "به پست‌هایش واکنش نشان بده"]
        }


class MessageSuggestionService:
    """
    سرویس پیشنهاد پیام بر اساس تحلیل شخصیت
    """
    
    def __init__(self, user, target_user):
        self.user = user
        self.target = target_user
        self.analyzer = TargetPersonalityAnalyzer(target_user)
    
    def get_opening_message_suggestions(self, count=3):
        """
        پیشنهاد پیام‌های شروع کننده مکالمه
        """
        analysis = self.analyzer.analyze_target()
        
        ollama = self.analyzer._get_ollama_client()
        
        if not ollama:
            return self._default_suggestions(analysis)
        
        prompt = f"""
        شما یک دستیار دوستانه برای شروع مکالمه هستید.
        
        اطلاعات فرد مقابل:
        - تیپ شخصیتی: {analysis.get('personality_type')}
        - علایق: {analysis.get('interests', [])}
        - سبک ارتباطی: {analysis.get('communication_style')}
        
        لطفاً {count} پیام کوتاه و صمیمی برای شروع مکالمه پیشنهاد بده.
        پیام‌ها باید دوستانه، محترمانه و متناسب با شخصیت فرد باشند.
        
        فقط {count} پیام را در یک لیست JSON برگردان.
        مثال: ["پیام اول", "پیام دوم", "پیام سوم"]
        """
        
        try:
            result = ollama.generate(prompt, temperature=0.8, max_tokens=200)
            
            if result.get('success'):
                import json
                import re
                text = result.get('response', '')
                match = re.search(r'\[.*\]', text, re.DOTALL)
                if match:
                    suggestions = json.loads(match.group())
                    return suggestions[:count]
            
            return self._default_suggestions(analysis)
            
        except Exception as e:
            logger.error(f"Message suggestion error: {e}")
            return self._default_suggestions(analysis)
    
    def _default_suggestions(self, analysis):
        """پیشنهادات پیش‌فرض"""
        interests = analysis.get('interests', [])
        
        suggestions = [
            "سلام! حال دیدن پست‌هات خوب بود، خیلی باحالن 👋",
            "سلام چطوری؟ پروفایل جالبی داری 😊",
        ]
        
        if interests:
            suggestions.append(f"سلام! دیدم به {interests[0]} علاقه داری، منم خیلی دوست دارم 🤝")
        
        return suggestions[:3]
    
    def get_reply_suggestion(self, last_message):
        """
        پیشنهاد پاسخ به آخرین پیام
        """
        ollama = self.analyzer._get_ollama_client()
        
        if not ollama:
            return "چیز جالبی بگو! 😊"
        
        prompt = f"""
        آخرین پیام دریافتی: "{last_message}"
        
        یک پاسخ طبیعی، دوستانه و مناسب پیشنهاد بده.
        پاسخ باید کوتاه و صمیمی باشد.
        
        فقط متن پاسخ را برگردان، بدون توضیح.
        """
        
        try:
            result = ollama.generate(prompt, temperature=0.8, max_tokens=100)
            
            if result.get('success'):
                return result.get('response', '')
            
            return "چه جالب! بگو بیشتر 😊"
            
        except Exception as e:
            logger.error(f"Reply suggestion error: {e}")
            return "چه جالب! بگو بیشتر 😊"