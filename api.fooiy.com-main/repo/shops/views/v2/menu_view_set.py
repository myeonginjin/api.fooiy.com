from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.response import Response

from accounts.helpers import index as AccountsHelpers
from shops.helpers import index as ShopsHelpers
from common import index as Common
from ...models import Menu
from ...serializers.v2 import index as ShopsSerailizerV2
from archives.models import Suggestion, SUGGESTION_TYPE
from fooiy.settings import DEBUG
import logging

logger = logging.getLogger("api")


class MenuViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    # 메뉴 관련 뷰셋
    ---
    - shops/menu/ (get) : 메뉴 리스트 API
    """

    serializer_class = ShopsSerailizerV2.MenuListSerializer
    http_method_names = ["get", "post"]

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @method_decorator(ShopsHelpers.get_shop_from_request())
    def list(self, request):
        """
        # 메뉴 리스트 API
        ---
        - ## header
            - ### Authorization : 푸이 계정 토큰
            - ### os : os
            - ### device-id : device uuid
        - ## query_params
            - ### shop_id : 매장 아이디
            - ### _type : API 타입 (개척 진행상황 메뉴판 OR 매장 피드 메뉴판)
        - ## payload
            - ### menu_list : 메뉴 정보 리스트
        - ## Error
            - ### 4996 : 요청에 매장 아이디를 넣지 않음
            - ### 4997 : 요청에 들어있는 매장 아이디(퍼블릭)에 해당하는 매장이 없음
            - ### 4998 : 중복 로그인
            - ### 4999 : 푸이 토큰이 유효하지 않음
            - ### 5016 : 서버에러
            - ### 5999 : 서버에러
        """

        _type = request.query_params.get("type", Common.AmenuType.A_MENU)
        shop = request.shop
        payload = {}

        try:
            menus = Menu.objects.filter(shop=shop)
            shop_category = (
                shop.category.first().name if shop.category.exists() else None
            )

            if _type == Common.AmenuType.SELECT_MENU:
                payload["menu_list"] = ShopsSerailizerV2.MenuListSerializer(
                    menus.order_by("-price"),
                    many=True,
                ).data

            else:
                payload["menu_list"] = ShopsHelpers.make_a_menu(
                    menus=menus.order_by("-id"),
                    shop_category=shop_category,
                )

            return Response(Common.fooiy_standard_response(True, payload))

        except Exception as e:
            return Response(
                Common.fooiy_standard_response(
                    False,
                    5016,
                    shop_name=shop.name,
                    type=_type,
                    error=e,
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @method_decorator(ShopsHelpers.get_shop_from_request())
    @action(detail=False, methods=["post"])
    def suggestion(self, request, *args, **kwargs):
        """
        # 문의 등록 API
        """

        account = request.account
        shop = request.shop
        content = request.data.get("content", None)

        try:
            Suggestion.objects.create(
                type=Common.SuggestionType.TIP_OFF,
                account=account,
                content=content,
            )

            Common.slack_post_message(
                "#notify_suggestion",
                "",
                Common.SlackAttachments.tip_off_slack_attachments(
                    account,
                    shop,
                    content,
                ),
            )

            return Response(
                Common.fooiy_standard_response(
                    True,
                ),
            )

        except Exception as e:
            return Response(
                Common.fooiy_standard_response(
                    False,
                    5036,
                    account_id=account.public_id,
                    content=content,
                    error=e,
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
