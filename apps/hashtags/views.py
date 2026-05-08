# apps/hashtags/views.py

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from django.db.models import Q
from .models import Hashtag, PostHashtag
from .serializers import (
    HashtagSerializer, 
    TrendingHashtagSerializer,
    HashtagSearchSerializer,
    HashtagPostsSerializer
)
from core.pagination import StandardPagination
from django.db import models


class HashtagViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """
    ViewSet for managing hashtags
    Provides endpoints for listing, searching, trending hashtags and their posts
    """
    serializer_class = HashtagSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardPagination
    lookup_field = 'name'
    lookup_value_regex = '[^/]+'  # Allow special characters in hashtag name

    def get_queryset(self):
        """
        Filter hashtags by search query if provided
        """
        query = self.request.query_params.get('search', '')
        if query:
            return Hashtag.objects.filter(name__icontains=query)
        return Hashtag.objects.all()

    @action(detail=False, methods=['get'], url_path='trending')
    def trending(self, request):
        """
        Get trending hashtags (most used)
        Returns top 20 hashtags ordered by usage count
        """
        hashtags = Hashtag.objects.order_by('-usage_count')[:20]
        serializer = TrendingHashtagSerializer(hashtags, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='posts')
    def posts(self, request, name=None):
        """
        Get all posts associated with a specific hashtag
        """
        hashtag = self.get_object()
        post_hashtags = PostHashtag.objects.filter(hashtag=hashtag).select_related('post', 'post__user')
        
        # Pagination
        page = self.paginate_queryset(post_hashtags)
        if page is not None:
            from apps.posts.serializers import PostSerializer
            posts = [ph.post for ph in page]
            serializer = PostSerializer(posts, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        from apps.posts.serializers import PostSerializer
        posts = [ph.post for ph in post_hashtags]
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='search')
    def search_hashtags(self, request):
        """
        Search hashtags by name
        """
        serializer = HashtagSearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        query = serializer.validated_data.get('q', '')
        limit = serializer.validated_data.get('limit', 20)
        
        if query:
            hashtags = Hashtag.objects.filter(name__icontains=query)[:limit]
        else:
            hashtags = Hashtag.objects.all()[:limit]
        
        response_serializer = HashtagSerializer(hashtags, many=True)
        return Response({
            'success': True,
            'count': len(hashtags),
            'data': response_serializer.data
        })

    @action(detail=True, methods=['get'], url_path='stats')
    def stats(self, request, name=None):
        """
        Get detailed statistics for a specific hashtag
        """
        hashtag = self.get_object()
        
        # Get post count for this hashtag
        post_count = PostHashtag.objects.filter(hashtag=hashtag).count()
        
        return Response({
            'success': True,
            'data': {
                'id': hashtag.id,
                'name': hashtag.name,
                'usage_count': hashtag.usage_count,
                'post_count': post_count,
                'created_at': hashtag.created_at
            }
        })


class HashtagSuggestView(GenericViewSet):
    """
    ViewSet for hashtag suggestions
    """
    permission_classes = [AllowAny]
    serializer_class = HashtagSearchSerializer
    
    def list(self, request):
        """
        Get hashtag suggestions based on partial input
        """
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        query = serializer.validated_data.get('q', '')
        limit = serializer.validated_data.get('limit', 10)
        
        if len(query) < 2:
            return Response({
                'success': True,
                'data': []
            })
        
        suggestions = Hashtag.objects.filter(
            name__icontains=query
        ).order_by('-usage_count')[:limit]
        
        response_serializer = HashtagSerializer(suggestions, many=True)
        return Response({
            'success': True,
            'data': response_serializer.data
        })