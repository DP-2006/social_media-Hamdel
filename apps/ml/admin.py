# # apps/accounts/admin.py

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import path

User = get_user_model()
# apps/ml/admin.py
from django.contrib import admin

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.html import format_html
from .services.ollama_client import OllamaClient
from apps.posts.models import Post, Like, Comment
from apps.follows.models import Follow
from apps.profiles.models import Profile



User = get_user_model()






# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'phone', 'analyze_button')
    
#     def analyze_button(self, obj):
#         # obj.id میتونه UUID باشه
#         return format_html(
#             '<a class="button" href="analyze/{}/" target="_blank" style="background:#2c3e50; color:white; padding:5px 10px; text-decoration:none; border-radius:3px;">🤖 تحلیل کامل</a>',
#             obj.id
#         )
#     analyze_button.short_description = 'تحلیل هوشمند'
    
#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path('analyze/<str:user_id>/', self.analyze_view, name='analyze-user-admin'),
#         ]
#         return custom_urls + urls
    
#     def analyze_view(self, request, user_id):
#         try:
#             user = User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             return render(request, 'admin/error.html', {
#                 'error': f'کاربر با آیدی {user_id} پیدا نشد'
#             })
        
#         # گرفتن آمار کاربر
#         posts_count = 0
#         likes_given = 0
#         comments_count = 0
#         followers_count = 0
#         following_count = 0
        
#         try:
#             from apps.posts.models import Post, Like, Comment
#             from apps.follows.models import Follow
            
#             posts_count = Post.objects.filter(user=user).count()
#             likes_given = Like.objects.filter(user=user).count()
#             comments_count = Comment.objects.filter(user=user).count()
#             followers_count = Follow.objects.filter(following=user).count()
#             following_count = Follow.objects.filter(follower=user).count()
#         except:
#             pass
        
#         # ساخت پرامپت برای AI
#         prompt = f"""
# کاربر {user.phone} را تحلیل کن:
# - پست: {posts_count}
# - لایک: {likes_given}
# - کامنت: {comments_count}
# - دنبال‌کننده: {followers_count}
# - دنبال‌شونده: {following_count}

# پاسخ بده: شخصیت کاربر، پیشنهادات برای بهبود، هشتگ‌های مناسب
# """
        
#         client = OllamaClient()
#         result = client.generate(prompt)
        
#         return render(request, 'admin/user_analysis.html', {
#             'user': user,
#             'statistics': {
#                 'posts': posts_count,
#                 'likes': likes_given,
#                 'comments': comments_count,
#                 'followers': followers_count,
#                 'following': following_count
#             },
#             'ai_analysis': result.get('response', 'خطا در دریافت تحلیل'),
#             'title': f'تحلیل کاربر {user.phone}'
#         })


# # رجیستر
# try:
#     admin.site.unregister(User)
# except:
#     pass
# admin.site.register(User, CustomUserAdmin)














# apps/ml/admin.py - نسخه اصلاح شده

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import path
from django.http import JsonResponse
from django.utils.html import format_html
from .services.ollama_client import OllamaClient
from django.db.models import Count

User = get_user_model()


class MLAdminPanel(admin.AdminSite):
    """پنل ادمین جداگانه برای ML"""
    site_header = "مدیریت هوش مصنوعی"
    site_title = "سیستم تحلیل با AI"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('analyze/<str:user_id>/', self.analyze_view, name='ml-analyze-user'),
        ]
        return custom_urls + urls
    
    def analyze_view(self, request, user_id):
        """تحلیل کاربر با AI"""
        try:
            # پیدا کردن کاربر
            try:
                user = User.objects.get(id=user_id)
            except (ValueError, User.DoesNotExist):
                try:
                    user = User.objects.get(id=int(user_id))
                except:
                    return JsonResponse({
                        'success': False,
                        'error': f'کاربر با آیدی {user_id} یافت نشد'
                    }, status=404)
            
            # اطلاعات پروفایل
            profile_data = {
                'full_name': None,
                'bio': None,
                'avatar': None
            }
            try:
                if hasattr(user, 'profile') and user.profile:
                    profile_data['full_name'] = user.profile.full_name
                    profile_data['bio'] = user.profile.bio
                    if user.profile.avatar:
                        profile_data['avatar'] = user.profile.avatar.url
            except:
                pass
            
            # آمار پست‌ها
            posts_count = 0
            total_likes_received = 0
            try:
                from apps.posts.models import Post
                posts = Post.objects.filter(user=user)
                posts_count = posts.count()
                # اصلاح: استفاده از count مستقیم
                total_likes_received = sum(p.likes.count() for p in posts)
            except Exception as e:
                print(f"Error in posts: {e}")
            
            # آمار لایک‌ها
            likes_given = 0
            try:
                from apps.posts.models import Like
                likes_given = Like.objects.filter(user=user).count()
            except:
                pass
            
            # آمار کامنت‌ها
            comments_count = 0
            try:
                from apps.posts.models import Comment
                comments_count = Comment.objects.filter(user=user).count()
            except:
                pass
            
            # آمار فالو
            followers_count = 0
            following_count = 0
            try:
                from apps.follows.models import Follow
                followers_count = Follow.objects.filter(following=user).count()
                following_count = Follow.objects.filter(follower=user).count()
            except:
                pass
            
            # هشتگ‌های پرتکرار
            top_hashtags = []
            try:
                from apps.hashtags.models import PostHashtag
                hashtags = PostHashtag.objects.filter(post__user=user).values('hashtag__name').annotate(
                    count=Count('id')).order_by('-count')[:5]
                top_hashtags = [
                    {'name': h['hashtag__name'], 'count': h['count']} 
                    for h in hashtags if h['hashtag__name']
                ]
            except:
                pass
            
            # سطح فعالیت
            activity_score = (posts_count * 10) + (likes_given * 2) + (comments_count * 3)
            if activity_score > 100:
                activity_level = "high"
                activity_level_fa = "زیاد"
            elif activity_score > 50:
                activity_level = "medium"
                activity_level_fa = "متوسط"
            else:
                activity_level = "low"
                activity_level_fa = "کم"
            
            # ساخت پرامپت
            prompt = f"""
کاربر شبکه اجتماعی را تحلیل کن:

اطلاعات:
- شماره: {user.phone}
- نام: {profile_data['full_name'] or 'ثبت نشده'}
- بیو: {profile_data['bio'] or 'ثبت نشده'}

آمار:
- پست: {posts_count}
- لایک داده: {likes_given}
- کامنت: {comments_count}
- دنبال‌کننده: {followers_count}
- دنبال‌شونده: {following_count}
- لایک دریافتی: {total_likes_received}

هشتگ‌ها: {', '.join([f"#{h['name']}" for h in top_hashtags]) if top_hashtags else 'هیچ'}

پاسخ را فقط به صورت JSON بده با این ساختار:
{{
    "personality_type": "نوع شخصیت",
    "content_preferences": ["نوع محتوا 1", "نوع محتوا 2"],
    "strengths": ["نقطه قوت 1", "نقطه قوت 2"],
    "weaknesses": ["نقطه ضعف 1", "نقطه ضعف 2"],
    "suggestions": ["پیشنهاد 1", "پیشنهاد 2", "پیشنهاد 3"],
    "recommended_hashtags": ["هشتگ1", "هشتگ2"],
    "summary": "توصیه خلاصه"
}}
"""
            
            client = OllamaClient()
            result = client.generate(prompt, temperature=0.7, max_tokens=1000)
            
            # Parse کردن JSON
            import json
            ai_analysis = {}
            if result.get('success'):
                try:
                    response_text = result.get('response', '')
                    start = response_text.find('{')
                    end = response_text.rfind('}') + 1
                    if start != -1 and end != 0:
                        json_str = response_text[start:end]
                        ai_analysis = json.loads(json_str)
                    else:
                        ai_analysis = {'raw_response': response_text}
                except:
                    ai_analysis = {'raw_response': result.get('response', '')}
            
            # برگرداندن پاسخ
            return JsonResponse({
                'success': result.get('success', False),
                'user': {
                    'id': str(user.id),
                    'phone': user.phone,
                    'date_joined': user.date_joined.isoformat() if user.date_joined else None,
                    'is_active': user.is_active,
                    'profile': profile_data
                },
                'statistics': {
                    'posts_count': posts_count,
                    'likes_given': likes_given,
                    'comments_count': comments_count,
                    'followers_count': followers_count,
                    'following_count': following_count,
                    'total_likes_received': total_likes_received,
                    'activity_score': activity_score,
                    'activity_level': activity_level,
                    'activity_level_fa': activity_level_fa
                },
                'top_hashtags': top_hashtags,
                'ai_analysis': ai_analysis,
                'error': result.get('error', '')
            }, json_dumps_params={'ensure_ascii': False})
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


# ایجاد نمونه از پنل ادمین ML
ml_admin_site = MLAdminPanel(name='ml')


# اگر می‌خواهی در ادمین اصلی هم دکمه داشته باشی:
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'is_active', 'analyze_button')
    search_fields = ('phone',)
    
    def analyze_button(self, obj):
        return format_html(
            '<a class="button" href="/admin/ml/analyze/{}/" target="_blank">🤖 تحلیل با AI</a>',
            obj.id
        )
    analyze_button.short_description = 'تحلیل هوشمند'


# رجیستر کردن
try:
    admin.site.unregister(User)
except:
    pass

admin.site.register(User, CustomUserAdmin)


























































