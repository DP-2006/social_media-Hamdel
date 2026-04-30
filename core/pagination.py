# core/pagination.py

from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    """Pagination استاندارد برای لیست‌ها"""
    page_size = 20  # پیش‌فرض 20 آیتم در هر صفحه
    page_size_query_param = 'page_size'
    max_page_size = 100


class CommentsPagination(PageNumberPagination):
    """Pagination مخصوص کامنت‌ها (چون معمولاً زیاد هستند)"""
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100


class MessagesPagination(PageNumberPagination):
    """Pagination مخصوص پیام‌ها"""
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200