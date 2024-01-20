from rest_framework import serializers

from ...models import SearchSpot


class SpotSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchSpot
        fields = (
            "id",
            "type",
            "name",
            "address",
            "longitude",
            "latitude",
        )
