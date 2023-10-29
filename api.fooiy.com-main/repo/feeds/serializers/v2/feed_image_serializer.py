from rest_framework import serializers

from ...models import Feed
from common import index as Common


class FeedImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    is_confirm = serializers.SerializerMethodField()

    class Meta:
        model = Feed
        fields = (
            "id",
            "image",
            "is_confirm",
            "created_at",
        )

    def get_image(self, obj):
        try:
            return [obj.to_image[0].image.url]
        except:
            return []

    def get_is_confirm(self, obj):
        return False
