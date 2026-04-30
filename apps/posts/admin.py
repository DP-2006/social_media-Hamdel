#آخرین بخش فعال 
# from django.contrib import admin
# from .models import Post, Like, Comment


# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     list_display = [
#         'id', 
#         'user', 
#         'content_preview', 
#         'likes_count_display',
#         'comments_count_display',
#         'created_at'
#     ]
#     list_filter = ['created_at', 'user']
#     search_fields = ['content', 'user__username']
#     raw_id_fields = ['user']
#     readonly_fields = ['created_at', 'updated_at']
#     date_hierarchy = 'created_at'
    
#     fieldsets = (
#         ("POST_INFORMATION", {
#             "fields": ("user", "content", "image")
#         }),
#         ("TIME", {
#             "fields": ("created_at", "updated_at")
#         }),
#     )
    
#     def content_preview(self, obj):
#         return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
#     content_preview.short_description = 'Mohtava_e_farhangi'
    
#     def likes_count_display(self, obj):
#         return obj.likes_count
#     likes_count_display.short_description = 'LIKE'
#     likes_count_display.admin_order_field = 'likes__count'
    
#     def comments_count_display(self, obj):
#         return obj.comments_count
#     comments_count_display.short_description = 'COMMENT'


# @admin.register(Like)
# class LikeAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'post', 'created_at']
#     list_filter = ['created_at']
#     search_fields = ['user__username', 'post__content']
#     raw_id_fields = ['user', 'post']
#     readonly_fields = ['created_at']
#     date_hierarchy = 'created_at'
    
#     def get_queryset(self, request):
#         return super().get_queryset(request).select_related('user', 'post')


# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ["id", "user", "post", "parent", "created_at"]
#     list_filter = ["created_at", "post"]
#     search_fields = ["text", "user__username", "post__content"]
#     readonly_fields = ["created_at"]
#     raw_id_fields = ['user', 'post', 'parent']
#     date_hierarchy = 'created_at'
    
#     fieldsets = (
#         ("comment infornation", {
#             "fields": ("post", "user", "parent", "text")
#         }),
#         ("TIME", {
#             "fields": ("created_at",)
#         }),
#     )
    
#     def get_queryset(self, request):
#         return super().get_queryset(request).select_related('user', 'post', 'parent')












# # apps/posts/admin.py (نسخه ساده‌تر)

# from django.contrib import admin
# from django.utils.html import format_html
# from .models import Post, Like, Comment

# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     list_display = [
#         'id', 
#         'user', 
#         'content_preview', 
#         'image_preview',
#         'file_link',  # لینک دانلود فایل در ادمین
#         'file_size_display',
#         'likes_count_display',
#         'comments_count_display',
#         'created_at'
#     ]
#     list_filter = ['created_at', 'user']
#     search_fields = ['content', 'user__username', 'file_name']
#     raw_id_fields = ['user']
#     readonly_fields = ['created_at', 'updated_at', 'file_size']
#     date_hierarchy = 'created_at'
    
#     fieldsets = (
#         ("اطلاعات پست", {
#             "fields": ("user", "content", "image")
#         }),
#         ("فایل ضمیمه", {
#             "fields": ("file", "file_name", "file_size"),
#             "classes": ("collapse",),
#             "description": "فایل‌های مجاز: PDF، DOC، DOCX، ZIP، TXT، تصاویر و ویدیوها"
#         }),
#         ("زمان", {
#             "fields": ("created_at", "updated_at")
#         }),
#     )
    
#     def content_preview(self, obj):
#         return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
#     content_preview.short_description = 'متن پست'
    
#     def image_preview(self, obj):
#         """نمایش پیش‌نمایش تصویر در ادمین"""
#         if obj.image:
#             return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover;" />', obj.image.url)
#         return '-'
#     image_preview.short_description = 'تصویر'
    
#     def file_link(self, obj):
#         """لینک دانلود فایل در ادمین"""
#         if obj.file:
#             return format_html('<a href="{}" target="_blank">📎 دانلود {}</a>', 
#                              obj.file.url, 
#                              obj.file_name or 'فایل')
#         return '-'
#     file_link.short_description = 'فایل'
    
#     def file_size_display(self, obj):
#         """نمایش حجم فایل به صورت خوانا"""
#         if obj.file_size:
#             size = obj.file_size
#             for unit in ['B', 'KB', 'MB', 'GB']:
#                 if size < 1024.0:
#                     return f"{size:.1f} {unit}"
#                 size /= 1024.0
#             return f"{size:.1f} TB"
#         return '-'
#     file_size_display.short_description = 'حجم فایل'
    
#     def likes_count_display(self, obj):
#         return obj.likes.count()
#     likes_count_display.short_description = '👍 لایک'
    
#     def comments_count_display(self, obj):
#         return obj.comments.count()
#     comments_count_display.short_description = '💬 کامنت'
    
#     def save_model(self, request, obj, form, change):
#         """ذخیره خودکار اطلاعات فایل"""
#         if obj.file:
#             # استخراج نام فایل
#             if not obj.file_name:
#                 obj.file_name = obj.file.name.split('/')[-1]
            
#             # محاسبه حجم فایل
#             if hasattr(obj.file, 'size') and not obj.file_size:
#                 obj.file_size = obj.file.size
        
#         super().save_model(request, obj, form, change)


# @admin.register(Like)
# class LikeAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'post_preview', 'created_at']
#     list_filter = ['created_at']
#     search_fields = ['user__username', 'post__content']
#     raw_id_fields = ['user', 'post']
#     readonly_fields = ['created_at']
#     date_hierarchy = 'created_at'
    
#     def post_preview(self, obj):
#         return obj.post.content[:50] if obj.post.content else '-'
#     post_preview.short_description = 'متن پست'
    
#     def get_queryset(self, request):
#         return super().get_queryset(request).select_related('user', 'post')


# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ["id", "user", "post_preview", "text_preview", "parent", "created_at"]
#     list_filter = ["created_at", "post"]
#     search_fields = ["text", "user__username", "post__content"]
#     readonly_fields = ["created_at"]
#     raw_id_fields = ['user', 'post', 'parent']
#     date_hierarchy = 'created_at'
    
#     fieldsets = (
#         ("اطلاعات کامنت", {
#             "fields": ("post", "user", "parent", "text")
#         }),
#         ("زمان", {
#             "fields": ("created_at",)
#         }),
#     )
    
#     def post_preview(self, obj):
#         return obj.post.content[:50] if obj.post.content else '-'
#     post_preview.short_description = 'پست'
    
#     def text_preview(self, obj):
#         return obj.text[:100] + '...' if len(obj.text) > 100 else obj.text
#     text_preview.short_description = 'متن کامنت'
    
#     def get_queryset(self, request):
#         return super().get_queryset(request).select_related('user', 'post', 'parent')










































# from django.contrib import admin
# from .models import Post, Like, Comment


# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     list_display = [
#         'id', 
#         'user', 
#         'content_preview',
#         'file_link',  # اضافه شد - نمایش فایل
#         'likes_count_display',
#         'comments_count_display',
#         'created_at'
#     ]
#     list_filter = ['created_at', 'user']
#     search_fields = ['content', 'user__username', 'file_name']  # اضافه شد - جستجو در نام فایل
#     raw_id_fields = ['user']
#     readonly_fields = ['created_at', 'updated_at', 'file_size']  # اضافه شد
#     date_hierarchy = 'created_at'
    
#     fieldsets = (
#         ("POST_INFORMATION", {
#             "fields": ("user", "content", "image")
#         }),
#         ("FILE INFORMATION", {  # سکشن جدید برای فایل
#             "fields": ("file", "file_name", "file_size"),
#             "classes": ("collapse",),  # قابلیت بسته شدن
#             "description": "فایل‌های مجاز: PDF، DOC، DOCX، TXT، ZIP، تصاویر"
#         }),
#         ("TIME", {
#             "fields": ("created_at", "updated_at")
#         }),
#     )
    
#     def content_preview(self, obj):
#         return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
#     content_preview.short_description = 'متن پست'
    
#     def file_link(self, obj):
#         """نمایش لینک فایل در ادمین"""
#         if obj.file:
#             from django.utils.html import format_html
#             return format_html(
#                 '<a href="{}" target="_blank" style="background:#3498db; color:white; padding:2px 8px; text-decoration:none; border-radius:3px;">📎 {}</a>',
#                 obj.file.url,
#                 obj.file_name or 'دانلود فایل'
#             )
#         return '-'
#     file_link.short_description = 'فایل ضمیمه'
    
#     def likes_count_display(self, obj):
#         return obj.likes.count()  # اصلاح شده
#     likes_count_display.short_description = 'تعداد لایک'
    
#     def comments_count_display(self, obj):
#         return obj.comments.count()  # اصلاح شده
#     comments_count_display.short_description = 'تعداد کامنت'


# @admin.register(Like)
# class LikeAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'post', 'created_at']
#     list_filter = ['created_at']
#     search_fields = ['user__username', 'post__content']
#     raw_id_fields = ['user', 'post']
#     readonly_fields = ['created_at']
#     date_hierarchy = 'created_at'
    
#     def get_queryset(self, request):
#         return super().get_queryset(request).select_related('user', 'post')


# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ["id", "user", "post", "parent", "created_at"]
#     list_filter = ["created_at", "post"]
#     search_fields = ["text", "user__username", "post__content"]
#     readonly_fields = ["created_at"]
#     raw_id_fields = ['user', 'post', 'parent']
#     date_hierarchy = 'created_at'
    
#     fieldsets = (
#         ("اطلاعات کامنت", {
#             "fields": ("post", "user", "parent", "text")
#         }),
#         ("زمان", {
#             "fields": ("created_at",)
#         }),
#     )
    
#     def get_queryset(self, request):
#         return super().get_queryset(request).select_related('user', 'post', 'parent')
































from django.contrib import admin
from .models import Post, Like, Comment, PostMedia  # PostMedia رو هم اضافه کن


class PostMediaInline(admin.TabularInline):  # این رو برای نمایش فایل‌ها اضافه کن
    model = PostMedia
    extra = 1
    fields = ['file', 'file_type', 'order']
    show_change_link = True


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'user', 
        'content_preview',
        'media_count',  # تغییر - به جای file_link
        'likes_count_display',
        'comments_count_display',
        'created_at'
    ]
    list_filter = ['created_at', 'user']
    search_fields = ['content', 'user__username'] 
    raw_id_fields = ['user']
    readonly_fields = ['created_at', 'updated_at'] 
    date_hierarchy = 'created_at'
    inlines = [PostMediaInline] 
    
    fieldsets = (
        ("POST_INFORMATION", {
            "fields": ("user", "content", "image", "file")
        }),
        ("TIME", {
            "fields": ("created_at", "updated_at")
        }),
    )
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'متن پست'
    
    def media_count(self, obj):
        """تعداد فایل‌های ارسال شده در پست"""
        count = obj.media_files.count()
        if count == 0:
            return '-'
        return f'{count} فایل'
    media_count.short_description = 'تعداد رسانه‌ها'
    
    def likes_count_display(self, obj):
        return obj.likes.count()
    likes_count_display.short_description = 'تعداد لایک'
    
    def comments_count_display(self, obj):
        return obj.comments.count()
    comments_count_display.short_description = 'تعداد کامنت'


@admin.register(PostMedia)  # این رو اضافه کن برای مدیریت فایل‌ها
class PostMediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'file_name', 'file_type', 'file_size', 'order', 'created_at']
    list_filter = ['file_type', 'created_at']
    search_fields = ['post__user__username', 'file_name', 'post__content']
    readonly_fields = ['created_at', 'file_name', 'file_size']
    raw_id_fields = ['post']
    
    fieldsets = (
        ("اطلاعات فایل", {
            "fields": ("post", "file", "file_type", "order")
        }),
        ("جزئیات فایل", {
            "fields": ("file_name", "file_size"),
            "classes": ("collapse",)
        }),
        ("زمان", {
            "fields": ("created_at",)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.file_name and obj.file:
            obj.file_name = obj.file.name.split('/')[-1]
        if not obj.file_size and obj.file:
            obj.file_size = obj.file.size
        super().save_model(request, obj, form, change)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__content']
    raw_id_fields = ['user', 'post']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'post')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "post", "parent", "created_at"]
    list_filter = ["created_at", "post"]
    search_fields = ["text", "user__username", "post__content"]
    readonly_fields = ["created_at"]
    raw_id_fields = ['user', 'post', 'parent']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ("اطلاعات کامنت", {
            "fields": ("post", "user", "parent", "text")
        }),
        ("زمان", {
            "fields": ("created_at",)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'post', 'parent')

































