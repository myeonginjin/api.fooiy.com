from rest_framework import serializers

from archives.models import PushNotification
from archives.helpers import index as ArchivesHelpers


class PushNotificationSerializer(serializers.ModelSerializer):
    navigation = serializers.SerializerMethodField()
    navigation_id = serializers.SerializerMethodField()

    class Meta:
        model = PushNotification
        fields = (
            "id",
            "image",
            "title",
            "content",
            "created_at",
            "navigation",
            "navigation_id",
        )

    def get_navigation(self, obj):
        return ArchivesHelpers.push_navigation(obj.type)

    def get_navigation_id(self, obj):
        return ArchivesHelpers.push_navigation_id(obj)
