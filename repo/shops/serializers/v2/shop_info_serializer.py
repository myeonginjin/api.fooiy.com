from rest_framework import serializers

from ...models import Shop
from common import index as Common


class ShopInfoSerializer(serializers.ModelSerializer):
    shop_id = serializers.SerializerMethodField()
    fooiyti = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    short_address = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = (
            "shop_id",
            "name",
            "address",
            "short_address",
            "fooiyti",
            "category",
            "longitude",
            "latitude",
        )

    def get_shop_id(self, obj):
        return obj.public_id

    def get_fooiyti(self, obj):
        try:
            if (
                obj.shopfooiyti.feed_count < 1
                or obj.category.first().name == Common.global_variables.category_cafe
            ):
                return None
            result = []
            account_fooiyti = self.context["fooiyti"]
            for index, fooiyti in enumerate(obj.shopfooiyti.fooiyti.lower()):
                result.append(
                    {
                        "fooiyti": fooiyti,
                        "percentage": getattr(
                            obj.shopfooiyti, f"{fooiyti}_percentage", 50
                        ),
                        "different": False
                        if account_fooiyti[index] == fooiyti
                        else True,
                    }
                )
            return result
        except:
            return None

    def get_category(self, obj):
        try:
            return obj.category.first().name
        except:
            return

    def get_short_address(self, obj):
        try:
            return (
                obj.address_depth1 + " " + obj.address_depth2 + " " + obj.address_depth3
            )
        except:
            obj.longitude, obj.latitude = Common.convert_address_to_coordinate(
                obj.address
            )
            (
                obj.address_depth1,
                obj.address_depth2,
                obj.address_depth3,
            ) = Common.convert_coordinate_to_address(obj.longitude, obj.latitude)
            obj.save()
            return (
                obj.address_depth1 + " " + obj.address_depth2 + " " + obj.address_depth3
            )
