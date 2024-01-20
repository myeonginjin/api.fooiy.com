from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.response import Response

from accounts.helpers import index as AccountHelpers
from common import index as Common
from accounts.models import Account
from accounts.serializers.v2 import index as AccountSerializerV2

import logging

logger = logging.getLogger("api")


class AccountsSearchPagination(Common.FooiyPagenation):
    default_limit = 20


class AccountsSearchViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    # 계정 검색 관련 뷰셋
    """

    pagination_class = AccountsSearchPagination
    http_method_names = ["get"]

    @method_decorator(AccountHelpers.fooiy_account_guard())
    def list(self, request):
        """
        # 계정 검색 API
        """

        keyword = request.query_params.get("keyword", None)

        if not keyword:
            return Response(
                Common.fooiy_standard_response(
                    False, 4000, api="account_search_list_api", keyword=keyword
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        payload = {}

        try:
            accounts = Account.objects.filter(nickname__startswith=keyword)

            page_accounts = self.paginate_queryset(accounts)
            page_accounts = AccountSerializerV2.AccountListSerializer(
                page_accounts, many=True
            ).data

            if page_accounts is not None:
                payload["accounts_list"] = self.get_paginated_response(page_accounts)

            return Response(Common.fooiy_standard_response(True, payload))
        except Exception as e:
            return Response(
                Common.fooiy_standard_response(False, 5045, error=e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
