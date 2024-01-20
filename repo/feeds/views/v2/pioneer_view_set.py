from django.utils.decorators import method_decorator
from django.db.models import Q
from django.db import transaction

from rest_framework import status
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.response import Response

from accounts.helpers import index as AccountsHelpers
from shops.models import Shop, Menu
from feeds.models import Feed
from ...helpers import index as FeedsHelpers
from ...models import Pioneer
from common import index as Common
from ...models import Feed, FeedFooiyti
from archives.models import Image
import logging
from shops import tasks as ShopsTasks
from shops.helpers import index as ShopsHelpers

logger = logging.getLogger("api")


class PioneerViewSet(mixins.CreateModelMixin, GenericViewSet):
    """
    # 개척 관련 뷰셋
    ---
    - feeds/pioneer/ (post) : 개척 등록 API
    """

    http_method_names = ["get", "post"]

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @method_decorator(ShopsHelpers.get_shop_from_request(require=False))
    def create(self, request, *args, **kwargs):
        """
        # 개척 등록 API
        ---
        - ## header
            - ### Authorization : 푸이 계정 토큰
            - ### os : os
            - ### device-id : device uuid
        - ## body
            - ### shop_name : 매장 명
            - ### menu_name : 메뉴 명
            - ### menu_price : 메뉴 가격
            - ### comment : 개척 코멘트
            - ### taste_evaluation : 맛 평가 (숫자로 전송, 100: 좋아요, 50: 보통, 0: 아쉬워요)
            - ### image_1 : 개척 이미지 (필수)
            - ### image_2 : 개척 이미지
            - ### image_3 : 개척 이미지
            - ### image_4 : 개척 이미지
            - ### image_5 : 개척 이미지
            - ### address : 매장 주소
        """
        account = request.account
        shop_name = request.data.get("shop_name", None)
        menu_name = request.data.get("menu_name", None)
        comment = request.data.get("comment", None)
        taste_evaluation = request.data.get("taste_evaluation", "0")
        address = Common.synchronize_address(request.data.get("address", None))
        image_1 = request.FILES.get("image_1", None)
        image_2 = request.FILES.get("image_2", None)
        image_3 = request.FILES.get("image_3", None)
        fooiyti_e = request.data.get("fooiyti_e", "50")
        fooiyti_i = request.data.get("fooiyti_i", "50")
        fooiyti_s = request.data.get("fooiyti_s", "50")
        fooiyti_n = request.data.get("fooiyti_n", "50")
        fooiyti_t = request.data.get("fooiyti_t", "50")
        fooiyti_f = request.data.get("fooiyti_f", "50")
        fooiyti_a = request.data.get("fooiyti_a", "50")
        fooiyti_c = request.data.get("fooiyti_c", "50")
        subscribe_parties = request.data.get("subscribe_parties", None)

        if menu_name and taste_evaluation and image_1:
            menu = None
            shop = None

            try:
                if address:
                    shop = Shop.objects.filter(
                        slug=ShopsHelpers.get_shop_slug(name=shop_name, address=address)
                    )
                trimed_menu_name = menu_name.replace(" ", "")
                if request.shop or shop.exists():
                    shop = request.shop if request.shop else shop.first()
                    shop_name = shop.name
                    menus = Menu.objects.filter(shop=shop).exclude(name__isnull=True)

                    for exist_menu in menus:

                        if trimed_menu_name == exist_menu.name.replace(" ", ""):
                            menu = exist_menu

                            break

                    if menu:
                        fooiyti_list = {
                            "e": int(fooiyti_e),
                            "i": int(fooiyti_i),
                            "s": int(fooiyti_s),
                            "n": int(fooiyti_n),
                            "t": int(fooiyti_t),
                            "f": int(fooiyti_f),
                            "a": int(fooiyti_a),
                            "c": int(fooiyti_c),
                        }

                        with transaction.atomic():
                            feed = Feed.objects.create(
                                account=account,
                                fooiyti=account.fooiyti,
                                shop=shop,
                                menu=menu,
                                description=comment,
                                taste_evaluation=taste_evaluation,
                            )

                            FeedFooiyti.objects.create(
                                feed=feed,
                                fooiyti_e=fooiyti_e,
                                fooiyti_i=fooiyti_i,
                                fooiyti_s=fooiyti_s,
                                fooiyti_n=fooiyti_n,
                                fooiyti_t=fooiyti_t,
                                fooiyti_f=fooiyti_f,
                                fooiyti_a=fooiyti_a,
                                fooiyti_c=fooiyti_c,
                            )

                            Image.objects.bulk_create(
                                Image(
                                    order=index,
                                    type=Common.ArchivesImageType.F,
                                    feed=feed,
                                    menu=menu,
                                    image=image,
                                    shop=shop,
                                    account=account,
                                )
                                for index, image in enumerate(
                                    Common.create_image_list(
                                        image_1,
                                        image_2,
                                        image_3,
                                    )
                                )
                            )
                        FeedsHelpers.update_feed_parties(feed, subscribe_parties)
                        ShopsTasks.CalculateShopScore.calculate_shop_fooiyti(
                            account, feed, fooiyti_list, Common.FeedUpdateState.REGISTER
                        )
                        ShopsTasks.CalculateShopScore.calculate_shop_score(
                            feed, taste_evaluation, Common.FeedUpdateState.REGISTER
                        )

                        AccountsHelpers.CheckRank.check_change_rank(
                            account=feed.account,
                            type=Common.CheckChangeRankType.REGISTRATION,
                        )

                        return Response(
                            Common.fooiy_standard_response(
                                True,
                            ),
                            status=status.HTTP_201_CREATED,
                        )

                if subscribe_parties:
                    subscribe_parties = str(subscribe_parties)
                if not shop:
                    shop = None
                pioneer = Pioneer.objects.create(
                    account_id=account.id,
                    fooiyti=account.fooiyti,
                    shop=shop,
                    shop_name=shop_name,
                    menu_name=menu_name,
                    comment=comment,
                    taste_evaluation=taste_evaluation,
                    address=address,
                    image_1=image_1,
                    image_2=image_2,
                    image_3=image_3,
                    fooiyti_e=fooiyti_e,
                    fooiyti_i=fooiyti_i,
                    fooiyti_s=fooiyti_s,
                    fooiyti_n=fooiyti_n,
                    fooiyti_t=fooiyti_t,
                    fooiyti_f=fooiyti_f,
                    fooiyti_a=fooiyti_a,
                    fooiyti_c=fooiyti_c,
                    subscribe_party=subscribe_parties,
                )

                Common.slack_post_message(
                    "#request_pioneer",
                    "",
                    FeedsHelpers.get_request_pioneer_slack_attachments(pioneer),
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
                        5010,
                        shop_name=shop_name,
                        menu_name=menu_name,
                        comment=comment,
                        taste_evaluation=taste_evaluation,
                        address=address,
                        image_1=image_1,
                        error=e,
                    ),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        else:

            return Response(
                Common.fooiy_standard_response(
                    False,
                    4018,
                    shop_name=shop_name,
                    menu_name=menu_name,
                    taste_evaluation=taste_evaluation,
                    address=address,
                    image_1=image_1,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
