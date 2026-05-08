# apps/interactions/views.py

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from apps.posts.serializers import PostSerializer
from .services.explore_feed import ExploreFeedService
from .serializers import (
    ExploreFeedQuerySerializer,
    ExploreFeedResponseSerializer,
    ExplorePostDataSerializer
)


class ExploreFeedView(GenericAPIView):
    """
    View for exploring personalized feed content
    
    Returns a personalized feed of posts based on user interests,
    hashtag preferences, and optionally AI-powered recommendations using Ollama.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ExploreFeedQuerySerializer
    
    def get(self, request):
        """
        Get personalized explore feed
        """
        # Validate query parameters
        query_serializer = self.get_serializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        
        # Extract validated parameters
        limit = query_serializer.validated_data.get('limit', 20)
        offset = query_serializer.validated_data.get('offset', 0)
        use_ollama = query_serializer.validated_data.get('use_ollama', True)
        
        # Initialize explore service
        explore_service = ExploreFeedService(request.user)
        
        # Get personalized feed data
        feed_data = explore_service.get_explore_feed(
            limit=limit,
            offset=offset,
            use_ollama=use_ollama
        )
        
        # Serialize posts
        serializer = PostSerializer(
            feed_data['posts'],
            many=True,
            context={'request': request}
        )
        
        # Enhance post data with explore metadata
        response_posts = []
        for idx, post_data in enumerate(serializer.data):
            post_data['explore_score'] = feed_data['scores'][idx]
            post_data['explore_reasons'] = feed_data['reasons'][idx]
            response_posts.append(post_data)
        
        # Prepare response
        response_data = {
            "success": True,
            "data": {
                "posts": response_posts,
                "used_hashtags": feed_data['used_hashtags'],
                "used_ollama": feed_data['used_ollama'],
                "pagination": {
                    "total_count": feed_data['total_count'],
                    "has_next": feed_data['has_next'],
                    "limit": limit,
                    "offset": offset
                }
            }
        }
        
        return Response(response_data, status=status.HTTP_200_OK)


class PersonalizedRecommendationsView(GenericAPIView):
    """
    View for getting personalized content recommendations
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ExploreFeedQuerySerializer
    
    def get(self, request):
        """
        Get personalized recommendations based on user behavior
        """
        query_serializer = self.get_serializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        
        limit = query_serializer.validated_data.get('limit', 10)
        use_ollama = query_serializer.validated_data.get('use_ollama', True)
        
        explore_service = ExploreFeedService(request.user)
        
        # Get recommendations
        recommendations = explore_service.get_personalized_recommendations(
            limit=limit,
            use_ollama=use_ollama
        )
        
        return Response({
            "success": True,
            "data": recommendations
        }, status=status.HTTP_200_OK)


class SimilarContentView(GenericAPIView):
    """
    View for getting content similar to a specific post
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, post_id):
        """
        Get posts similar to the specified post
        """
        from apps.posts.models import Post
        
        # Validate post_id
        try:
            post = Post.objects.get(id=post_id, is_active=True)
        except Post.DoesNotExist:
            return Response({
                "success": False,
                "error": "Post not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        limit = min(int(request.query_params.get('limit', 10)), 30)
        
        explore_service = ExploreFeedService(request.user)
        
        similar_posts = explore_service.get_similar_posts(
            post=post,
            limit=limit
        )
        
        serializer = PostSerializer(
            similar_posts,
            many=True,
            context={'request': request}
        )
        
        return Response({
            "success": True,
            "data": {
                "original_post_id": post_id,
                "similar_posts": serializer.data,
                "count": len(serializer.data)
            }
        }, status=status.HTTP_200_OK)