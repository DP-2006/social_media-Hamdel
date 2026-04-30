
import json
import requests
from collections import Counter
from datetime import datetime
from django.db.models import Count
from django.utils import timezone
from apps.accounts.models import User
from apps.posts.models import Post
#from apps.interactions.models import Like, Comment
from apps.stories.models import Story
from apps.follows.models import Follow
from apps.hashtags.models import PostHashtag
from apps.messaging.models import Message

class OllamaClient:
    """Client for Ollama AI service"""
    
    def __init__(self, base_url="http://127.0.0.1:11434", model="gemma3:27b"):
        self.base_url = base_url
        self.model = model
    
    def generate(self, prompt, timeout=120):
        """Generate response from AI"""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_ctx": 4096,
                        "temperature": 0.7
                    }
                },
                timeout=timeout
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "response": response.json().get("response", "")
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def analyze_personality_with_ai(self, user_data):
        """Analyze user personality using AI"""
        prompt = f"""
        Analyze this social media user's personality based on their data:

        User Data:
        - Bio: {user_data.get('bio', 'No bio')}
        - Sample posts: {user_data.get('sample_posts', 'No posts')}
        - Top hashtags: {user_data.get('top_hashtags', [])}
        - Posts count: {user_data.get('posts_count', 0)}
        - Followers count: {user_data.get('followers_count', 0)}

        Provide analysis in JSON format with these fields:
        {{
            "personality_type": "MBTI style type",
            "big_five": {{"openness": 0-10, "conscientiousness": 0-10, "extraversion": 0-10, "agreeableness": 0-10, "neuroticism": 0-10}},
            "interests": ["interest1", "interest2"],
            "communication_style": "description",
            "best_time_to_post": "time range",
            "recommendations": ["rec1", "rec2"]
        }}
        """
        
        return self.generate(prompt)


class PersonalityAnalyzer:
    """Personality analyzer for users"""
    
    def __init__(self, user, use_ai=False):
        self.user = user
        self.profile = user.profile if hasattr(user, 'profile') else None
        self.use_ai = use_ai
        self.ollama_client = OllamaClient() if use_ai else None
    
    def analyze_complete_profile(self):
        """Complete personality analysis"""
        
        # Statistical analysis
        result = {
            'user_info': self._get_user_info(),
            'personality_profile': self._analyze_personality(),
            'interests': self._analyze_interests(),
            'behavioral_metrics': self._analyze_behavior(),
            'philosophical_orientation': self._analyze_philosophy(),
            'recommendations': self._generate_recommendations()
        }
        
        # AI enhancement if enabled
        if self.use_ai and self.ollama_client:
            ai_result = self._enhance_with_ai()
            result['ai_enhancement'] = ai_result
        
        return result
    
    def _get_user_info(self):
        """Get basic user info"""
        return {
            'id': str(self.user.id),
            'username': self.user.username,
            'phone': self.user.phone,
            'email': self.user.email,
            'join_date': self.user.date_joined.isoformat(),
            'account_age_days': (timezone.now() - self.user.date_joined).days
        }
    
    def _analyze_personality(self):
        """Analyze personality based on behavior"""
        
        # Get user activity data
        posts_count = Post.objects.filter(user=self.user).count()
        comments_count = Comment.objects.filter(user=self.user).count()
        likes_given = Like.objects.filter(user=self.user).count()
        stories_count = Story.objects.filter(user=self.user).count()
        followers_count = Follow.objects.filter(following=self.user).count()
        following_count = Follow.objects.filter(follower=self.user).count()
        
        # Calculate Big Five scores
        openness = self._calculate_openness()
        conscientiousness = self._calculate_conscientiousness()
        extraversion = self._calculate_extraversion()
        agreeableness = self._calculate_agreeableness()
        neuroticism = self._calculate_neuroticism()
        
        # Determine personality type
        personality_type = self._determine_personality_type({
            'openness': openness,
            'conscientiousness': conscientiousness,
            'extraversion': extraversion,
            'agreeableness': agreeableness,
            'neuroticism': neuroticism
        })
        
        return {
            'personality_type': personality_type,
            'big_five': {
                'openness': round(openness * 10, 1),
                'conscientiousness': round(conscientiousness * 10, 1),
                'extraversion': round(extraversion * 10, 1),
                'agreeableness': round(agreeableness * 10, 1),
                'neuroticism': round(neuroticism * 10, 1)
            }
        }
    
    def _calculate_openness(self):
        """Calculate openness score"""
        score = 0.5
        
        # Check hashtag diversity
        hashtags_used = PostHashtag.objects.filter(
            post__user=self.user
        ).values('hashtag__name').distinct().count()
        
        if hashtags_used > 20:
            score += 0.3
        elif hashtags_used > 10:
            score += 0.15
        
        # Check following count
        following_count = Follow.objects.filter(follower=self.user).count()
        if following_count > 100:
            score += 0.2
        elif following_count > 50:
            score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_conscientiousness(self):
        """Calculate conscientiousness score"""
        score = 0.5
        
        # Post regularity
        posts = Post.objects.filter(user=self.user)
        if posts.count() > 5:
            score += 0.2
        
        # Having a bio
        if self.profile and self.profile.bio:
            score += 0.15
        
        # Profile completion
        if self.profile and self.profile.full_name:
            score += 0.15
        
        return min(score, 1.0)
    
    def _calculate_extraversion(self):
        """Calculate extraversion score"""
        score = 0.5
        
        # Followers count
        followers = Follow.objects.filter(following=self.user).count()
        if followers > 100:
            score += 0.25
        elif followers > 30:
            score += 0.15
        
        # Stories count
        stories = Story.objects.filter(user=self.user).count()
        if stories > 20:
            score += 0.15
        elif stories > 5:
            score += 0.1
        
        # Messages sent
        messages = Message.objects.filter(sender=self.user).count()
        if messages > 100:
            score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_agreeableness(self):
        """Calculate agreeableness score"""
        score = 0.5
        
        # Likes given to others
        likes = Like.objects.filter(user=self.user).count()
        if likes > 200:
            score += 0.3
        elif likes > 50:
            score += 0.15
        
        return min(score, 1.0)
    
    def _calculate_neuroticism(self):
        """Calculate neuroticism score (lower is better)"""
        score = 0.3
        
        # Late night activity (anxiety indicator)
        late_posts = Post.objects.filter(
            user=self.user,
            created_at__hour__gte=23
        ).count()
        
        if late_posts > 10:
            score += 0.2
        
        return min(score, 1.0)
    
    def _determine_personality_type(self, traits):
        """Determine personality type from traits"""
        if traits['openness'] > 0.7 and traits['extraversion'] > 0.6:
            return "The Explorer"
        elif traits['openness'] > 0.7 and traits['conscientiousness'] > 0.6:
            return "The Creator"
        elif traits['extraversion'] > 0.7 and traits['agreeableness'] > 0.6:
            return "The Influencer"
        elif traits['conscientiousness'] > 0.7:
            return "The Professional"
        elif traits['openness'] > 0.6:
            return "The Thinker"
        elif traits['extraversion'] > 0.6:
            return "The Socialite"
        elif traits['agreeableness'] > 0.6:
            return "The Supporter"
        else:
            return "The Observer"
    
    def _analyze_interests(self):
        """Analyze user interests"""
        
        # Get top hashtags used
        hashtags_used = PostHashtag.objects.filter(
            post__user=self.user
        ).values('hashtag__name').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        
        # Get active hours
        posts = Post.objects.filter(user=self.user)
        hours = [p.created_at.hour for p in posts]
        hour_counts = Counter(hours)
        most_active = hour_counts.most_common(2) if hours else []
        
        return {
            'top_hashtags': [h['hashtag__name'] for h in hashtags_used],
            'active_hours': [f"{hour}:00" for hour, count in most_active],
            'content_categories': self._categorize_interests(hashtags_used)
        }
    
    def _categorize_interests(self, hashtags):
        """Categorize interests based on hashtags"""
        categories = {
            'Technology': ['tech', 'ai', 'coding', 'programming', 'python'],
            'Art': ['art', 'design', 'drawing', 'painting', 'photo'],
            'Sports': ['sport', 'gym', 'fitness', 'football', 'workout'],
            'Music': ['music', 'song', 'guitar', 'piano', 'concert'],
            'Food': ['food', 'cooking', 'recipe', 'restaurant', 'coffee'],
            'Travel': ['travel', 'trip', 'nature', 'adventure', 'beach']
        }
        
        detected = []
        for h in hashtags:
            tag = h['hashtag__name'].lower()
            for cat, keywords in categories.items():
                if any(kw in tag for kw in keywords):
                    if cat not in detected:
                        detected.append(cat)
        
        return detected[:3]
    
    def _analyze_behavior(self):
        """Analyze behavioral metrics"""
        
        posts = Post.objects.filter(user=self.user).count()
        comments = Comment.objects.filter(user=self.user).count()
        likes = Like.objects.filter(user=self.user).count()
        stories = Story.objects.filter(user=self.user).count()
        followers = Follow.objects.filter(following=self.user).count()
        following = Follow.objects.filter(follower=self.user).count()
        
        total_interactions = comments + likes
        engagement_rate = total_interactions / (posts + 1) if posts > 0 else 0
        
        return {
            'total_posts': posts,
            'total_comments': comments,
            'total_likes': likes,
            'total_stories': stories,
            'followers': followers,
            'following': following,
            'engagement_rate': round(engagement_rate, 2)
        }
    
    def _analyze_philosophy(self):
        """Analyze philosophical orientation"""
        
        bio = self.profile.bio if self.profile else ""
        
        philosophies = {
            'Stoic': ['life', 'control', 'peace', 'patience'],
            'Humanist': ['love', 'kindness', 'human', 'respect'],
            'Explorer': ['adventure', 'travel', 'new', 'experience'],
            'Creator': ['create', 'make', 'build', 'design']
        }
        
        detected = []
        bio_lower = bio.lower()
        
        for philosophy, keywords in philosophies.items():
            if any(kw in bio_lower for kw in keywords):
                detected.append(philosophy)
        
        return {
            'primary': detected[0] if detected else 'Undefined',
            'description': 'Based on bio analysis'
        }
    
    def _generate_recommendations(self):
        """Generate personalized recommendations"""
        
        behavior = self._analyze_behavior()
        
        recommendations = []
        
        if behavior['engagement_rate'] < 0.3:
            recommendations.append("Increase engagement with others")
        
        if behavior['total_posts'] < 5:
            recommendations.append("Post more regularly")
        
        if behavior['followers'] < 50:
            recommendations.append("Use relevant hashtags to reach more people")
        
        if not recommendations:
            recommendations.append("Continue your consistent engagement")
        
        return recommendations
    
    def _enhance_with_ai(self):
        """Enhance analysis with AI"""
        
        user_data = {
            'bio': self.profile.bio if self.profile else '',
            'sample_posts': self._get_sample_posts(),
            'top_hashtags': self._analyze_interests()['top_hashtags'][:5],
            'posts_count': self._analyze_behavior()['total_posts'],
            'followers_count': self._analyze_behavior()['followers']
        }
        
        result = self.ollama_client.analyze_personality_with_ai(user_data)
        
        if result['success']:
            try:
                return json.loads(result['response'])
            except:
                return {'raw_response': result['response']}
        else:
            return {'error': result.get('error')}
    
    def _get_sample_posts(self):
        """Get sample posts from user"""
        posts = Post.objects.filter(user=self.user)[:5]
        return ' '.join([p.content for p in posts if p.content])


# Helper function for quick analysis
def analyze_user(username=None, user_id=None, use_ai=False):
    """Quick analyze a user by username or ID"""
    
    if username:
        user = User.objects.filter(username=username).first()
    elif user_id:
        user = User.objects.filter(id=user_id).first()
    else:
        user = User.objects.first()
    
    if not user:
        return {"error": "User not found"}
    
    analyzer = PersonalityAnalyzer(user, use_ai=use_ai)
    return analyzer.analyze_complete_profile()