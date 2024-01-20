from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.viewsets import (
    mixins,
    GenericViewSet,
)

from rest_framework.response import Response
from common import index as Common
from accounts.helpers import index as AccountsHelpers
from ...serializers.v2 import index as ArchivesSerializerV2
from ...models import PushNotification

import logging

logger = logging.getLogger("api")


class PushNotificationPagination(Common.FooiyPagenation):
    default_limit = 20


class PushNotificationViewSet(mixins.ListModelMixin, GenericViewSet):
    pagination_class = PushNotificationPagination

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    def list(self, request):
        payload = {}
        try:
            account = request.account
            push_notifications = PushNotification.objects.filter(
                receiver=account
            ).order_by("-created_at")
            push_notifications = self.paginate_queryset(push_notifications)
            push_notifications = ArchivesSerializerV2.PushNotificationSerializer(
                push_notifications,
                many=True,
            ).data

            payload["push_notifications"] = self.get_paginated_response(
                push_notifications
            )

            return Response(Common.fooiy_standard_response(True, payload))

        except Exception as e:
            Response(
                Common.fooiy_standard_response(False, 5046, account=account, error=e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
