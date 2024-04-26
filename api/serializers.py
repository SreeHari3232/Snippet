from rest_framework import serializers
from .models import TextSnippet, Tag
from rest_framework.reverse import reverse
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username',]


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class BaseSnippetSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    class Meta:
        model = TextSnippet
        fields = ['title', 'tags']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', None)
        snippet = TextSnippet.objects.create(**validated_data)
        
        if tags_data:
            for tag_data in tags_data:
                tag_title = tag_data.get('name')
                tag = Tag.objects.filter(name=tag_title).first()
                if tag:
                    snippet.tags.add(tag)
                else:
                    new_tag = Tag.objects.create(name=tag_title)
                    snippet.tags.add(new_tag)
               
        return snippet
    
    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)

        instance.title = validated_data.get('title', instance.title)
        instance.save()

        if tags_data:
            instance.tags.clear()
            for tag_data in tags_data:
                tag_title = tag_data.get('name')
                tag = Tag.objects.filter(name=tag_title).first()
                if tag:
                    instance.tags.add(tag)
                else:
                    new_tag = Tag.objects.create(name=tag_title)
                    instance.tags.add(new_tag)

        return instance

    
class TextSnippetSerializer(BaseSnippetSerializer):

    url = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    user = UserSerializer()
    class Meta:
        model = TextSnippet
        fields = ['id', 'title', 'url', 'date', 'user', 'tags']

    def get_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("snippets-detail", kwargs={"pk":obj.pk}, request=request)
