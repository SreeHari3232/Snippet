from rest_framework import generics, viewsets
from rest_framework.response import Response
from .models import TextSnippet, Tag
from .serializers import TextSnippetSerializer, TagSerializer , BaseSnippetSerializer
from django.db.models import Count
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        
        data['username'] = self.user.username
        data['email'] = self.user.email
        return data
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

class CustomPagination(PageNumberPagination):
    page_size = 20

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'data': data
        })

class Snippets(viewsets.ModelViewSet):
    queryset = TextSnippet.objects.all()
    serializer_class = TextSnippetSerializer
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return BaseSnippetSerializer
        return TextSnippetSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

   

class Tags(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
