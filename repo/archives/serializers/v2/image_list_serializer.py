from rest_framework import serializers

from ...models import Image


class ImageListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ("image",)

    def get_image(self, obj):
        return obj.image.url
