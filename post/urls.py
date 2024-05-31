from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view
from .views import PostGeneratorView, CategoryView, TitleView, api_root

schema_view = get_schema_view(title='Pastebin API')

app_name = "post"

router = routers.DefaultRouter()
router.register("", PostGeneratorView, basename="post_generator")
router.register("categories", CategoryView, basename="categories")
router.register("titles", TitleView, basename="titles")

#urlpatterns = router.urls

urlpatterns = [
    path('schema/', schema_view, name='schema'),
    path('post/', include(router.urls)),
    path('', api_root),
]
