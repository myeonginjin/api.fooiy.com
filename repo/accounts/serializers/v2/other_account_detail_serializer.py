from rest_framework import serializers

from ...models import Account


class OtherAccountDetailSerializer(serializers.ModelSerializer):
    fooiyti = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    feed_count = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = (
            "public_id",
            "rank",
            "nickname",
            "introduction",
            "fooiyti",
            "profile_image",
            "feed_count",
        )

    def get_fooiyti(self, obj):
        try:
            return obj.fooiyti.fooiyti
        except Exception as e:
            return None

    def get_profile_image(self, obj):
        try:
            return obj.profile_image.url
        except:
            return None

    def get_feed_count(self, obj):
        try:
            return obj.feed.count()
        except:
            return 0
