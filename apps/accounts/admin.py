# # from django.contrib import admin

# # # Register your models here.


# # # apps/accounts/admin.py


# # # apps/accounts/admin.py - اضافه کردن متدهای تحلیل به ادمین موجود

# # from django.contrib import admin
# # from django.contrib.auth import get_user_model
# # from django.contrib.auth.admin import UserAdmin
# # from django.http import JsonResponse
# # from django.urls import path
# # from django.contrib import admin
# # from .models import User, OTP

# # @admin.register(User)
# # class UserAdmin(admin.ModelAdmin):
# #     list_display = ['id', 'phone', 'username', 'is_active', 'is_staff', 'date_joined']
# #     list_filter = ['is_active', 'is_staff']
# #     search_fields = ['phone', 'username']
# #     readonly_fields = ['id', 'date_joined']

# # @admin.register(OTP)
# # class OTPAdmin(admin.ModelAdmin):
# #     list_display = ['id', 'phone', 'code', 'created_at', 'expires_at', 'is_used']
# #     list_filter = ['is_used', 'created_at']
# #     search_fields = ['phone']
# #     readonly_fields = ['id', 'created_at']




# # User = get_user_model()

# # @admin.register(User)
# # class CustomUserAdmin(UserAdmin):
# #     # ... کدهای موجود ...
    
# #     def get_urls(self):
# #         urls = super().get_urls()
# #         custom_urls = [
# #             path('analyze/<int:user_id>/', 
# #                  self.admin_site.admin_view(self.analyze_user),
# #                  name='analyze_user'),
# #         ]
# #         return custom_urls + urls
    
# #     def analyze_user(self, request, user_id):
# #         from apps.ml.services.personality_analyzer import PersonalityAnalyzer
# #         # ... بقیه کد





# # apps/accounts/admin.py - نسخه صحیح

# # from django.contrib import admin
# # from django.contrib.auth import get_user_model
# # from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# # from django.http import JsonResponse
# # from django.urls import path
# # from .models import User, OTP

# # # ============================================================
# # # رجیستر OTP
# # # ============================================================
# # @admin.register(OTP)
# # class OTPAdmin(admin.ModelAdmin):
# #     list_display = ['id', 'phone', 'code', 'created_at', 'expires_at', 'is_used']
# #     list_filter = ['is_used', 'created_at']
# #     search_fields = ['phone']
# #     readonly_fields = ['id', 'created_at']


# # ============================================================
# # رجیستر User - فقط یک بار
# # ============================================================
# # @admin.register(User)
# # class CustomUserAdmin(BaseUserAdmin):
# #     """ادمین سفارشی User با قابلیت تحلیل شخصیت"""
    
# #     # تنظیمات نمایش
# #     list_display = ['id', 'phone', 'username', 'is_active', 'is_staff', 'date_joined']
# #     list_filter = ['is_active', 'is_staff']
# #     search_fields = ['phone', 'username']
# #     readonly_fields = ['id', 'date_joined']
    
# #     # فیلدهای مورد نیاز UserAdmin
# #     fieldsets = (
# #         (None, {'fields': ('username', 'password')}),
# #         ('اطلاعات شخصی', {'fields': ('phone', 'email', 'first_name', 'last_name')}),
# #         ('دسترسی‌ها', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
# #         ('تاریخ‌ها', {'fields': ('last_login', 'date_joined')}),
# #     )
    
# #     add_fieldsets = (
# #         (None, {
# #             'classes': ('wide',),
# #             'fields': ('username', 'phone', 'password1', 'password2'),
# #         }),
# #     )
    
# #     # ============================================================
# #     # متدهای تحلیل شخصیت
# #     # ============================================================
    
# #     def get_urls(self):
# #         """اضافه کردن URL سفارشی برای تحلیل"""
# #         urls = super().get_urls()
# #         custom_urls = [
# #             path(
# #                 'analyze/<int:user_id>/',
# #                 self.admin_site.admin_view(self.analyze_user),
# #                 name='analyze_user'
# #             ),
# #         ]
# #         return custom_urls + urls
    
# #     def analyze_user(self, request, user_id):
# #         """API تحلیل شخصیت کاربر - خروجی JSON"""
# #         from apps.ml.services.personality_analyzer import PersonalityAnalyzer
        
# #         try:
# #             user = User.objects.get(id=user_id)
# #             analyzer = PersonalityAnalyzer(user)
# #             analysis = analyzer.analyze_complete_profile()
            
# #             # برگرداندن JSON خالص
# #             return JsonResponse(
# #                 analysis,
# #                 json_dumps_params={'ensure_ascii': False, 'indent': 2}
# #             )
            
# #         except User.DoesNotExist:
# #             return JsonResponse(
# #                 {'error': 'کاربر یافت نشد'},
# #                 status=404
# #             )
# #         except Exception as e:
# #             return JsonResponse(
# #                 {'error': str(e)},
# #                 status=500
# #             )
    
# #     # اکشن برای تحلیل کاربران انتخاب شده
# #     def analyze_selected_users(self, request, queryset):
# #         """اکشن برای تحلیل چند کاربر"""
# #         results = []
# #         from apps.ml.services.personality_analyzer import PersonalityAnalyzer
        
# #         for user in queryset:
# #             analyzer = PersonalityAnalyzer(user)
# #             analysis = analyzer.analyze_complete_profile()
# #             results.append({
# #                 'user_id': user.id,
# #                 'username': user.username,
# #                 'phone': user.phone,
# #                 'personality_type': analysis['personality_profile']['personality_type'],
# #                 'engagement_rate': analysis['behavioral_metrics']['engagement_rate']
# #             })
        
# #         return JsonResponse({
# #             'total': len(results),
# #             'results': results
# #         }, json_dumps_params={'ensure_ascii': False, 'indent': 2})
    
# #     analyze_selected_users.short_description = "🔍 تحلیل شخصیت کاربر(های) انتخاب شده"
    
# #     # اضافه کردن اکشن به ادمین
# #     actions = ['analyze_selected_users']


# # دومی 




































































# # # apps/accounts/admin.py
# # from django.contrib import admin
# # from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# # from django.http import JsonResponse
# # from django.urls import path
# # from .models import User, OTP

# # # ============================================================
# # # رجیستر OTP
# # # ============================================================
# # @admin.register(OTP)
# # class OTPAdmin(admin.ModelAdmin):
# #     list_display = ['id', 'phone', 'code', 'created_at', 'expires_at', 'is_used']
# #     list_filter = ['is_used', 'created_at']
# #     search_fields = ['phone']
# #     readonly_fields = ['id', 'created_at']


# # # ============================================================
# # # رجیستر User - با قابلیت‌های ML
# # # ============================================================
# # @admin.register(User)
# # class CustomUserAdmin(BaseUserAdmin):
# #     """ادمین سفارشی User با قابلیت تحلیل شخصیت"""
    
# #     # تنظیمات نمایش در لیست کاربران
# #     list_display = ['id', 'phone', 'username', 'is_active', 'is_staff', 'date_joined']
# #     list_filter = ['is_active', 'is_staff']
# #     search_fields = ['phone', 'username']
# #     readonly_fields = ['id', 'date_joined', 'last_login']
    
# #     # فیلدهایی که در فرم نمایش داده می‌شوند
# #     fieldsets = (
# #         (None, {'fields': ('username', 'password')}),
# #         ('اطلاعات شخصی', {'fields': ('phone',)}),
# #         ('دسترسی‌ها', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
# #         ('تاریخ‌ها', {'fields': ('last_login', 'date_joined')}),
# #     )
    
# #     # فیلدهایی که در فرم ایجاد کاربر جدید نمایش داده می‌شوند
# #     add_fieldsets = (
# #         (None, {
# #             'classes': ('wide',),
# #             'fields': ('username', 'phone', 'password1', 'password2'),
# #         }),
# #     )
    
# #     # ============================================================
# #     # متدهای تحلیل شخصیت (ML)
# #     # ============================================================
    
# #     def get_urls(self):
# #         """اضافه کردن URL سفارشی برای تحلیل"""
# #         urls = super().get_urls()
# #         custom_urls = [
# #             path(
# #                 'analyze/<uuid:user_id>/',
# #                 self.admin_site.admin_view(self.analyze_user),
# #                 name='analyze_user'
# #             ),
# #         ]
# #         return custom_urls + urls
    
# #     def analyze_user(self, request, user_id):
# #         """API تحلیل شخصیت کاربر - خروجی JSON"""
# #         try:
# #             # بررسی وجود سرویس ML
# #             try:
# #                 from apps.ml.services.personality_analyzer import PersonalityAnalyzer
# #             except ImportError:
# #                 return JsonResponse(
# #                     {'error': 'سرویس تحلیل شخصیت در دسترس نیست'},
# #                     status=503
# #                 )
            
# #             user = User.objects.get(id=user_id)
# #             analyzer = PersonalityAnalyzer(user)
# #             analysis = analyzer.analyze_complete_profile()
            
# #             return JsonResponse(
# #                 analysis,
# #                 json_dumps_params={'ensure_ascii': False, 'indent': 2}
# #             )
            
# #         except User.DoesNotExist:
# #             return JsonResponse(
# #                 {'error': 'کاربر یافت نشد'},
# #                 status=404
# #             )
# #         except Exception as e:
# #             return JsonResponse(
# #                 {'error': str(e)},
# #                 status=500
# #             )
    
# #     def analyze_selected_users(self, request, queryset):
# #         """اکشن برای تحلیل چند کاربر"""
# #         results = []
        
# #         try:
# #             from apps.ml.services.personality_analyzer import PersonalityAnalyzer
# #         except ImportError:
# #             self.message_user(request, 'سرویس تحلیل شخصیت در دسترس نیست')
# #             return
        
# #         for user in queryset:
# #             try:
# #                 analyzer = PersonalityAnalyzer(user)
# #                 analysis = analyzer.analyze_complete_profile()
# #                 results.append({
# #                     'user_id': str(user.id),
# #                     'username': user.username,
# #                     'phone': user.phone,
# #                     'personality_type': analysis.get('personality_profile', {}).get('personality_type', 'N/A'),
# #                     'engagement_rate': analysis.get('behavioral_metrics', {}).get('engagement_rate', 0)
# #                 })
# #             except Exception as e:
# #                 results.append({
# #                     'user_id': str(user.id),
# #                     'username': user.username,
# #                     'phone': user.phone,
# #                     'error': str(e)
# #                 })
        
# #         return JsonResponse({
# #             'total': len(results),
# #             'results': results
# #         }, json_dumps_params={'ensure_ascii': False, 'indent': 2})
    
# #     analyze_selected_users.short_description = "🔍 تحلیل شخصیت کاربر(های) انتخاب شده"
    
# #     # اضافه کردن اکشن به ادمین
# #     actions = ['analyze_selected_users']


















































































# # apps/accounts/admin.py - نسخه نهایی
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.http import JsonResponse
# from django.urls import path
# from django.utils.html import format_html
# from .models import User, OTP

# # ============================================================
# # رجیستر OTP
# # ============================================================
# @admin.register(OTP)
# class OTPAdmin(admin.ModelAdmin):
#     list_display = ['id', 'phone', 'code', 'created_at', 'expires_at', 'is_used']
#     list_filter = ['is_used', 'created_at']
#     search_fields = ['phone']
#     readonly_fields = ['id', 'created_at']


# # ============================================================
# # رجیستر User - با قابلیت‌های ML
# # ============================================================
# @admin.register(User)
# class CustomUserAdmin(BaseUserAdmin):
#     """ادمین سفارشی User با قابلیت تحلیل شخصیت"""
    
#     list_display = ['id', 'phone', 'username', 'is_active', 'is_staff', 'date_joined', 'analyze_button']
#     list_filter = ['is_active', 'is_staff']
#     search_fields = ['phone', 'username']
#     readonly_fields = ['id', 'date_joined', 'last_login']
    
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('اطلاعات شخصی', {'fields': ('phone',)}),
#         ('دسترسی‌ها', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('تاریخ‌ها', {'fields': ('last_login', 'date_joined')}),
#     )
    
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'phone', 'password1', 'password2'),
#         }),
#     )
    
#     # ============================================================
#     # دکمه تحلیل - با آدرس صحیح
#     # ============================================================
# def analyze_button(self, obj):
#     from django.utils.html import format_html
#     return format_html(
#         '<a class="button" href="/admin/analyze-user/{}/" target="_blank" style="background:#2c3e50; color:white; padding:5px 12px; text-decoration:none; border-radius:4px;">🤖 تحلیل با AI</a>',
#         obj.id
#     )

#     # ============================================================
#     # اکشن گروهی
#     # ============================================================
#     def analyze_selected_users(self, request, queryset):
#         from django.http import HttpResponse
#         import json
        
#         results = []
#         for user in queryset:
#             results.append({
#                 'user_id': str(user.id),
#                 'phone': user.phone,
#                 'username': user.username,
#             })
        
#         return JsonResponse({
#             'status': 'success',
#             'users': results
#         }, json_dumps_params={'ensure_ascii': False})
    
#     analyze_selected_users.short_description = "🔍 تحلیل کاربران انتخاب شده"
#     actions = ['analyze_selected_users']









from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http import JsonResponse
from django.utils.html import format_html
from .models import User, OTP


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone', 'code', 'created_at', 'expires_at', 'is_used']
    list_filter = ['is_used', 'created_at']
    search_fields = ['phone']
    readonly_fields = ['id', 'created_at']


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ['id', 'phone', 'username', 'is_active', 'is_staff', 'date_joined', 'analyze_button']
    list_filter = ['is_active', 'is_staff']
    search_fields = ['phone', 'username']
    readonly_fields = ['id', 'date_joined', 'last_login']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('اطلاعات شخصی', {'fields': ('phone',)}),
        ('دسترسی‌ها', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('تاریخ‌ها', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'phone', 'password1', 'password2'),
        }),
    )
    
    def analyze_button(self, obj):
        return format_html(
            '<a class="button" href="/api/ml/users/{}/analyze/" target="_blank" style="background:#2c3e50; color:white; padding:5px 12px; text-decoration:none; border-radius:4px;">🤖 تحلیل با AI</a>',
            obj.id
        )
    analyze_button.short_description = 'تحلیل هوشمند'
    
    def analyze_selected_users(self, request, queryset):
        results = []
        for user in queryset:
            results.append({
                'user_id': str(user.id),
                'phone': user.phone,
                'username': user.username,
            })
        return JsonResponse({
            'status': 'success',
            'users': results
        }, json_dumps_params={'ensure_ascii': False})
    
    analyze_selected_users.short_description = "🔍 تحلیل کاربران انتخاب شده"
    actions = ['analyze_selected_users']