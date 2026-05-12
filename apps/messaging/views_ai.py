"""
AI-powered views for messaging app
"""

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView

from .serializers import (
    TargetAnalysisSerializer,
    OpeningMessageSuggestionsSerializer,
    ReplySuggestionSerializer,
    IceBreakerTopicsSerializer,
    StartConversationSerializer
)
from apps.blocks.views import BlockedUsersMixin
from .ai_client import OllamaClient  

import json
import re

User = get_user_model()


class TargetAnalysisView(GenericAPIView, BlockedUsersMixin):
    """Get personality analysis for a target user using AI"""
    permission_classes = [IsAuthenticated]
    serializer_class = TargetAnalysisSerializer
    
    def get(self, request, user_id):
        serializer = self.get_serializer(data={'user_id': user_id})
        serializer.is_valid(raise_exception=True)
        
        target = get_object_or_404(User, id=user_id)
        
        blocked_ids = self.get_mutually_blocked_ids(request.user)
        if target.id in blocked_ids:
            return Response({
                "success": False,
                "error": "این کاربر را بلاک کرده‌اید"
            }, status=status.HTTP_403_FORBIDDEN)
        
        ollama = OllamaClient()
        analysis_data = None
        source = "fallback"
        
        if ollama.is_available():
            try:
                #get the data from the Database 
                from apps.posts.models import Post
                from apps.hashtags.models import PostHashtag
                
                posts = Post.objects.filter(user=target, is_deleted=False)
                hashtags = PostHashtag.objects.filter(
                    post__user=target
                ).values_list('hashtag__name', flat=True).distinct()[:5]
                
                bio = ""
                if hasattr(target, 'profile') and target.profile:
                    bio = target.profile.bio or ""
                
                prompt = f"""
                تحلیل شخصیت کاربر بر اساس اطلاعات زیر:
                - نام کاربری: {target.username}
                - بیوگرافی: {bio}
                - تعداد پست: {posts.count()}
                - تعداد فالوور: {target.followers.count() if hasattr(target, 'followers') else 0}
                - هشتگ‌های پرکاربرد: {list(hashtags)}
                
                خروجی JSON:
                {{
                    "personality_type": "نوع شخصیت",
                    "interests": ["علاقه1", "علاقه2", "علاقه3"],
                    "communication_style": "سبک ارتباطی",
                    "icebreakers": ["موضوع1", "موضوع2"],
                    "topics_to_avoid": ["موضوع1"],
                    "best_time_to_message": "زمان",
                    "tips": ["نکته1", "نکته2"]
                }}
                """
                
                result = ollama.generate(prompt, temperature=0.7, max_tokens=500)
                if result.get('success'):
                    text = result.get('response', '')
                    match = re.search(r'\{.*\}', text, re.DOTALL)
                    if match:
                        analysis_data = json.loads(match.group())
                        source = "ollama"
            except Exception as e:
                pass  
        
        if not analysis_data:
            analysis_data = {
                "personality_type": "دوستانه و صمیمی",
                "interests": ["هنر", "موسیقی", "سفر"],
                "communication_style": "صمیمی",
                "icebreakers": ["سلام! چطوری؟", "چه خبر؟"],
                "topics_to_avoid": ["سیاست"],
                "best_time_to_message": "عصرها",
                "tips": ["با احترام صحبت کن", "بهش فرصت بده"]
            }
        
        return Response({
            "success": True,
            "data": {
                "target_username": target.username,
                "analysis": analysis_data,
                "source": source 
            }
        })


class OpeningMessageSuggestionsView(GenericAPIView, BlockedUsersMixin):
    """Get AI-powered opening message suggestions"""
    permission_classes = [IsAuthenticated]
    serializer_class = OpeningMessageSuggestionsSerializer
    
    def get(self, request, user_id):
        count = request.query_params.get('count', 3)
        serializer = self.get_serializer(data={
            'user_id': user_id,
            'count': count
        })
        serializer.is_valid(raise_exception=True)
        
        target = get_object_or_404(User, id=user_id)
        validated_count = int(serializer.validated_data['count'])
        
        blocked_ids = self.get_mutually_blocked_ids(request.user)
        if target.id in blocked_ids:
            return Response({
                "success": False,
                "error": "این کاربر را بلاک کرده‌اید"
            }, status=status.HTTP_403_FORBIDDEN)
        
        ollama = OllamaClient()
        suggestions = None
        source = "fallback"
        
        if ollama.is_available():
            try:
                prompt = f"""
                {validated_count} پیام کوتاه و صمیمی برای شروع مکالمه با کاربری به نام {target.username} پیشنهاد بده.
                فقط لیست JSON برگردان. مثال: ["پیام1", "پیام2", "پیام3"]
                پیام‌ها باید دوستانه و طبیعی باشند.
                """
                
                result = ollama.generate(prompt, temperature=0.8, max_tokens=200)
                if result.get('success'):
                    text = result.get('response', '')
                    match = re.search(r'\[.*\]', text, re.DOTALL)
                    if match:
                        suggestions = json.loads(match.group())[:validated_count]
                        source = "ollama"
            except Exception as e:
                pass
        
        if not suggestions:
            suggestions = [
                f"سلام {target.username}! چطوری؟",
                f"{target.username} جان! چه خبر؟",
                "سلام! امیدوارم روز خوبی داشته باشی"
            ][:validated_count]
        
        return Response({
            "success": True,
            "data": {
                "target": target.username,
                "suggestions": suggestions,
                "source": source
            }
        })