from rest_framework import serializers

from ...models import Feed

from common import index as Common


class FeedStorageSerializer(serializers.ModelSerializer):
    feed_id = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    shop_name = serializers.SerializerMethodField()
    menu_name = serializers.SerializerMethodField()
    menu_price = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Feed
        fields = (
            "feed_id",
            "profile_image",
            "nickname",
            "image",
            "fooiyti",
            "shop_name",
            "menu_name",
            "menu_price",
        )

    def get_feed_id(self, obj):
        return obj.id

    def get_nickname(self, obj):
        if obj.account.nickname:
            return obj.account.nickname
        return Common.global_variables.withdrawn_member_nickname

    def get_profile_image(self, obj):
        return obj.account.profile_image.url

    def get_fooiyti(self, obj):
        return obj.account.fooiyti

    def get_shop_name(self, obj):
        try:
            return obj.shop.name
        except:
            return "삭제된 매장입니다"

    def get_menu_name(self, obj):
        try:
            return obj.menu.name
        except:
            return ""

    def get_menu_price(self, obj):
        try:
            return f"{obj.menu.price:,}원"
        except:
            return ""

    def get_image(self, obj):
        try:
            return [obj.image.order_by("order").first().image.url]
        except:
            return []
