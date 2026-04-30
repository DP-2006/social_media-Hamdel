from django.shortcuts import render

# Create your views here.
# apps/follows/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Follow
from .serializers import FollowSerializer
from core.pagination import StandardPagination  


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination 

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user).select_related('following')
0222
    @action(detail=False, methods=['get'] , methods = ['Post'])
    def following(self, request):
        following = Follow.objects.filter(follower=request.user).select_related('following')
        page = self.paginate_queryset(following)    
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(following, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)