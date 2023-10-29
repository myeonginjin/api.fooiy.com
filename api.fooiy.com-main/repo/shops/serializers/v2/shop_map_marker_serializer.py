from rest_framework import serializers

from ...models import Shop


class ShopMapMarkerSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = (
            "id",
            "longitude",
            "latitude",
        )

    def get_id(self, obj):
        return obj.public_id
