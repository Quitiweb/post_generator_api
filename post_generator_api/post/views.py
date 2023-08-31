from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .gpt import generate_post_gpt
from .models import Post, Title
from .serializers import PostGeneratorSerializer


class PostGeneratorView(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostGeneratorSerializer

    @action(methods=["get"], detail=False, url_path="generate", serializer_class=PostGeneratorSerializer)
    def generate(self, request, *args, **kwargs):
        category = request.query_params.get("category")
        if category:
            tokens = 0
            title = Title.get_random_title_from_cat(category)
            if title:
                prefix = r"https://" if request.is_secure() else r"http://"
                domain = prefix + request.get_host()
                result, tokens = generate_post_gpt(title, tokens, domain)
                print("Total tokens used: {}".format(tokens))
                print()

                return Response({"title": title.name, "description": result}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "there is not title for that category."}, status=status.HTTP_303_SEE_OTHER)

        return Response({}, status=status.HTTP_400_BAD_REQUEST)
