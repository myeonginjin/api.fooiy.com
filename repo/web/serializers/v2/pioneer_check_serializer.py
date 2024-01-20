from rest_framework import serializers

from feeds.models import Pioneer
from common import index as Common
from web.helpers import index as WebHelpers


class PioneerCheckSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    is_pioneered_shop = serializers.SerializerMethodField()
    shop_id = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Pioneer
        fields = (
            "id",
            "taste_evaluation",
            "shop_name",
            "address",
            "menu_name",
            "comment",
            "image",
            "is_pioneered_shop",
            "shop_id",
            "category",
        )

    def get_address(self, obj):
        return obj.address

    def get_image(self, obj):
        image = []

        if obj.image_1:
            image.append(obj.image_1.url)

        return image

    def get_is_pioneered_shop(self, obj):
        if obj.shop:
            return True
        else:
            return False

    def get_shop_id(self, obj):
        if obj.shop:
            return obj.shop.public_id
        else:
            return None

    def get_category(self, obj):
        if obj.shop_name:
            return WebHelpers.check_shop_category(obj.shop_name, obj.menu_name)
