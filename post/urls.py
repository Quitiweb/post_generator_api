from rest_framework import routers

from .views import PostGeneratorView, CategoryView, TitleView

app_name = "post"

router = routers.DefaultRouter()
router.register("", PostGeneratorView, basename="post_generator")
router.register("categories", CategoryView, basename="categories")
router.register("titles", TitleView, basename="titles")

urlpatterns = router.urls
