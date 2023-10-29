from django.utils.decorators import method_decorator
from django.db.models import F, Q, CharField
from django.db.models.functions import Cast, Abs
from rest_framework import status
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.response import Response

from accounts.helpers import index as AccountHelpers
from common import index as Common
from shops.models import Shop, ShopCategory
from search.helpers import index as SearchHelpers
from shops.serializers.v2 import index as ShopSerailizerV2

import logging

logger = logging.getLogger("api")


class ShopsSearchPagination(Common.FooiyPagenation):
    default_limit = 12


class ShopsSearchViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    # 계정 검색 관련 뷰셋
    """

    pagination_class = ShopsSearchPagination
    http_method_names = ["get"]

    @method_decorator(AccountHelpers.fooiy_account_guard())
    def list(self, request):
        """
        # 음식점 검색 API
        """
        longitude = request.query_params.get(
            "longitude", Common.global_variables.default_longitude
        )
        latitude = request.query_params.get(
            "latitude", Common.global_variables.default_latitude
        )
        keyword = request.query_params.get("keyword", None)

        payload = {}

        try:
            if not keyword:
                return Response(
                    Common.fooiy_standard_response(
                        False, 4000, api="shop_search_list_api", keyword=keyword
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            category = SearchHelpers.get_category_from_keyword.get(keyword, "")
            shops = (
                Shop.objects.filter(
                    (
                        Q(name__icontains=keyword)
                        | Q(menu__name__icontains=keyword)
                        | Q(category__name=category)
                    ),
                    is_exposure=True,
                    shopscore__isnull=False,
                )
                .exclude(longitude__isnull=True)
                .distinct()
            )

            shops = (
                shops.annotate(distance_longitude=Abs(F("longitude") - longitude))
                .annotate(distance_latitude=Abs(F("latitude") - latitude))
                .annotate(
                    order=F("distance_longitude")
                    + F("distance_latitude")
                    - Cast("shopscore__score", CharField()) / 2500
                )
                .annotate(score=F("shopscore__score"))
                .order_by("order")
            )

            page_shops = self.paginate_queryset(shops)
            page_shops = ShopSerailizerV2.ShopMapListSerializer(
                page_shops, many=True
            ).data

            if page_shops is not None:
                payload["shop_list"] = self.get_paginated_response(page_shops)
            else:
                payload["shop_list"] = page_shops

            return Response(Common.fooiy_standard_response(True, payload))
        except Exception as e:
            return Response(
                Common.fooiy_standard_response(False, 5013, error=e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
