from rest_framework import routers

from .views import TestAWSPaapiView

app_name = "aws"

router = routers.DefaultRouter()
router.register("", TestAWSPaapiView, basename="test-paapi")

urlpatterns = router.urls
