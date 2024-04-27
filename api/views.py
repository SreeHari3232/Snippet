from rest_framework import generics, viewsets
from rest_framework.response import Response
from .models import TextSnippet, Tag
from .serializers import TextSnippetSerializer, TagSerializer , BaseSnippetSerializer
from django.db.models import Count
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


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
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        tags_data = request.data.get('tags', None)
        serializer = BaseSnippetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        snippet = serializer.instance
        if tags_data:
            for tag_data in tags_data:
                tag_title = tag_data.get('name')
                tag, created = Tag.objects.get_or_create(name=tag_title)
                if created:
                    tag.save()
                snippet.tags.add(tag)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        tags_data = request.data.get('tags', None)
        serializer = BaseSnippetSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        snippet = serializer.instance
        if tags_data:
            snippet.tags.clear()
            
            for tag_data in tags_data:
                tag_title = tag_data.get('name')
                tag, created = Tag.objects.get_or_create(name=tag_title)
                if created:
                    tag.save()
                snippet.tags.add(tag)

        return Response(serializer.data)

class Tags(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]


    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()
        snippets = instance.textsnippet_set.all()
        serializer = TextSnippetSerializer(snippets, many=True)
        snippet_titles = [snippet['title'] for snippet in serializer.data]
        serialized_data = {
            "id": instance.id,
            "name": instance.name,
            "title": snippet_titles
        }
        return Response(serialized_data)
