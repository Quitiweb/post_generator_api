from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from aws.samples.sample_get_items_api import get_items
from aws.utils import get_product_title_and_description
from .serializers import TestAWSPaapiSerializer
import json


class TestAWSPaapiView(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    @action(methods=["get"], detail=False, url_path="test-paapi", serializer_class=TestAWSPaapiSerializer)
    def test_paapi(self, request):
        asin = request.query_params.get("asin", "B094D3JGLT")  # Default ASIN if not provided
        paapi_res = get_items([asin])

        if paapi_res is None:
            return Response(
                {
                    "ASIN": asin,
                    "Message": "The PAAPI returned None.",
                    "Status": "N/A",
                    "Errors": {"Message": "The PAAPI returned None."},
                    "RequestID": "N/A"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if len(paapi_res) > 1:
            exception = paapi_res[1]
            error_details = exception.body
            if isinstance(error_details, str):
                try:
                    error_details = json.loads(error_details)
                except json.JSONDecodeError:
                    error_details = {"Message": "Unable to parse error details"}

            return Response(
                {
                    "ASIN": asin,
                    "Message": "The PAAPI is not working.",
                    "Status": exception.status,
                    "Errors": error_details,
                    "RequestID": exception.headers.get("x-amzn-RequestId", "N/A")
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        else:
            title, description = get_product_title_and_description(asin)
            return Response({"title": title, "description": description}, status=status.HTTP_200_OK)
