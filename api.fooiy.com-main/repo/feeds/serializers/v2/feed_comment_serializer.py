from rest_framework import serializers

from ...models import FeedComment

from common import index as Common


class FeedCommentSerializer(serializers.ModelSerializer):
    comment_id = serializers.SerializerMethodField()
    account_id = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    fooiyti = serializers.SerializerMethodField()
    is_reply = serializers.SerializerMethodField()

    class Meta:
        model = FeedComment
        fields = (
            "comment_id",
            "account_id",
            "profile_image",
            "rank",
            "nickname",
            "fooiyti",
            "content",
            "is_reply",
            "created_at",
        )

    def get_comment_id(self, obj):
        return obj.id

    def get_account_id(self, obj):
        try:
            return obj.writer.public_id
        except:
            return None

    def get_rank(self, obj):
        try:
            return obj.writer.rank
        except:
            return ""

    def get_nickname(self, obj):
        if obj.writer.nickname:
            return obj.writer.nickname
        return Common.global_variables.withdrawn_member_nickname

    def get_fooiyti(self, obj):
        try:
            return obj.writer.fooiyti.fooiyti
        except:
            return

    def get_profile_image(self, obj):
        try:
            return obj.writer.profile_image.url
        except:
            return None

    def get_is_reply(self, obj):
        return True if obj.parent else False
