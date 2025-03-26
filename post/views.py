from decouple import config
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .gpt import generate_aws_post_gpt, generate_post_gpt
from .models import Category, Post, Title
from .serializers import CategorySerializer, PostGeneratorSerializer, TitleSerializer

TEST = config("TEST", default=False, cast=bool)


class PostGeneratorView(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostGeneratorSerializer

    @action(methods=["get"], detail=False, url_path="generate", serializer_class=PostGeneratorSerializer)
    def generate(self, request, *args, **kwargs):
        if TEST:
            data_test = {"title": "Test Generate Title", "description": "Test Generate Description"}
            return Response(data_test, status=status.HTTP_200_OK)

        category = request.query_params.get("category")
        if category:
            tokens = 0
            title = Title.get_random_title_from_cat(category)
            if title:
                prefix = r"https://" if request.is_secure() else r"http://"
                domain = prefix + request.get_host()
                result, tokens = generate_post_gpt(
                    title=title,
                    tokens=tokens,
                    domain=domain,
                )
                print("Total tokens used: {}".format(tokens))
                print()

                return Response({"title": title.name, "description": result}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "there is not title for that category."}, status=status.HTTP_303_SEE_OTHER)

        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["get"], detail=False, url_path="aws", serializer_class=PostGeneratorSerializer)
    def aws(self, request, *args, **kwargs):
        """
        Gets a category and an ASIN (amazon product ID) to return a post title and a post description
        using the amazon product description from amazon (using PAAPI) with the help of Chat-GPT.

        :param request: HttpRequest object
        :param args: No args required
        :param kwargs: None
        :return: HttpResponse
        """
        amazon_id = request.query_params.get("asin")

        if TEST:
            data_test = {"title": f"Test AWS Title for {amazon_id}", "description": f"Test AWS Description for {amazon_id}"}
            return Response(data_test, status=status.HTTP_200_OK)

        if amazon_id:
            result, tokens, title_name = generate_aws_post_gpt(asin=amazon_id)
            return Response({"title": title_name, "description": result}, status=status.HTTP_200_OK)

        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class CategoryView(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleView(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
