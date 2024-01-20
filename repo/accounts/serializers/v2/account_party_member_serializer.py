from rest_framework import serializers

from ...models import AccountParty
from common import index as Common


class AccountPartyMemberSerializer(serializers.ModelSerializer):
    account_id = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    feed_count = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    fooiyti = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()

    class Meta:
        model = AccountParty
        fields = (
            "account_id",
            "is_owner",
            "nickname",
            "feed_count",
            "profile_image",
            "fooiyti",
            "rank",
        )

    def get_account_id(self, obj):
        return obj.account.public_id

    def get_is_owner(self, obj):
        return obj.party.owner == obj.account

    def get_nickname(self, obj):
        return obj.account.nickname

    def get_feed_count(self, obj):
        return obj.account.feed.count()

    def get_profile_image(self, obj):
        try:
            return obj.account.profile_image.url
        except:
            return None

    def get_fooiyti(self, obj):
        try:
            return obj.account.fooiyti.fooiyti
        except:
            return

    def get_rank(self, obj):
        return obj.account.rank
