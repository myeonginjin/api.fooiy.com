from rest_framework import serializers

from ...models import Feed

from common import index as Common


class FeedListSerializer(serializers.ModelSerializer):
    account_id = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
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
    is_liked = serializers.SerializerMethodField()
    count_liked = serializers.SerializerMethodField()
    count_comment = serializers.SerializerMethodField()
    fooiyti_e = serializers.SerializerMethodField()
    fooiyti_i = serializers.SerializerMethodField()
    fooiyti_s = serializers.SerializerMethodField()
    fooiyti_n = serializers.SerializerMethodField()
    fooiyti_t = serializers.SerializerMethodField()
    fooiyti_f = serializers.SerializerMethodField()
    fooiyti_a = serializers.SerializerMethodField()
    fooiyti_c = serializers.SerializerMethodField()
    is_cafe = serializers.SerializerMethodField()

    class Meta:
        model = Feed
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
            "description",
            "created_at",
            "is_store",
            "is_liked",
            "count_liked",
            "longitude",
            "latitude",
            "count_comment",
            "fooiyti_e",
            "fooiyti_i",
            "fooiyti_s",
            "fooiyti_n",
            "fooiyti_t",
            "fooiyti_f",
            "fooiyti_a",
            "fooiyti_c",
            "is_cafe",
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
        return obj.account.fooiyti

    def get_profile_image(self, obj):
        return obj.account.profile_image.url

    def get_is_confirm(self, obj):
        return False

    def get_taste_evaluation(self, obj):
        return obj.taste_evaluation

    def get_shop_id(self, obj):
        try:
            return obj.shop.public_id
        except:
            return ""

    def get_shop_name(self, obj):
        try:
            return obj.shop.name
        except:
            return "삭제된 매장입니다"

    def get_shop_address(self, obj):
        try:
            return obj.shop.address
        except:
            return ""

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
            return [image.image.url for image in obj.to_image]
        except:
            return []

    def get_is_store(self, obj):
        try:
            return (
                obj.storage.filter(account=self.context["account"])[0].state
                == Common.FeedState.SUBSCRIBE
            )
        except:
            return False

    def get_is_liked(self, obj):
        try:
            return (
                obj.like.filter(account=self.context["account"])[0].state
                == Common.FeedState.SUBSCRIBE
            )
        except:
            return False

    def get_count_liked(self, obj):
        return obj.like.filter(state=Common.FeedState.SUBSCRIBE).count()

    def get_count_comment(self, obj):
        return obj.feed_comment.count()

    def get_fooiyti_e(self, obj):
        try:
            return obj.feedfooiyti.fooiyti_e
        except:
            return 50

    def get_fooiyti_i(self, obj):
        try:
            return obj.feedfooiyti.fooiyti_i
        except:
            return 50

    def get_fooiyti_s(self, obj):
        try:
            return obj.feedfooiyti.fooiyti_s
        except:
            return 50

    def get_fooiyti_n(self, obj):
        try:
            return obj.feedfooiyti.fooiyti_n
        except:
            return 50

    def get_fooiyti_t(self, obj):
        try:
            return obj.feedfooiyti.fooiyti_t
        except:
            return 50

    def get_fooiyti_f(self, obj):
        try:
            return obj.feedfooiyti.fooiyti_f
        except:
            return 50

    def get_fooiyti_a(self, obj):
        try:
            return obj.feedfooiyti.fooiyti_a
        except:
            return 50

    def get_fooiyti_c(self, obj):
        try:
            return obj.feedfooiyti.fooiyti_c
        except:
            return 50

    def get_is_cafe(self, obj):
        try:
            return (
                obj.shop.category.first().name == Common.global_variables.category_cafe
            )
        except:
            return False
