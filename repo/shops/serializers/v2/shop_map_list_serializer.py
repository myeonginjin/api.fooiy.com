from rest_framework import serializers

from ...models import Shop
from common import index as Common


class ShopMapListSerializer(serializers.ModelSerializer):
    shop_category_list = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    menu_price = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = (
            "public_id",
            "address",
            "name",
            "shop_category_list",
            "score",
            "thumbnail",
            "menu_price",
        )

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

    def get_menu_price(self, obj):
        if obj.menu_max_price:
            return f"{obj.menu_min_price:,}원~{obj.menu_max_price:,}원"
        else:
            return f"{obj.menu_min_price:,}원"
