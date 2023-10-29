from rest_framework import serializers

from accounts.models import Party
from common import index as Common


class PartyInfoSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    owner_id = serializers.SerializerMethodField()
    owner_rank = serializers.SerializerMethodField()
    owner_fooiyti = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    join_state = serializers.SerializerMethodField()
    waiting_join_count = serializers.SerializerMethodField()

    class Meta:
        model = Party
        fields = (
            "name",
            "owner",
            "owner_id",
            "owner_rank",
            "owner_fooiyti",
            "image",
            "feed_count",
            "account_count",
            "introduction",
            "join_state",
            "waiting_join_count",
        )

    def get_name(self, obj):
        return obj.name

    def get_owner(self, obj):
        return obj.owner.nickname

    def get_owner_id(self, obj):
        return obj.owner.public_id

    def get_owner_rank(self, obj):
        return obj.owner.rank

    def get_owner_fooiyti(self, obj):
        return obj.owner.fooiyti.fooiyti

    def get_image(self, obj):
        try:
            return obj.party_image.url
        except:
            return None

    def get_join_state(self, obj):
        try:
            return obj.account_party.filter(account=self.context["account"])[0].state
        except:
            return Common.PartyState.UNSUBSCRIBE

    def get_waiting_join_count(self, obj):
        return obj.account_party.filter(state=Common.PartyState.CONFIRM).count()
