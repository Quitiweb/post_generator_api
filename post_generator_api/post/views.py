from rest_framework.viewsets import ModelViewSet

from .serializers import PostGeneratorSerializer


class PostGeneratorView(ModelViewSet):
    serializer_class = PostGeneratorSerializer
