from rest_framework import serializers

from ...models import Notice


class NoticeSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Notice
        fields = (
            "id",
            "image",
        )

    def get_image(self, obj):
        try:
            return obj.image.first().image.url
        except Exception:
            return ""
