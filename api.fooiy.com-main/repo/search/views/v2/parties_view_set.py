from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.response import Response

from accounts.helpers import index as AccountHelpers
from common import index as Common
from accounts.models import Party
from accounts.serializers.v2 import index as AccountSerializerV2

import logging

logger = logging.getLogger("api")


class PartiesSearchPagination(Common.FooiyPagenation):
    default_limit = 20


class PartiesSearchViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    # 파티 검색 관련 뷰셋
    """

    pagination_class = PartiesSearchPagination
    http_method_names = ["get"]

    @method_decorator(AccountHelpers.fooiy_account_guard())
    def list(self, request):
        """
        # 파티 검색 API
        """

        keyword = request.query_params.get("keyword", None)
        payload = {}
        if not keyword:
            return Response(
                Common.fooiy_standard_response(
                    False, 4000, api="party_search_list_api", keyword=keyword
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            parties = Party.objects.filter(name__startswith=keyword)

            page_parties = self.paginate_queryset(parties)
            page_parties = AccountSerializerV2.PartyListSerializer(
                page_parties, many=True
            ).data

            if page_parties is not None:
                payload["accounts_list"] = self.get_paginated_response(page_parties)

            return Response(Common.fooiy_standard_response(True, payload))
        except Exception as e:
            return Response(
                Common.fooiy_standard_response(False, 5070, error=e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
