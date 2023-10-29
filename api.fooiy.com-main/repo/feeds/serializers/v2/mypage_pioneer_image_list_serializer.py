from rest_framework import serializers

from ...models import Pioneer

from common import index as Common


class MypagePioneerImageListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    is_confirm = serializers.SerializerMethodField()

    class Meta:
        model = Pioneer
        fields = (
            "id",
            "image",
            "is_confirm",
            "created_at",
        )

    def get_image(self, obj):
        if obj.state == Common.PioneerState.CONFIRM:
            return [obj.image_1.url]
        return []

    def get_is_confirm(self, obj):
        if obj.state == Common.PioneerState.CONFIRM:
            return True
        return False
