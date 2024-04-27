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
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = TextSnippet
        fields = ['title', 'tags']
        
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
