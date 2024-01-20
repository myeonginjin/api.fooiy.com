from rest_framework import serializers

from shops.models import Shop
from common import index as Common
from shops.helpers import index as ShopsHelpers


class NearbyShopListSerializer(serializers.ModelSerializer):
    shop_id = serializers.SerializerMethodField()
    shop_name = serializers.SerializerMethodField()
    menu_price = serializers.SerializerMethodField()
    shop_category_list = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = (
            "shop_id",
            "shop_name",
            "menu_price",
            "shop_category_list",
            "score",
            "thumbnail",
            "distance",
        )

    def get_shop_id(self, obj):
        return obj.public_id

    def get_shop_name(self, obj):
        try:
            return obj.name
        except:
            return "삭제된 매장입니다"

    def get_menu_price(self, obj):
        if obj.menu_max_price:
            return f"{obj.menu_min_price:,}원~{obj.menu_max_price:,}원"
        else:
            return f"{obj.menu_min_price:,}원"

    def get_shop_category_list(self, obj):
        return [
            Common.global_variables.shop_category_dict[category.name]
            for category in obj.category.all()
        ]

    def get_score(self, obj):
        return obj.score

    def get_thumbnail(self, obj):
        try:
            return obj.thumbnail.url
        except:
            return None

    def get_distance(self, obj):
        try:
            accout_spot = self.context["account_spot"]
            distance = ShopsHelpers.get_distance(
                obj.latitude, obj.longitude, accout_spot
            )

            return distance

        except:
            return ""
