from rest_framework import serializers
from feeds.models import Feed


from common import index as Common


class LatestShopListSerializer(serializers.ModelSerializer):
    shop_id = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Feed
        fields = (
            "shop_id",
            "image",
        )

    def get_shop_id(self, obj):
        try:
            return obj.shop.public_id
        except:
            return ""

    def get_image(self, obj):
        try:
            return obj.to_image[0].image.url
        except:
            return None
