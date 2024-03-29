from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .gpt import generate_post_gpt
from .models import Category, Post, Title
from .serializers import CategorySerializer, PostGeneratorSerializer, TitleSerializer


class PostGeneratorView(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
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
        category_name = request.query_params.get("category")
        amazon_id = request.query_params.get("asin")

        if category_name and amazon_id:
            try:
                category = Category.objects.get(name=category_name)
            except Category.DoesNotExist:
                return Response(
                    {"error": "there is not category with that name."}, status=status.HTTP_303_SEE_OTHER)

            title = Title(category=category)
            result, tokens = generate_post_gpt(
                title=title,
                asin=amazon_id,
            )
            return Response({"title": title.name, "description": result}, status=status.HTTP_200_OK)

        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class CategoryView(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleView(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
