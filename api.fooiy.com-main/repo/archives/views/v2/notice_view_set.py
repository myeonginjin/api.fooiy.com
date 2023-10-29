from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.viewsets import (
    mixins,
    GenericViewSet,
)

from rest_framework.response import Response
from rest_framework.decorators import action

from common import index as Common
from accounts.helpers import index as AccountsHelpers
from ...serializers.v2 import index as ArchivesSerializerV1
from ...models import Notice

import logging

logger = logging.getLogger("api")


class NoticeViewSet(mixins.ListModelMixin, GenericViewSet):
    @method_decorator(AccountsHelpers.fooiy_account_guard())
    def list(self, request):
        """
        # 공지사항 API
        """
        payload = {}

        try:
            notices = Notice.objects.filter(
                is_exposure=True,
                is_emergency=False,
            ).order_by("order", "-id")

            payload["notice_list"] = ArchivesSerializerV1.NoticeSerializer(
                notices, many=True
            ).data

            return Response(Common.fooiy_standard_response(True, payload))

        except Exception as e:
            return Response(
                Common.fooiy_standard_response(False, 5035, error=e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
