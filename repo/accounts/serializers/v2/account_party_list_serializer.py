from rest_framework import serializers

from accounts.models import AccountParty
from feeds.models import FeedParty
from common import index as Common


class AccountPartyListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    owner_id = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    feed_count = serializers.SerializerMethodField()
    account_count = serializers.SerializerMethodField()
    is_subscribe = serializers.SerializerMethodField()

    class Meta:
        model = AccountParty
        fields = (
            "party_id",
            "name",
            "owner",
            "owner_id",
            "image",
            "feed_count",
            "account_count",
            "is_subscribe",
        )

    def get_name(self, obj):
        return obj.party.name

    def get_owner(self, obj):
        return obj.party.owner.nickname

    def get_owner_id(self, obj):
        return obj.party.owner.public_id

    def get_image(self, obj):
        try:
            return obj.party.party_image.url
        except:
            return None

    def get_feed_count(self, obj):
        return obj.party.feed_count

    def get_account_count(self, obj):
        return obj.party.account_count

    def get_is_subscribe(self, obj):
        if self.context["feed"]:
            return FeedParty.objects.filter(
                party=obj.party, feed=self.context["feed"]
            ).exists()
        else:
            return False
