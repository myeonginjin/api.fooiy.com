from rest_framework import serializers

from ...models import AddressCluster


class AddressClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressCluster
        fields = (
            "id",
            "name",
            "longitude",
            "latitude",
            "count",
        )
