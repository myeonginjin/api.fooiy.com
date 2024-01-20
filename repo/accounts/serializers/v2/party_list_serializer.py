from rest_framework import serializers

from accounts.models import Party
from common import index as Common


class PartyListSerializer(serializers.ModelSerializer):
    party_id = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    owner_id = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Party
        fields = (
            "party_id",
            "name",
            "owner",
            "owner_id",
            "image",
            "feed_count",
            "account_count",
        )

    def get_party_id(self, obj):
        return obj.id

    def get_owner(self, obj):
        return obj.owner.nickname

    def get_owner_id(self, obj):
        return obj.owner.public_id

    def get_image(self, obj):
        try:
            return obj.party_image.url
        except:
            return None
