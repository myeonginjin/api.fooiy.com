from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Prefetch, F
from accounts.helpers import index as AccountsHelpers
from feeds.models import Feed
from archives.models import Image
from common import index as Common
from shops.models import Shop
from shops.serializers.v2 import index as ShopSerailizerV2
import logging

logger = logging.getLogger("api")


class MenuClinicPagination(Common.FooiyPagenation):
    default_limit = 12


class MenuClinicViewSet(GenericViewSet):
    http_method_names = ["get"]
    pagination_class = MenuClinicPagination

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @action(detail=False, methods=["get"])
    def latest_order(self, request):
        """
        #카테고리별 최신순 피드 리스트 API
        """

        category = request.query_params.get("category", None)
        payload = {}

        try:
            feeds = (
                Feed.objects.select_related(
                    "shop",
                )
                .prefetch_related(
                    Prefetch(
                        "image",
                        queryset=Image.objects.only("image").order_by("order"),
                        to_attr="to_image",
                    )
                )
                .filter(
                    shop__category__name=category,
                    is_exposure=True,
                    menu__isnull=False,
                    shop__isnull=False,
                )
                .exclude(account__state=Common.AccountState.WITHDRAWAL)
                .only(
                    "created_at",
                    "shop__public_id",
                    "shop__name",
                    "shop__address",
                )
                .order_by("-created_at")
                .distinct()
            )

            pagenate_feeds = self.paginate_queryset(feeds)

            pagenate_feeds = ShopSerailizerV2.LatestShopListSerializer(
                pagenate_feeds, many=True
            ).data

            payload["feed_list"] = self.get_paginated_response(pagenate_feeds)

            return Response(
                Common.fooiy_standard_response(True, payload),
            )

        except Exception as e:
            return Response(
                Common.fooiy_standard_response(False, 5061, error=e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @action(detail=False, methods=["get"])
    def distance_order(self, request):
        """
        #카테고리 별 거리순 매장 리스트 API
        """
        account = request.account
        category = request.query_params.get("category", None)
        longitude = request.query_params.get("longitude", None)
        latitude = request.query_params.get("latitude", None)

        payload = {}

        try:
            if not (longitude and latitude):
                return Response(
                    Common.fooiy_standard_response(
                        False,
                        4050,
                        account=account.id,
                        longitude=longitude,
                        latitude=latitude,
                    ),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            longitude, latitude = float(longitude), float(latitude)
            account_spot = (latitude, longitude)

            shops = (
                Shop.objects.filter(
                    category__name=category,
                    latitude__range=(
                        latitude
                        - Common.global_variables.LONGITUDE_KIOLMETER_RATIO * 2,
                        latitude
                        + Common.global_variables.LONGITUDE_KIOLMETER_RATIO * 2,
                    ),
                    longitude__range=(
                        longitude
                        - Common.global_variables.LATITUDE_KIOLMETER_RATIO * 2,
                        longitude
                        + Common.global_variables.LATITUDE_KIOLMETER_RATIO * 2,
                    ),
                    shopscore__isnull=False,
                    shopfooiyti__isnull=False,
                    feed__isnull=False,
                )
                .annotate(score=F("shopscore__score"))
                .order_by("-score")
                .distinct()
            )

            pagenate_shops = self.paginate_queryset(shops)

            pagenate_shops = ShopSerailizerV2.NearbyShopListSerializer(
                pagenate_shops, context={"account_spot": account_spot}, many=True
            ).data

            if pagenate_shops is not None:
                payload["shop_list"] = self.get_paginated_response(pagenate_shops)
            else:
                payload["shop_list"] = pagenate_shops

            return Response(Common.fooiy_standard_response(True, payload))

        except Exception as e:
            return Response(
                Common.fooiy_standard_response(False, 5062, error=e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
