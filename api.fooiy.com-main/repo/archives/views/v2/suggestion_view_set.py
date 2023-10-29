from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.viewsets import (
    mixins,
    GenericViewSet,
)

from rest_framework.response import Response

from fooiy.settings import DEBUG
from common import index as Common

from accounts.helpers import index as AccountsHelpers
from ...models import Suggestion, SUGGESTION_TYPE

import logging

logger = logging.getLogger("api")


class SuggestionViewSet(mixins.CreateModelMixin, GenericViewSet):
    """
    # 문의 관련 뷰셋
    ---
    - archives/suggestion (post) : 문의 등록 API
    """

    http_method_names = ["post"]

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    def create(self, request, *args, **kwargs):
        """
        # 문의 등록 API
        """
        account = request.account

        _type = request.data.get("type", None)
        content = request.data.get("content", None)

        try:
            Suggestion.objects.create(
                type=_type,
                account=account,
                content=content,
            )

            Common.slack_post_message(
                "#notify_suggestion",
                "",
                Common.SlackAttachments.suggestion_slack_attachments(
                    account,
                    _type,
                    content,
                ),
            )

            return Response(
                Common.fooiy_standard_response(
                    True,
                ),
            )

        except Exception as e:
            return Response(
                Common.fooiy_standard_response(
                    False,
                    5036,
                    account_id=account.public_id,
                    type=_type,
                    content=content,
                    error=e,
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
