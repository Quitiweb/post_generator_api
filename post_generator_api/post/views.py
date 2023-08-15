from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .gpt import generate_post_gpt, generate_title_gpt
from .models import Post
from .serializers import PostGeneratorSerializer


class PostGeneratorView(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostGeneratorSerializer

    @action(methods=["get"], detail=False, url_path="generate", serializer_class=PostGeneratorSerializer)
    def generate(self, request, *args, **kwargs):
        category = request.query_params.get("category")
        if category:
            title, tokens = generate_title_gpt(category, 0)
            result, tokens = generate_post_gpt(title, tokens)

            print("Total tokens used: {}".format(tokens))
            print()

            return Response({"title": title, "description": result}, status=status.HTTP_200_OK)

        return Response({}, status=status.HTTP_400_BAD_REQUEST)
