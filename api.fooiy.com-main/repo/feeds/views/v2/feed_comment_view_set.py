from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action


from accounts.helpers import index as AccountsHelpers
from feeds.helpers import index as FeedsHelpers
from archives.helpers import index as ArchivesHelpers
from feeds.models import FeedComment
from feeds.serializers.v2 import index as FeedsSerializerV2
from common import index as Common

import logging

logger = logging.getLogger("api")


class FeedCommentPagination(Common.FooiyPagenation):
    default_limit = 20


class FeedCommentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    http_method_names = ["get", "post", "patch", "delete"]
    pagination_class = FeedCommentPagination

    default_order_gap = 1000
    nested_comment_order_gap = 1

    queryset = FeedComment.objects.all()

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @method_decorator(FeedsHelpers.get_feed_from_request())
    def list(self, request):
        """
        # 피드 댓글 리스트 API
        """
        feed = request.feed
        payload = {}
        try:
            comments = (
                FeedComment.objects.select_related("writer")
                .filter(feed=feed)
                .order_by("order")
            )
            pagenate_comments = self.paginate_queryset(comments)
            pagenate_comments = FeedsSerializerV2.FeedCommentSerializer(
                pagenate_comments, many=True
            ).data
            payload["comment_list"] = self.get_paginated_response(pagenate_comments)

            return Response(
                Common.fooiy_standard_response(True, payload),
            )

        except Exception as e:
            return Response(
                Common.fooiy_standard_response(
                    False, 5057, account=request.account, feed=request.feed, error=e
                )
            )

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @method_decorator(FeedsHelpers.get_feed_from_request())
    @method_decorator(FeedsHelpers.get_feed_comment_from_request(require=False))
    def create(self, request):
        """
        # 피드 댓글 등록 API
        """
        feed = request.feed
        comment = request.comment
        account = request.account
        sender = account
        state = Common.CommentState.PARENT_COMMENT
        content = request.data.get("content", None)
        order = self.default_order_gap

        try:
            if not content:
                return Response(
                    Common.fooiy_standard_response(
                        False, 4000, api="create_feed_comment_api", content=content
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if comment:
                if comment.parent:

                    state = Common.CommentState.CHILD_COMMENT
                    receiver = comment.writer
                    comment = comment.parent

                order_gap = self.nested_comment_order_gap
                last_comment = (
                    FeedComment.objects.filter(
                        feed=feed,
                        order__range=(
                            comment.order // order * order,
                            (comment.order // order + 1) * order - 1,
                        ),
                    )
                    .order_by("order")
                    .last()
                )
            else:
                order_gap = self.default_order_gap
                last_comment = (
                    FeedComment.objects.filter(feed=feed, parent__isnull=True)
                    .order_by("order")
                    .last()
                )

            if last_comment:
                order = last_comment.order + order_gap

            FeedComment.objects.create(
                feed=feed, parent=comment, writer=account, content=content, order=order
            )

            if state == Common.CommentState.PARENT_COMMENT:
                if comment and comment.writer != account:
                    receiver = comment.writer
                    ArchivesHelpers.push_notifications(
                        account=account,
                        sender=sender,
                        receiver=receiver,
                        feed=feed,
                        content=content,
                        state=Common.CommentState.PARENT_COMMENT,
                        type=Common.PushNotificationType.COMMENT,
                    )

                elif not comment and feed.account != account:
                    receiver = feed.account
                    ArchivesHelpers.push_notifications(
                        account=account,
                        sender=sender,
                        receiver=receiver,
                        feed=feed,
                        content=content,
                        state=Common.CommentState.PARENT_COMMENT,
                        type=Common.PushNotificationType.COMMENT,
                    )

            if state == Common.CommentState.CHILD_COMMENT:

                if receiver != account:

                    ArchivesHelpers.push_notifications(
                        account=account,
                        sender=sender,
                        receiver=receiver,
                        feed=feed,
                        content=content,
                        state=Common.CommentState.CHILD_COMMENT,
                        type=Common.PushNotificationType.COMMENT,
                    )

            return Response(Common.fooiy_standard_response(True))

        except Exception as e:
            return Response(
                Common.fooiy_standard_response(
                    False, 5058, account=request.account, feed=request.feed, error=e
                )
            )

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @method_decorator(FeedsHelpers.get_feed_comment_from_request())
    def patch(self, request):
        """
        # 피드 댓글 변경 API
        """
        comment = request.comment
        account = request.account
        content = request.data.get("content", None)

        try:
            if not content:
                return Response(
                    Common.fooiy_standard_response(
                        False, 4000, api="create_feed_comment_api", content=content
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if comment.writer == account:
                comment.content = content
                comment.save(update_fields=["content"])

            return Response(Common.fooiy_standard_response(True))

        except Exception as e:
            return Response(
                Common.fooiy_standard_response(
                    False, 5059, account=request.account, feed=request.feed, error=e
                )
            )

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @method_decorator(FeedsHelpers.get_feed_comment_from_request())
    def destroy(self, request, pk=None):
        """
        # 피드 댓글 삭제 API
        """
        comment = request.comment
        account = request.account
        try:
            if comment.writer == account or comment.feed.account == account:
                child_comments = FeedComment.objects.filter(parent=comment)
                for child_comment in child_comments:
                    child_comment.delete()
                comment.delete()

            return Response(Common.fooiy_standard_response(True))

        except Exception as e:
            return Response(
                Common.fooiy_standard_response(
                    False, 5060, account=request.account, feed=request.feed, error=e
                )
            )

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @method_decorator(FeedsHelpers.get_feed_comment_from_request())
    @action(detail=False, methods=["get"])
    def report(self, request):
        """
        # 피드 댓글 신고 API
        """
        comment = request.comment
        account = request.account
        try:
            comment.is_reported = True
            comment.save(update_fields=["is_reported"])

            Common.slack_post_message(
                "#user_report",
                "",
                FeedsHelpers.get_notification_report_comment_attachments(
                    account, comment
                ),
            )

            return Response(Common.fooiy_standard_response(True))

        except Exception as e:
            return Response(
                Common.fooiy_standard_response(
                    False,
                    5061,
                    account=request.account,
                    comment=request.comment,
                    error=e,
                )
            )
