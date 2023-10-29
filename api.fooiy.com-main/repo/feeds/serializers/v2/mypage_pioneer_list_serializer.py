from rest_framework import serializers

from ...models import Pioneer

from common import index as Common


class MypagePioneerListSerializer(serializers.ModelSerializer):
    account_id = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    is_confirm = serializers.SerializerMethodField()
    shop_id = serializers.SerializerMethodField()
    shop_name = serializers.SerializerMethodField()
    shop_address = serializers.SerializerMethodField()
    menu_name = serializers.SerializerMethodField()
    menu_price = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    taste_evaluation = serializers.SerializerMethodField()
    is_store = serializers.SerializerMethodField()

    class Meta:
        model = Pioneer
        fields = (
            "id",
            "account_id",
            "rank",
            "shop_id",
            "is_confirm",
            "profile_image",
            "nickname",
            "image",
            "fooiyti",
            "taste_evaluation",
            "shop_name",
            "shop_address",
            "menu_name",
            "menu_price",
            "comment",
            "created_at",
            "is_store",
        )

    def get_rank(self, obj):
        try:
            return obj.account.rank
        except:
            return ""

    def get_account_id(self, obj):
        try:
            return obj.account.public_id
        except:
            return None

    def get_nickname(self, obj):
        if obj.account.nickname:
            return obj.account.nickname
        return Common.global_variables.withdrawn_member_nickname

    def get_fooiyti(self, obj):
        if obj.state != Common.PioneerState.CONFIRM:
            return obj.fooiyti
        return obj.account.fooiyti

    def get_profile_image(self, obj):
        return obj.account.profile_image.url

    def get_is_confirm(self, obj):
        if obj.state == Common.PioneerState.CONFIRM:
            return True
        return False

    def get_taste_evaluation(self, obj):
        return obj.taste_evaluation

    def get_shop_id(self, obj):
        try:
            return obj.shop.public_id
        except Exception:
            return ""

    def get_shop_name(self, obj):
        try:
            return obj.shop.name
        except Exception:
            if obj.state == Common.PioneerState.CONFIRM:
                return obj.shop_name
            return "삭제된 매장입니다"

    def get_shop_address(self, obj):
        try:
            return obj.shop.address
        except Exception:
            return ""

    def get_menu_name(self, obj):
        try:
            return obj.menu.name
        except Exception:
            if obj.state == Common.PioneerState.CONFIRM:
                return obj.menu_name
            return ""

    def get_menu_price(self, obj):
        try:
            return f"{obj.menu.price:,}원"
        except Exception:
            if obj.state == Common.PioneerState.CONFIRM:
                return f"{obj.menu_price:,}원"
            return

    def get_image(self, obj):
        if obj.state == Common.PioneerState.CONFIRM:
            return [obj.image_1.url]
        return [image.url for image in obj.image_1]

    def get_is_store(self, obj):
        return False
