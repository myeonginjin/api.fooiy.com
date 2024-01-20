from rest_framework import serializers
from ...models import Account


class AccountListSerializer(serializers.ModelSerializer):
    fooiyti = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = (
            "public_id",
            "count",
            "nickname",
            "fooiyti",
            "profile_image",
            "rank",
        )

    def get_fooiyti(self, obj):
        try:
            return obj.fooiyti.fooiyti
        except Exception as e:
            return None

    def get_profile_image(self, obj):
        return obj.profile_image.url

    def get_count(self, obj):
        try:
            return obj.count
        except:
            return obj.feed.count()
