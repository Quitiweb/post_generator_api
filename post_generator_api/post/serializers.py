from rest_framework import serializers

from .models import Post


class PostGeneratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "description", ]
