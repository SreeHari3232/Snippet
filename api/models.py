from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):

    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

class TextSnippet(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    title = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
