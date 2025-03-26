from rest_framework import serializers


class TestAWSPaapiSerializer(serializers.Serializer):
    asin = serializers.CharField(max_length=20)

    def validate_asin(self, value):
        if not value.isalnum():
            raise serializers.ValidationError("ASIN must be alphanumeric.")
        if len(value) > 20:
            raise serializers.ValidationError("ASIN must not exceed 20 characters.")
        return value
