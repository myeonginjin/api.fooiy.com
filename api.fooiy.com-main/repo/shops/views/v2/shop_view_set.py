from django.utils.decorators import method_decorator
from django.db.models import F, Q
from rest_framework import status
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from search.serializers.v2 import index as SearchSerailizerV2
from search.models import SearchSpot
from common import index as Common
from archives.models import Image, AddressCluster
from accounts.helpers import index as AccountsHelpers
from shops.helpers import index as ShopsHelpers
from ...models import (
    Shop,
    Menu,
    LATITUDE_METER_RATIO,
    LONGITUDE_METER_RATIO,
)
from archives.serializers.v2 import index as ArchivesSerailizerV2
from ...serializers.v2 import index as ShopsSerailizerV2

import logging

logger = logging.getLogger("api")


class ShopPagination(Common.FooiyPagenation):
    default_limit = 20


class ShopViewSet(mixins.DestroyModelMixin, GenericViewSet):
    """
    # 매장 관련 뷰셋
    ---
    - shops/nearby/ (get) : 근처 매장 검색 API
    - shops/search/ (get) : 매장 이름으로 검색 API
    """

    serializer_class = ShopsSerailizerV2.ShopListSerializer
    http_method_names = ["get"]
    pagination_class = ShopPagination

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @method_decorator(ShopsHelpers.get_shop_from_request())
    @action(detail=False, methods=["get"])
    def info(self, request):
        shop = request.shop
        payload = {}
        try:
            payload["shop_info"] = ShopsSerailizerV2.ShopInfoSerializer(
                shop, context={"fooiyti": request.account.fooiyti.fooiyti.lower()}
            ).data
            return Response(
                Common.fooiy_standard_response(True, payload),
            )
        except Exception as e:
            return Response(
                Common.fooiy_standard_response(False, 5034, error=e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @action(detail=False, methods=["get"])
    def nearby(self, request):
        """
        # 근처 매장 검색 API
        """

        address = request.query_params.get("address", None)
        shop_category = request.query_params.get("shop_category", None)

        distance = 100
        payload = {}

        if address:
            try:
                longitude, latitude = Common.convert_address_to_coordinate(address)
                longitude_distance, latitude_distance = (
                    distance * LONGITUDE_METER_RATIO,
                    distance * LATITUDE_METER_RATIO,
                )
                longitude_min, longitude_max, latitude_min, latitude_max = (
                    eval(f"{longitude}-{longitude_distance}"),
                    eval(f"{longitude}+{longitude_distance}"),
                    eval(f"{latitude}-{latitude_distance}"),
                    eval(f"{latitude}+{latitude_distance}"),
                )
                shops = Shop.objects.filter(
                    longitude__range=(longitude_min, longitude_max),
                    latitude__range=(latitude_min, latitude_max),
                    is_exposure=True,
                ).only(
                    "public_id",
                    "name",
                    "address",
                    "longitude",
                    "latitude",
                    "is_exposure",
                )

                if shop_category == Common.global_variables.category_cafe:
                    shops = shops.filter(category__name=shop_category)
                else:
                    shops = shops.exclude(
                        category__name=Common.global_variables.category_cafe
                    )

                page_shops = self.paginate_queryset(shops)
                if page_shops is not None:
                    payload["shop_list"] = self.get_paginated_response(
                        ShopsSerailizerV2.ShopListSerializer(page_shops, many=True).data
                    )
                else:
                    payload["shop_list"] = ShopsSerailizerV2.ShopListSerializer(
                        shops, many=True
                    ).data

                return Response(
                    Common.fooiy_standard_response(True, payload),
                )

            except Exception as e:
                return Response(
                    Common.fooiy_standard_response(False, 5012, error=e),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        else:
            return Response(
                Common.fooiy_standard_response(
                    False,
                    4020,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @action(detail=False, methods=["get"])
    def shop_map_marker(self, request):
        """
        # 음식점 지도 마커 API
        """
        longitude_left_bottom = request.query_params.get(
            "longitude_left_bottom",
            Common.global_variables.default_longitude_left_bottom,
        )
        latitude_left_bottom = request.query_params.get(
            "latitude_left_bottom", Common.global_variables.default_latitude_left_bottom
        )
        longitude_right_top = request.query_params.get(
            "longitude_right_top", Common.global_variables.default_longitude_right_top
        )
        latitude_right_top = request.query_params.get(
            "latitude_right_top", Common.global_variables.default_latitude_right_top
        )
        shop_category = request.query_params.get("shop_category", None)
        depth = request.query_params.get("depth", None)
        type = request.query_params.get("type", None)
        payload = {}

        try:
            if type == Common.ShopMapMarkerType.SPOT:

                regions = {}
                regions["regions"] = SearchSerailizerV2.SpotSearchSerializer(
                    SearchSpot.objects.filter(
                        type=Common.ShopMapMarkerType.LANDMARK,
                    ),
                    many=True,
                ).data

                payload["spot_list"] = regions

                return Response(
                    Common.fooiy_standard_response(True, payload),
                )

            # Depth 1
            if depth == Common.global_variables.LARGEST_DEPTH:
                regions = {}
                regions["regions"] = ArchivesSerailizerV2.AddressClusterSerializer(
                    AddressCluster.objects.filter(
                        count__gt=0,
                        depth=depth,
                        longitude__range=(longitude_left_bottom, longitude_right_top),
                        latitude__range=(latitude_left_bottom, latitude_right_top),
                    ),
                    many=True,
                ).data

                payload["shop_list"] = regions

            # Depth 3,4
            else:
                shops = (
                    Shop.objects.filter(
                        longitude__range=(longitude_left_bottom, longitude_right_top),
                        latitude__range=(latitude_left_bottom, latitude_right_top),
                        is_exposure=True,
                        shopscore__isnull=False,
                        feed__isnull=False,
                    )
                    .only(
                        "longitude",
                        "latitude",
                    )
                    .distinct()
                )
                if shop_category == Common.global_variables.category_cafe:
                    shops = shops.filter(category__name=shop_category)
                else:
                    shops = shops.filter(
                        ~Q(category__name=Common.global_variables.category_cafe)
                    )

                shops_count = shops.count()

                if depth == Common.global_variables.LOWEST_DEPTH:
                    if shops:
                        shops = ShopsSerailizerV2.ShopMapMarkerSerializer(
                            shops, many=True
                        ).data

                    payload["shop_count"] = shops_count
                    payload["shop_list"] = shops

                # Depth2
                else:
                    payload["shop_count"] = shops_count

            return Response(
                Common.fooiy_standard_response(True, payload),
            )

        except Exception as e:
            return Response(
                Common.fooiy_standard_response(False, 5024, error=e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @action(detail=False, methods=["get"])
    def shop_map_marker_detail(self, request):
        """
        # 음식점 지도 마커 상세 API
        """
        longitude = request.query_params.get("longitude", None)
        latitude = request.query_params.get("latitude", None)
        shop_category = request.query_params.get("shop_category", None)

        payload = {}

        try:
            account = request.account
        except:
            account = None

        if not (longitude and latitude):
            return Response(
                Common.fooiy_standard_response(
                    False, 4000, longitude=longitude, latitude=latitude
                ),
                status=status.HTTP_400_BAD_REQUES,
            )

        try:
            shops = (
                Shop.objects.annotate(score=ShopsHelpers.personalize_fooiyti(account))
                .filter(longitude=longitude, latitude=latitude)
                .order_by("-score")
            )

            if shop_category == Common.global_variables.category_cafe:
                shops = shops.filter(category__name=shop_category)
            else:
                shops = shops.filter(
                    ~Q(category__name=Common.global_variables.category_cafe)
                )

            shops_count = shops.count()

            shops = ShopsSerailizerV2.ShopMapDetailSerializer(
                shops,
                many=True,
            ).data

            payload["shop_count"] = shops_count
            payload["shop_list"] = shops

            return Response(Common.fooiy_standard_response(True, payload))

        except Exception as e:
            return Response(
                Common.fooiy_standard_response(False, 5001, error=e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @action(detail=False, methods=["get"])
    def shop_map_list(self, request):
        """
        # 음식점 지도 리스트 API
        """
        longitude_left_bottom = request.query_params.get(
            "longitude_left_bottom",
            Common.global_variables.default_longitude_left_bottom,
        )
        latitude_left_bottom = request.query_params.get(
            "latitude_left_bottom", Common.global_variables.default_latitude_left_bottom
        )
        longitude_right_top = request.query_params.get(
            "longitude_right_top", Common.global_variables.default_longitude_right_top
        )
        latitude_right_top = request.query_params.get(
            "latitude_right_top", Common.global_variables.default_latitude_right_top
        )
        shop_category = request.query_params.get("shop_category", None)
        _filter = request.query_params.get("filter", Common.ShopFilter.PERSONALIZE)
        try:
            account = request.account
        except:
            account = None

        payload = {}

        shops = Shop.objects.all()

        try:
            shops = shops.filter(
                longitude__range=(longitude_left_bottom, longitude_right_top),
                latitude__range=(latitude_left_bottom, latitude_right_top),
                is_exposure=True,
                feed__isnull=False,
                shopscore__isnull=False,
                shopfooiyti__isnull=False,
            )
            if shop_category == Common.global_variables.category_cafe:
                shops = shops.filter(category__name=shop_category)
                shops = shops.annotate(score=F("shopscore__score"))
            else:
                shops = shops.filter(
                    ~Q(category__name=Common.global_variables.category_cafe)
                )
                if _filter == Common.ShopFilter.PERSONALIZE:
                    shops = shops.annotate(
                        score=ShopsHelpers.personalize_fooiyti(account)
                    )
                elif _filter == Common.ShopFilter.POPULAR:
                    shops = shops.annotate(score=F("shopscore__score"))

            shops = shops.distinct().order_by("-score", "created_at")

            pagenate_shops = self.paginate_queryset(shops)

            if pagenate_shops:
                pagenate_shops = ShopsSerailizerV2.ShopMapListSerializer(
                    pagenate_shops,
                    many=True,
                ).data
                payload["shop_list"] = self.get_paginated_response(pagenate_shops)
            else:
                # ! Delete
                payload["image"] = Image.objects.get(
                    type=Common.ArchivesImageType.NSI
                ).image.url

            return Response(
                Common.fooiy_standard_response(True, payload),
            )

        except Exception as e:
            return Response(
                Common.fooiy_standard_response(False, 5025, error=e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
