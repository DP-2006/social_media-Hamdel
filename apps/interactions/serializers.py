# apps/interactions/serializers.py

from rest_framework import serializers


class ExploreFeedQuerySerializer(serializers.Serializer):
    """
    Serializer for explore feed query parameters
    """
    limit = serializers.IntegerField(
        required=False,
        default=20,
        min_value=1,
        max_value=50,
        help_text="Number of posts to return (max 50)"
    )
    offset = serializers.IntegerField(
        required=False,
        default=0,
        min_value=0,
        help_text="Number of posts to skip for pagination"
    )
    use_ollama = serializers.BooleanField(
        required=False,
        default=True,
        help_text="Whether to use Ollama AI for personalized recommendations"
    )
    
    def validate_limit(self, value):
        if value > 50:
            raise serializers.ValidationError("Limit cannot exceed 50")
        return value
    
    def validate_offset(self, value):
        if value < 0:
            raise serializers.ValidationError("Offset cannot be negative")
        return value


class ExplorePostDataSerializer(serializers.Serializer):
    """
    Serializer for individual post data in explore feed
    """
    explore_score = serializers.FloatField(help_text="Relevance score for the post")
    explore_reasons = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="Reasons why this post was recommended"
    )


class ExploreFeedPaginationSerializer(serializers.Serializer):
    """
    Serializer for pagination metadata in explore feed
    """
    total_count = serializers.IntegerField(help_text="Total number of available posts")
    has_next = serializers.BooleanField(help_text="Whether there are more posts available")
    limit = serializers.IntegerField(help_text="Number of posts per page")
    offset = serializers.IntegerField(help_text="Current offset value")


class ExploreFeedDataSerializer(serializers.Serializer):
    """
    Serializer for the data object in explore feed response
    """
    posts = serializers.ListField(
        child=serializers.DictField(),
        help_text="List of posts with explore metadata"
    )
    used_hashtags = serializers.ListField(
        child=serializers.CharField(),
        help_text="Hashtags used for recommendation"
    )
    used_ollama = serializers.BooleanField(help_text="Whether Ollama was used for recommendations")
    pagination = ExploreFeedPaginationSerializer(help_text="Pagination information")


class ExploreFeedResponseSerializer(serializers.Serializer):
    """
    Serializer for complete explore feed response
    """
    success = serializers.BooleanField(default=True)
    data = ExploreFeedDataSerializer()


class RecommendationItemSerializer(serializers.Serializer):
    """
    Serializer for individual recommendation item
    """
    id = serializers.IntegerField()
    type = serializers.ChoiceField(choices=['post', 'hashtag', 'user'])
    score = serializers.FloatField()
    reason = serializers.CharField()
    data = serializers.DictField()


class PersonalizedRecommendationsSerializer(serializers.Serializer):
    """
    Serializer for personalized recommendations response
    """
    success = serializers.BooleanField(default=True)
    data = serializers.ListField(child=RecommendationItemSerializer())


class SimilarContentQuerySerializer(serializers.Serializer):
    """
    Serializer for similar content query parameters
    """
    limit = serializers.IntegerField(
        required=False,
        default=10,
        min_value=1,
        max_value=30,
        help_text="Number of similar posts to return"
    )


class SimilarContentResponseSerializer(serializers.Serializer):
    """
    Serializer for similar content response
    """
    success = serializers.BooleanField(default=True)
    data = serializers.DictField()


class InteractionStatsSerializer(serializers.Serializer):
    """
    Serializer for user interaction statistics
    """
    total_likes = serializers.IntegerField()
    total_comments = serializers.IntegerField()
    total_shares = serializers.IntegerField()
    total_views = serializers.IntegerField()
    engagement_rate = serializers.FloatField()
    preferred_categories = serializers.ListField(child=serializers.CharField())
    preferred_hashtags = serializers.ListField(child=serializers.CharField())


class UserInterestSerializer(serializers.Serializer):
    """
    Serializer for user interests data
    """
    hashtags = serializers.ListField(child=serializers.CharField())
    categories = serializers.ListField(child=serializers.CharField())
    topics = serializers.ListField(child=serializers.CharField())
    last_updated = serializers.DateTimeField()






class ExploreFeedQuerySerializer(serializers.Serializer):
    """
    Serializer for explore feed query parameters
    """
    limit = serializers.IntegerField(
        required=False,
        default=20,
        min_value=1,
        max_value=50,
        help_text="Number of posts to return (max 50)"
    )
    offset = serializers.IntegerField(
        required=False,
        default=0,
        min_value=0,
        help_text="Number of posts to skip for pagination"
    )
    use_ollama = serializers.BooleanField(
        required=False,
        default=True,
        help_text="Whether to use Ollama AI for personalized recommendations"
    )
    
    def validate_limit(self, value):
        if value > 50:
            raise serializers.ValidationError("Limit cannot exceed 50")
        return value
    
    def validate_offset(self, value):
        if value < 0:
            raise serializers.ValidationError("Offset cannot be negative")
        return value


class ExplorePostDataSerializer(serializers.Serializer):
    """
    Serializer for individual post data in explore feed
    """
    explore_score = serializers.FloatField(help_text="Relevance score for the post")
    explore_reasons = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="Reasons why this post was recommended"
    )


class ExploreFeedPaginationSerializer(serializers.Serializer):
    """
    Serializer for pagination metadata in explore feed
    """
    total_count = serializers.IntegerField(help_text="Total number of available posts")
    has_next = serializers.BooleanField(help_text="Whether there are more posts available")
    limit = serializers.IntegerField(help_text="Number of posts per page")
    offset = serializers.IntegerField(help_text="Current offset value")


class ExploreFeedDataSerializer(serializers.Serializer):
    """
    Serializer for the data object in explore feed response
    """
    posts = serializers.ListField(
        child=serializers.DictField(),
        help_text="List of posts with explore metadata"
    )
    used_hashtags = serializers.ListField(
        child=serializers.CharField(),
        help_text="Hashtags used for recommendation"
    )
    used_ollama = serializers.BooleanField(help_text="Whether Ollama was used for recommendations")
    pagination = ExploreFeedPaginationSerializer(help_text="Pagination information")


class ExploreFeedResponseSerializer(serializers.Serializer):
    """
    Serializer for complete explore feed response
    """
    success = serializers.BooleanField(default=True)
    data = ExploreFeedDataSerializer()


class RecommendationItemSerializer(serializers.Serializer):
    """
    Serializer for individual recommendation item
    """
    id = serializers.IntegerField()
    type = serializers.ChoiceField(choices=['post', 'hashtag', 'user'])
    score = serializers.FloatField()
    reason = serializers.CharField()
    data = serializers.DictField()


class PersonalizedRecommendationsSerializer(serializers.Serializer):
    """
    Serializer for personalized recommendations response
    """
    success = serializers.BooleanField(default=True)
    data = serializers.ListField(child=RecommendationItemSerializer())


class SimilarContentQuerySerializer(serializers.Serializer):
    """
    Serializer for similar content query parameters
    """
    limit = serializers.IntegerField(
        required=False,
        default=10,
        min_value=1,
        max_value=30,
        help_text="Number of similar posts to return"
    )


class SimilarContentResponseSerializer(serializers.Serializer):
    """
    Serializer for similar content response
    """
    success = serializers.BooleanField(default=True)
    data = serializers.DictField()


class InteractionStatsSerializer(serializers.Serializer):
    """
    Serializer for user interaction statistics
    """
    total_likes = serializers.IntegerField()
    total_comments = serializers.IntegerField()
    total_shares = serializers.IntegerField()
    total_views = serializers.IntegerField()
    engagement_rate = serializers.FloatField()
    preferred_categories = serializers.ListField(child=serializers.CharField())
    preferred_hashtags = serializers.ListField(child=serializers.CharField())


class UserInterestSerializer(serializers.Serializer):
    """
    Serializer for user interests data
    """
    hashtags = serializers.ListField(child=serializers.CharField())
    categories = serializers.ListField(child=serializers.CharField())
    topics = serializers.ListField(child=serializers.CharField())
    last_updated = serializers.DateTimeField()


# ============================================
# NEW: Serializer for ExploreView with fallback
# ============================================

class ExploreViewResponseSerializer(serializers.Serializer):
    """
    Serializer for the new ExploreView with Ollama fallback support
    """
    explore = serializers.ListField(
        child=serializers.DictField(),
        help_text="List of posts"
    )
    count = serializers.IntegerField(help_text="Number of posts returned")
    has_more = serializers.BooleanField(help_text="Whether there are more posts available")
    used_ollama = serializers.BooleanField(help_text="Whether Ollama was used for recommendations")
    algorithm = serializers.ChoiceField(
        choices=['ollama', 'simple'],
        help_text="Algorithm used for recommendations"
    )
    used_hashtags = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="Hashtags used for recommendation (only present with ollama algorithm)"
    )

# apps/interactions/serializers.py

from rest_framework import serializers


class ExploreFeedQuerySerializer(serializers.Serializer):
    """
    Serializer for explore feed query parameters
    """
    limit = serializers.IntegerField(
        required=False,
        default=20,
        min_value=1,
        max_value=50,
        help_text="Number of posts to return (max 50)"
    )
    offset = serializers.IntegerField(
        required=False,
        default=0,
        min_value=0,
        help_text="Number of posts to skip for pagination"
    )
    use_ollama = serializers.BooleanField(
        required=False,
        default=True,
        help_text="Whether to use Ollama AI for personalized recommendations"
    )
    
    def validate_limit(self, value):
        if value > 50:
            raise serializers.ValidationError("Limit cannot exceed 50")
        return value
    
    def validate_offset(self, value):
        if value < 0:
            raise serializers.ValidationError("Offset cannot be negative")
        return value


class ExplorePostDataSerializer(serializers.Serializer):
    """
    Serializer for individual post data in explore feed
    """
    explore_score = serializers.FloatField(help_text="Relevance score for the post")
    explore_reasons = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="Reasons why this post was recommended"
    )


class ExploreFeedPaginationSerializer(serializers.Serializer):
    """
    Serializer for pagination metadata in explore feed
    """
    total_count = serializers.IntegerField(help_text="Total number of available posts")
    has_next = serializers.BooleanField(help_text="Whether there are more posts available")
    limit = serializers.IntegerField(help_text="Number of posts per page")
    offset = serializers.IntegerField(help_text="Current offset value")


class ExploreFeedDataSerializer(serializers.Serializer):
    """
    Serializer for the data object in explore feed response
    """
    posts = serializers.ListField(
        child=serializers.DictField(),
        help_text="List of posts with explore metadata"
    )
    used_hashtags = serializers.ListField(
        child=serializers.CharField(),
        help_text="Hashtags used for recommendation"
    )
    used_ollama = serializers.BooleanField(help_text="Whether Ollama was used for recommendations")
    pagination = ExploreFeedPaginationSerializer(help_text="Pagination information")


class ExploreFeedResponseSerializer(serializers.Serializer):
    """
    Serializer for complete explore feed response
    """
    success = serializers.BooleanField(default=True)
    data = ExploreFeedDataSerializer()


class RecommendationItemSerializer(serializers.Serializer):
    """
    Serializer for individual recommendation item
    """
    id = serializers.IntegerField()
    type = serializers.ChoiceField(choices=['post', 'hashtag', 'user'])
    score = serializers.FloatField()
    reason = serializers.CharField()
    data = serializers.DictField()


class PersonalizedRecommendationsSerializer(serializers.Serializer):
    """
    Serializer for personalized recommendations response
    """
    success = serializers.BooleanField(default=True)
    data = serializers.ListField(child=RecommendationItemSerializer())


class SimilarContentQuerySerializer(serializers.Serializer):
    """
    Serializer for similar content query parameters
    """
    limit = serializers.IntegerField(
        required=False,
        default=10,
        min_value=1,
        max_value=30,
        help_text="Number of similar posts to return"
    )


class SimilarContentResponseSerializer(serializers.Serializer):
    """
    Serializer for similar content response
    """
    success = serializers.BooleanField(default=True)
    data = serializers.DictField()


class InteractionStatsSerializer(serializers.Serializer):
    """
    Serializer for user interaction statistics
    """
    total_likes = serializers.IntegerField()
    total_comments = serializers.IntegerField()
    total_shares = serializers.IntegerField()
    total_views = serializers.IntegerField()
    engagement_rate = serializers.FloatField()
    preferred_categories = serializers.ListField(child=serializers.CharField())
    preferred_hashtags = serializers.ListField(child=serializers.CharField())


class UserInterestSerializer(serializers.Serializer):
    """
    Serializer for user interests data
    """
    hashtags = serializers.ListField(child=serializers.CharField())
    categories = serializers.ListField(child=serializers.CharField())
    topics = serializers.ListField(child=serializers.CharField())
    last_updated = serializers.DateTimeField()


# ============================================
# UPDATED: Serializer for ExploreView with fallback
# trending_by_likes
# ============================================

class ExploreViewResponseSerializer(serializers.Serializer):
    """
    Serializer for the new ExploreView with Ollama fallback support
    """
    explore = serializers.ListField(
        child=serializers.DictField(),
        help_text="List of posts"
    )
    count = serializers.IntegerField(help_text="Number of posts returned")
    has_more = serializers.BooleanField(help_text="Whether there are more posts available")
    used_ollama = serializers.BooleanField(help_text="Whether Ollama was used for recommendations")
    algorithm = serializers.ChoiceField(
        choices=['ollama', 'simple', 'trending_by_likes'],  #trending_by_likes
        help_text="Algorithm used for recommendations"
    )
    used_hashtags = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="Hashtags used for recommendation (only present with ollama algorithm)"
    )
    total_count = serializers.IntegerField(  # total_count
        required=False,
        help_text="Total number of posts available"
    )


# ============================================
# NEW: Serializer for simple explore response (deny Ollama)
# ============================================

class SimpleExploreResponseSerializer(serializers.Serializer):
    """
    Serializer for simple explore response (trending by likes)
    """
    explore = serializers.ListField(
        child=serializers.DictField(),
        help_text="List of posts sorted by likes"
    )
    count = serializers.IntegerField(help_text="Number of posts returned")
    total_count = serializers.IntegerField(help_text="Total number of posts available")
    has_more = serializers.BooleanField(help_text="Whether there are more posts available")
    used_ollama = serializers.BooleanField(
        default=False,
        help_text="Always false for simple explore"
    )
    algorithm = serializers.ChoiceField(
        choices=['trending_by_likes'],
        default='trending_by_likes',
        help_text="Algorithm used for recommendations"
    )