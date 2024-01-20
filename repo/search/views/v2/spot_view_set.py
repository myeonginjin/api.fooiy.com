from django.utils.decorators import method_decorator
from django.db.models import F
from django.db.models.functions import Abs
from rest_framework import status
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.response import Response

from accounts.helpers import index as AccountHelpers
from common import index as Common
from ...serializers.v2 import index as SpotSearchSerializersV2
from search.helpers import index as SearchHelpers
from ...models import SearchSpot

import logging

logger = logging.getLogger("api")


class SpotSearchPagination(Common.FooiyPagenation):
    default_limit = 12


class SpotSearchViewSet(mixins.ListModelMixin, GenericViewSet):
    pagination_class = SpotSearchPagination
    http_method_names = ["get"]

    @method_decorator(AccountHelpers.fooiy_account_guard())
    def list(self, request):
        longitude = request.query_params.get("longitude", None)
        latitude = request.query_params.get("latitude", None)
        keyword = request.query_params.get("keyword", "")
        payload = {}

        if not keyword:
            return Response(
                Common.fooiy_standard_response(
                    False, 4000, api="spot_search_list_api", keyword=keyword
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            keyword = SearchHelpers.refine_keyword(keyword)

            spots = SearchSpot.objects.filter(name__icontains=keyword)
            if not spots:
                Common.slack_post_message(
                    "#request_spots",
                    "",
                    SearchHelpers.get_keyword_slack_attachments(keyword),
                )

            if longitude and latitude and len(keyword) > 1:
                spots = (
                    spots.annotate(distance_longitude=Abs(F("longitude") - longitude))
                    .annotate(distance_latitude=Abs(F("latitude") - latitude))
                    .annotate(order=F("distance_longitude") + F("distance_latitude"))
                    .order_by("order")
                )

            page_spots = self.paginate_queryset(spots)
            page_spots = SpotSearchSerializersV2.SpotSearchSerializer(
                page_spots, many=True
            ).data

            if page_spots is not None:
                payload["spot_list"] = self.get_paginated_response(page_spots)
            else:
                payload["spot_list"] = page_spots

            return Response(Common.fooiy_standard_response(True, payload))

        except Exception as e:
            return Response(
                Common.fooiy_standard_response(False, 5056, error=e),
                status=status.HTTP_400_BAD_REQUEST,
            )
