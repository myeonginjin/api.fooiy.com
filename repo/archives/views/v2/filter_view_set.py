from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.viewsets import (
    mixins,
    GenericViewSet,
)
from django.db.models import F, Q
from rest_framework.response import Response
from rest_framework.decorators import action

from common import index as Common
from accounts.helpers import index as AccountsHelpers
from archives.helpers import index as ArchivesHelpers
from accounts.models import Storage

import logging

logger = logging.getLogger("api")


class FilterViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    # 필터 뷰셋
    """

    http_method_names = ["get"]

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @action(detail=False, methods=["get"])
    def address(self, request):
        """
        # 필터 리스트 API
        """
        payload = {}
        account = request.account

        try:
            address = ArchivesHelpers.FilterAddress.remove_duplicates(
                Storage.objects.annotate(address=F("feed__shop__address_depth1"))
                .filter(
                    Q(account=account, state=Common.FeedState.SUBSCRIBE)
                    & ~Q(feed__isnull=True)
                    & ~Q(feed__shop__address_depth1__isnull=True)
                )
                .values_list("address")
            )
            address = ArchivesHelpers.FilterAddress.sort_area_by_priority(address)
            payload["address_list"] = address

            return Response(
                Common.fooiy_standard_response(True, payload),
            )
        except Exception as e:
            return Response(
                Common.fooiy_standard_response(False, 5026, error=e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
