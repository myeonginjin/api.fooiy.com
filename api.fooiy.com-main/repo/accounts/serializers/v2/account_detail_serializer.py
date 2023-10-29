from rest_framework import serializers
from ...models import Account


class AccountDetailSerializer(serializers.ModelSerializer):
    fooiyti = serializers.SerializerMethodField()
    fooiyti_nickname = serializers.SerializerMethodField()
    fooiyti_description = serializers.SerializerMethodField()
    fooiyti_result_image = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    feed_count = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = (
            "public_id",
            "rank",
            "phone_number",
            "email",
            "nickname",
            "introduction",
            "gender",
            "birth_year",
            "fooiyti",
            "fooiyti_nickname",
            "fooiyti_description",
            "fooiyti_result_image",
            "fooiyti_e_percentage",
            "fooiyti_i_percentage",
            "fooiyti_n_percentage",
            "fooiyti_s_percentage",
            "fooiyti_t_percentage",
            "fooiyti_f_percentage",
            "fooiyti_c_percentage",
            "fooiyti_a_percentage",
            "account_token",
            "state",
            "profile_image",
            "is_mkt_agree",
            "feed_count",
        )

    def get_fooiyti(self, obj):
        try:
            return obj.fooiyti.fooiyti
        except:
            return None

    def get_fooiyti_nickname(self, obj):
        try:
            return obj.fooiyti.nickname
        except:
            return None

    def get_fooiyti_description(self, obj):
        try:
            return obj.fooiyti.description
        except:
            return None

    def get_fooiyti_result_image(self, obj):
        try:
            return obj.fooiyti.image.last().image.url
        except:
            return None

    def get_profile_image(self, obj):
        return obj.profile_image.url

    def get_feed_count(self, obj):
        return obj.feed.count()
