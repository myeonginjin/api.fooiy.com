from django.utils.decorators import method_decorator
from django.db import transaction

from rest_framework import status
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.response import Response

from accounts.helpers import index as AccountsHelpers
from shops.helpers import index as ShopsHelpers
from ...models import Feed, FeedFooiyti
from ...helpers import index as FeedsHelpers
from archives.models import Image
from common import index as Common
from shops import tasks as ShopsTasks

import logging

logger = logging.getLogger("api")


class RecordViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    """
    # 기록 관련 뷰셋
    """

    http_method_names = ["get", "post", "delete", "patch"]

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @method_decorator(ShopsHelpers.get_shop_from_request())
    def create(self, request, *args, **kwargs):
        """
        # 기록 등록 API
        """

        account = request.account
        shop = request.shop
        menu_id = request.data.get("menu_id", None)
        comment = request.data.get("comment", None)
        taste_evaluation = request.data.get("taste_evaluation", None)
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
        is_exposure = Common.convert_request_to_boolean[
            request.data.get("is_exposure", "true")
        ]
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

        if menu_id and taste_evaluation and image_1:
            try:
                with transaction.atomic():
                    feed = Feed.objects.create(
                        account=account,
                        fooiyti=account.fooiyti,
                        shop=shop,
                        menu_id=menu_id,
                        description=comment,
                        taste_evaluation=taste_evaluation,
                        is_exposure=is_exposure,
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
                            menu_id=menu_id,
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
                AccountsHelpers.CheckRank.check_change_rank(
                    account=feed.account,
                    type=Common.CheckChangeRankType.REGISTRATION,
                )

                ShopsTasks.CalculateShopScore.calculate_shop_fooiyti(
                    account, feed, fooiyti_list, Common.FeedUpdateState.REGISTER
                )
                ShopsTasks.CalculateShopScore.calculate_shop_score(
                    feed, taste_evaluation, Common.FeedUpdateState.REGISTER
                )
                return Response(
                    Common.fooiy_standard_response(
                        True,
                    )
                )
            except Exception as e:
                return Response(
                    Common.fooiy_standard_response(False, 5011, error=e),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        else:
            return Response(
                Common.fooiy_standard_response(
                    False,
                    4019,
                    menu_id=menu_id,
                    taste_evaluation=taste_evaluation,
                    image_1=image_1,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    def destroy(self, request, pk=None):
        """
        # 기록 삭제 API
        """
        account = request.account

        if not pk:
            return Response(
                Common.fooiy_standard_response(
                    False,
                    4042,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            feed = Feed.objects.get(account=account, id=pk)
            print(feed)
            ShopsTasks.CalculateShopScore.calculate_shop_fooiyti(
                account, feed, None, Common.FeedUpdateState.DELETE
            )
            ShopsTasks.CalculateShopScore.calculate_shop_score(
                feed, None, Common.FeedUpdateState.DELETE
            )
            feed.delete()

            if account.rank == Common.RankType.RANKER:
                AccountsHelpers.CheckRank.check_change_rank(
                    account=account,
                    type=Common.CheckChangeRankType.DEMOTION,
                )

            elif not account.rank == Common.RankType.RANKER:

                AccountsHelpers.CheckRank.check_current_rank(
                    account=account,
                    no_push=True,
                )

            return Response(Common.fooiy_standard_response(True))

        except Exception as e:
            return Response(
                Common.fooiy_standard_response(False, 5038, error=e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
