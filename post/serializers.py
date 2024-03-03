from rest_framework import serializers

from .models import Category, Post, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id", "name", "section",
        ]


class PostGeneratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id", "title", "description", "featured", "img1", "img2", "img3",
        ]


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = [
            "id", "name", "description", "category", "gpt_prompt", "used",
        ]
