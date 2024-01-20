from django.db import transaction
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from shops.models import Shop, Menu, ShopScore, ShopFooiyti
from feeds.models import Pioneer, PIONEER_REJECT_REASON
from ...serializers.v2 import index as WebSerializerV2
from ...helpers import index as WebHelpers
from common import index as Common
from shops.helpers import index as ShopsHelpers
from archives.helpers import index as ArchivesHelpers
from accounts.helpers import index as AccountsHelpers


import logging

logger = logging.getLogger("api")


@swagger_auto_schema(methods=["get", "patch"])
class PioneerViewSet(GenericViewSet):
    """
    # 개척 관련 뷰셋
    """

    serializer_class = WebSerializerV2.PioneerCheckSerializer
    http_method_names = ["get", "patch"]

    @method_decorator(WebHelpers.fooiy_web_guard())
    @action(detail=False, methods=["get"])
    def check(self, request):
        """
        # GET : 웹 개척 검수 정보 API
        """

        try:
            pioneer_id = request.query_params.get("pioneer_id", None)

            pioneer = Pioneer.objects.get(id=pioneer_id)

            if (
                pioneer.state != Common.PioneerState.CONFIRM
                and pioneer.state != Common.PioneerState.REJECT
            ):
                return Response(
                    Common.fooiy_standard_response(
                        True,
                        {"is_already_checked": True},
                    ),
                )

            return Response(
                Common.fooiy_standard_response(
                    True,
                    {
                        "pioneer_info": WebSerializerV2.PioneerCheckSerializer(
                            pioneer
                        ).data,
                        "reject_reasons": [
                            {
                                "name": reason[1],
                                "value": reason[0],
                            }
                            for reason in PIONEER_REJECT_REASON
                        ],
                    },
                ),
            )
        except Pioneer.DoesNotExist as e:
            return Response(
                Common.fooiy_standard_response(
                    False, 4028, id_uuid=pioneer_id, error=e
                ),
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                Common.fooiy_standard_response(
                    False, 5021, id_uuid=pioneer_id, error=e
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @method_decorator(WebHelpers.fooiy_web_guard())
    @action(detail=False, methods=["patch"])
    def check_success(self, request):
        """
        # PATCH : 웹 개척 검수 성공 API
        """
        _type = request.data.get(
            "type", Common.ShopMainCategory.COMMON
        )  # 카페, 주점, 일반 음식점
        pioneer_id = request.data.get("pioneer_id", None)

        # 매장 관련
        shop_name = request.data.get("shop_name", None)
        category1 = request.data.get("category1", None)
        category2 = request.data.get("category2", None)
        category3 = request.data.get("category3", None)
        address = Common.synchronize_address(request.data.get("address", None))

        # 메뉴 관련
        menu_name = request.data.get("menu_name", None)
        menu_price = request.data.get("menu_price", None)
        menu_category = request.data.get("menu_category", None)

        try:
            # 타입이랑 개척정보가 없을 때
            pioneer = Pioneer.objects.filter(id=pioneer_id)
            if not (_type in Common.ShopMainCategory and pioneer.exists()):
                return Response(
                    Common.fooiy_standard_response(
                        False, 4000, api="web_check_success", pioneer_id=pioneer_id
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # 그 외의 필수로 필요한 정보가 없을 때
            if not (
                shop_name and address and menu_name and menu_price and menu_category
            ):
                return Response(
                    Common.fooiy_standard_response(
                        False,
                        4002,
                        shop_name=shop_name,
                        address=address,
                        category1=category1,
                        menu_name=menu_name,
                        menu_price=menu_price,
                        menu_category=menu_category,
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            pioneer = WebHelpers.register_pioneer(
                pioneer=pioneer.first(),
                shop_name=shop_name,
                address=address,
                menu_name=menu_name,
                menu_price=menu_price,
                menu_category=menu_category,
                category1=category1,
                category2=category2,
                category3=category3,
                _type=_type,
            )

            #### 개척 등록 및 푸시 알림 로직 ####
            if WebHelpers.feed_register(pioneer):
                #### 계정 랭크 변화 확인 및 푸시 로직 ####
                AccountsHelpers.CheckRank.check_change_rank(
                    account=pioneer.account,
                    type=Common.CheckChangeRankType.REGISTRATION,
                )
                return Response(Common.fooiy_standard_response(True))

        except Exception as e:
            pioneer.state = Common.PioneerState.ERROR
            pioneer.error_message = str(e)
            pioneer.save(update_fields=["state", "error_message"])

            return Response(
                Common.fooiy_standard_response(False, 5030, id=pioneer_id, error=e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @method_decorator(WebHelpers.fooiy_web_guard())
    @action(detail=False, methods=["patch"])
    def check_reject(self, request):
        """
        # PATCH : 웹 개척 검수 반려 API
        ---
        - ## header
            - ### Authorization : 푸이 웹 토큰
        - ## body
            - ### pioneer_id : 개척 id
            - ### reason : 반려 사유
        - ## Error
            - ### 4035 : 일치하는 개척 id를 찾을 수 없음
            - ### 4036 : 필수 필드 누락 (반려 사유)
            - ### 4995 : 푸이 웹 토큰이 유효하지 않음
            - ### 5031 : 서버에러
        """
        pioneer_id = request.data.get("pioneer_id", None)
        reason = request.data.get("reason", None)

        if reason:
            try:
                try:
                    pioneer = Pioneer.objects.get(id=pioneer_id)

                    if (
                        pioneer.state != Common.PioneerState.CONFIRM
                        and pioneer.state != Common.PioneerState.ERROR
                    ):
                        return Response(
                            Common.fooiy_standard_response(
                                True,
                                {"is_already_checked": True},
                            ),
                        )
                except Pioneer.DoesNotExist as e:
                    return Response(
                        Common.fooiy_standard_response(
                            False, 4035, id_uuid=pioneer_id, error=e
                        ),
                        status=status.HTTP_404_NOT_FOUND,
                    )

                pioneer.state = Common.PioneerState.REJECT
                pioneer.reject_reason = reason
                pioneer.save(update_fields=["state", "reject_reason"])

                Common.slack_post_message(
                    "#request_pioneer",
                    f"*[🚫 {ShopsHelpers.get_shop_and_menu(pioneer.shop_name, pioneer.menu_name)} 개척 반려 🚫]*\n*반려사유* : {dict(PIONEER_REJECT_REASON)[reason]}",
                )

                #### 개척 반려 푸시 발송 로직 ####

                ArchivesHelpers.push_notifications(
                    pioneer=pioneer,
                    receiver=pioneer.account,
                    type=Common.PushNotificationType.PIONEER_REJECT,
                )

                return Response(
                    Common.fooiy_standard_response(
                        True,
                    ),
                )

            except Exception as e:
                pioneer.state = Common.PioneerState.ERROR
                pioneer.error_message = str(e)
                pioneer.save(update_fields=["state", "error_message"])

                return Response(
                    Common.fooiy_standard_response(
                        False, 5031, id_uuid=pioneer_id, error=e
                    ),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return Response(
                Common.fooiy_standard_response(False, 4036, reason=reason),
                status=status.HTTP_400_BAD_REQUEST,
            )
