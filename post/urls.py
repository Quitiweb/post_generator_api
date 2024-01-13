from rest_framework import routers

from .views import PostGeneratorView

app_name = "post"

router = routers.DefaultRouter()
router.register("", PostGeneratorView, basename="post_generator")

urlpatterns = router.urls
