from rest_framework import serializers


class RecipeLikeSerializer(serializers.Serializer):
    user = serializers.CharField(max_length=100, required=False)
    recipe = serializers.CharField(max_length=100, required=False)
