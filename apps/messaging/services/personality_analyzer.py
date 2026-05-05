# apps/messaging/services/personality_analyzer.py

import logging
import json
import re
from collections import Counter
from django.db.models import Count
from django.core.cache import cache
from django.conf import settings

from apps.posts.models import Post, Like, Comment
from apps.hashtags.models import PostHashtag
from apps.follows.models import Follow

logger = logging.getLogger(__name__)
# اینجا سرویس مستقل از اپ ml برای این 
#این کارو کردم که اگه خواستم اینو تغیررش بدم خیلی راحت باشه و وابستگی کمی هم داره در ضمن خیلی راحت میتونید این قسمت رو بردارید و یه جای دیگه پیاده سازی کنید مناسب اپتون 

class OllamaClient:
    """
    کلاینت ساده اتصال به Ollama
    """
    
    def __init__(self):
        self.base_url = getattr(settings, 'OLLAMA_BASE_URL', 'http://localhost:11434')
        self.model = getattr(settings, 'OLLAMA_MODEL', 'gemma3:27b')
    
    def generate(self, prompt, temperature=0.7, max_tokens=500):
        import requests
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "response": response.json().get("response", "")
                }
            else:
                return {"success": False, "error": f"HTTP {response.status_code}"}
                
        except requests.exceptions.ConnectionError:
            return {"success": False, "error": "Ollama در حال اجرا نیست"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def check_health(self):
        import requests
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = [m['name'] for m in response.json().get('models', [])]
                return {
                    'status': 'healthy',
                    'models': models,
                    'model_available': self.model in models
                }
            return {'status': 'unhealthy'}
        except:
            return {'status': 'unhealthy'}


class TargetPersonalityAnalyzer:
    
    def __init__(self, target_user):
        self.target = target_user
        self._ollama_client = None
    
    def _get_ollama_client(self):
        if self._ollama_client is None:
            self._ollama_client = OllamaClient()
        return self._ollama_client
    
    def analyze_target(self, force_refresh=False):
        cache_key = f"target_analysis_{self.target.id}"
        
        if not force_refresh:
            cached = cache.get(cache_key)
            if cached:
                logger.info(f"Using cached analysis for user {self.target.id}")
                return cached
        
        # جمع‌آوری داده‌ها
        data = self._collect_data()
        
        # تحلیل با AI
        analysis = self._ai_analysis(data)
        
        # ذخیره در کش (6 ساعت)
        cache.set(cache_key, analysis, 60 * 60 * 6)
        
        return analysis
    
    def _collect_data(self):
        """جمع‌آوری داده‌های کاربر"""
        
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
        
        ollama = self._get_ollama_client()
        
        # بررسی سلامت Ollama
        health = ollama.check_health()
        if health.get('status') != 'healthy':
            logger.warning("Ollama is not available, using fallback analysis")
            return self._fallback_analysis(data)
        
        prompt = f"""
        شما یک مشاور روابط اجتماعی هستید. بر اساس اطلاعات زیر، شخصیت فرد را تحلیل کن:
        
        اطلاعات فرد:
        - نام کاربری: {data.get('username')}
        - بیوگرافی: {data.get('bio', 'ندارد')}
        - تعداد پست: {data.get('posts_count', 0)}
        - تعداد فالوور: {data.get('followers_count', 0)}
        - هشتگ‌های پرکاربرد: {data.get('top_hashtags', [])[:5]}
        
        خروجی را به صورت JSON برگردان با این ساختار:
        {{
            "personality_type": "نوع شخصیت",
            "interests": ["علاقه1", "علاقه2", "علاقه3"],
            "communication_style": "سبک ارتباطی پیشنهادی",
            "icebreakers": ["موضوع1", "موضوع2"],
            "topics_to_avoid": ["موضوع1"],
            "best_time_to_message": "زمان پیشنهادی",
            "tips": ["نکته1", "نکته2"]
        }}
        
        فقط JSON را برگردان.
        """
        
        try:
            result = ollama.generate(prompt, temperature=0.7, max_tokens=600)
            
            if result.get('success'):
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
        
        return {
            "personality_type": "برون‌گرا" if data.get('posts_count', 0) > 20 else "درون‌گرا",
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
        """پیشنهاد پیام‌های شروع کننده"""
        
        analysis = self.analyzer.analyze_target()
        ollama = self.analyzer._get_ollama_client()
        
        health = ollama.check_health()
        if health.get('status') != 'healthy':
            return self._default_suggestions(analysis)
        
        prompt = f"""
        شما یک دستیار دوستانه برای شروع مکالمه هستید.
        
        اطلاعات فرد مقابل:
        - تیپ شخصیتی: {analysis.get('personality_type')}
        - علایق: {analysis.get('interests', [])}
        
        {count} پیام کوتاه و صمیمی برای شروع مکالمه پیشنهاد بده.
        
        فقط یک لیست JSON برگردان. مثال: ["پیام1", "پیام2"]
        """
        
        try:
            result = ollama.generate(prompt, temperature=0.8, max_tokens=200)
            
            if result.get('success'):
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
            "سلام! حال دیدن پست‌هات خوب بود 👋",
            "سلام چطوری؟ پروفایل جالبی داری 😊",
        ]
        
        if interests:
            suggestions.append(f"سلام! دیدم به {interests[0]} علاقه داری، منم خیلی دوست دارم 🤝")
        
        return suggestions[:3]
    
    def get_reply_suggestion(self, last_message):
        
        ollama = self.analyzer._get_ollama_client()
        
        health = ollama.check_health()
        if health.get('status') != 'healthy':
            return "چه جالب! بگو بیشتر 😊"
        
        prompt = f"""
        آخرین پیام دریافتی: "{last_message}"
        
        یک پاسخ طبیعی، دوستانه و کوتاه پیشنهاد بده.
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