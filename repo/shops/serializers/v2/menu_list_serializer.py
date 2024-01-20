from rest_framework import serializers

from ...models import Menu


class MenuListSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = (
            ("id"),
            ("name"),
            ("price"),
            ("is_best"),
            ("is_popular"),
        )

    def get_price(self, obj):
        return f"{obj.price:,}"
