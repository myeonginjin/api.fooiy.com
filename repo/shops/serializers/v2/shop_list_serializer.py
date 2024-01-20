from rest_framework import serializers

from ...models import Shop


class ShopListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = (
            ("public_id"),
            ("name"),
            ("address"),
        )
