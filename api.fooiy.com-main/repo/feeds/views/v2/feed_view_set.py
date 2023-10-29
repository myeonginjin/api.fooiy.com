from django.utils.decorators import method_decorator
from django.db.models import Prefetch, Q
from django.db import transaction

from rest_framework import status
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from accounts.helpers import index as AccountsHelpers
from archives.helpers import index as ArchivesHelpers
from feeds.helpers import index as FeedsHelpers
from shops.helpers import index as ShopsHelpers
from feeds.models import Pioneer, Feed, FeedFooiyti, FeedParty
from archives.models import Image, PushNotification
from accounts.models import Storage, Like
from feeds.serializers.v2 import index as FeedsSerializerV2
from common import index as Common
from common.utils.decorators import Decorators
from shops import tasks as ShopsTasks

import logging

logger = logging.getLogger("api")


class FeedPagination(Common.FooiyPagenation):
    default_limit = 20


class FeedViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    http_method_names = ["get", "post", "patch", "delete"]
    pagination_class = FeedPagination

    @action(detail=False, methods=["get"])
    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @method_decorator(FeedsHelpers.get_feed_from_request())
    def retrieve_feed(self, request):
        """
        # 피드 상세 보기 API
        """
        feed = request.feed
        try:
            account = request.account
        except:
            account = None
        payload = {
            "feed": FeedsSerializerV2.FeedListSerializer(
                feed, context={"account": account}
            ).data
        }
        return Response(
            Common.fooiy_standard_response(True, payload),
        )

    @action(detail=False, methods=["get"])
    @method_decorator(AccountsHelpers.fooiy_account_guard())
    def mypage(self, request):
        """
        # 마이페이지 피드 리스트 API
        """

        _type = request.query_params.get("type", None)
        feed_id = request.query_params.get("feed_id", None)
        pioneer_id = request.query_params.get("pioneer_id", None)
        other_account_id = request.query_params.get("other_account_id", None)

        try:
            offset = int(request.query_params["offset"])
        except (KeyError, ValueError):
            offset = 0

        feeds = []
        confirm_pioneer = []
        confirm_pioneer_count = 0
        payload = {}

        if other_account_id:
            try:
                my_account = request.account
            except:
                my_account = None
            account = AccountsHelpers.convert_public_id_to_account(other_account_id)
            other = True
        else:
            account = request.account
            my_account = account
            other = False

        try:
            if _type not in [Common.FeedListType.IMAGE, Common.FeedListType.LIST]:
                return Response(
                    Common.fooiy_standard_response(False, 4037, type=_type),
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # 이미지 보기
            elif _type == Common.FeedListType.IMAGE:
                resize_type = Common.ImageRizeType.SMALL

                ### 자신의 마이페이지일 때 검수중인 개척 확인 ###
                if not other:
                    confirm_pioneer = (
                        Pioneer.objects.filter(
                            account=account, state=Common.PioneerState.CONFIRM
                        )
                        .only("created_at")
                        .order_by("-created_at")
                    )
                    confirm_pioneer_count = confirm_pioneer.count()
                    confirm_pioneer = (
                        FeedsSerializerV2.MypagePioneerImageListSerializer(
                            confirm_pioneer,
                            many=True,
                        ).data
                    )
                    confirm_pioneer = confirm_pioneer[offset:confirm_pioneer_count]

                feeds = (
                    Feed.objects.prefetch_related(
                        Prefetch(
                            "image",
                            queryset=Image.objects.only("image").order_by("order"),
                            to_attr="to_image",
                        )
                    )
                    .filter(account=account)
                    .only("created_at")
                    .order_by("-created_at")
                )

            # 리스트 보기
            elif _type == Common.FeedListType.LIST:
                if not (feed_id or pioneer_id):
                    return Response(
                        Common.fooiy_standard_response(
                            False, 4033, feed_id=feed_id, pioneer_id=pioneer_id
                        ),
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    resize_type = Common.ImageRizeType.MEDIUM
                    if pioneer_id:
                        created_at = Pioneer.objects.get(id=pioneer_id).created_at
                        ### 자신의 마이페이지일 때 검수중인 개척 확인 ###
                        if not other:
                            confirm_pioneer = (
                                Pioneer.objects.select_related(
                                    "account", "shop", "menu"
                                )
                                .filter(
                                    account=account,
                                    created_at__lte=created_at,
                                    state=Common.PioneerState.CONFIRM,
                                )
                                .only(
                                    "fooiyti",
                                    "taste_evaluation",
                                    "comment",
                                    "created_at",
                                    "account__public_id",
                                    "account__nickname",
                                    "account__profile_image",
                                    "shop__public_id",
                                    "shop__name",
                                    "shop__address",
                                    "menu__name",
                                    "menu__price",
                                )
                                .order_by("-created_at")
                            )
                            confirm_pioneer_count = confirm_pioneer.count()
                            confirm_pioneer = (
                                FeedsSerializerV2.MypagePioneerListSerializer(
                                    confirm_pioneer,
                                    many=True,
                                ).data
                            )
                            confirm_pioneer = confirm_pioneer[
                                offset:confirm_pioneer_count
                            ]
                    else:
                        created_at = Feed.objects.get(id=feed_id).created_at

                    feeds = (
                        Feed.objects.select_related("account", "shop", "menu")
                        .prefetch_related(
                            Prefetch(
                                "image",
                                queryset=Image.objects.only("image").order_by("order"),
                                to_attr="to_image",
                            )
                        )
                        .prefetch_related(
                            Prefetch(
                                "storage",
                                queryset=Storage.objects.filter(account=my_account),
                            )
                        )
                        .prefetch_related(
                            "like",
                        )
                        .filter(
                            account=account,
                            created_at__lte=created_at,
                        )
                        .only(
                            "fooiyti",
                            "taste_evaluation",
                            "description",
                            "created_at",
                            "account__public_id",
                            "account__nickname",
                            "account__profile_image",
                            "shop__public_id",
                            "shop__name",
                            "shop__address",
                            "menu__name",
                            "menu__price",
                        )
                        .order_by("-created_at")
                    )

            if confirm_pioneer_count:
                request.confirm_pioneer_count = confirm_pioneer_count

            page_feeds = self.paginate_queryset(feeds)
            if resize_type == Common.ImageRizeType.SMALL:
                page_feeds = (
                    confirm_pioneer
                    + FeedsSerializerV2.FeedImageSerializer(page_feeds, many=True).data
                )
            else:
                page_feeds = (
                    confirm_pioneer
                    + FeedsSerializerV2.FeedListSerializer(
                        page_feeds, context={"account": request.account}, many=True
                    ).data
                )
            payload["feed_list"] = self.get_paginated_response(page_feeds)
            payload["feed_list"]["total_count"] += confirm_pioneer_count
            if not page_feeds:
                payload["image"] = Image.objects.get(
                    type=Common.ArchivesImageType.NMF
                ).image.url

            return Response(
                Common.fooiy_standard_response(True, payload),
            )

        except Exception as e:
            return Response(
                Common.fooiy_standard_response(False, 5020, error=e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"])
    @method_decorator(FeedsHelpers.get_feed_from_request(require=False))
    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @method_decorator(Decorators.get_party_from_request())
    def party(self, request):
        """
        # 파티 피드 리스트 API
        """

        _type = request.query_params.get("type", None)
        feed = request.feed
        party = request.party
        account = request.account
        payload = {}

        try:
            if _type not in [Common.FeedListType.IMAGE, Common.FeedListType.LIST]:
                return Response(
                    Common.fooiy_standard_response(
                        False, 4000, api="party_feed_list", type=_type
                    )
                )
            # 이미지 보기
            elif _type == Common.FeedListType.IMAGE:
                resize_type = Common.ImageRizeType.SMALL

                feeds = (
                    Feed.objects.prefetch_related(
                        Prefetch(
                            "image",
                            queryset=Image.objects.only("image").order_by("order"),
                            to_attr="to_image",
                        )
                    )
                    .filter(
                        feed_party__party=party,
                        feed_party__state=Common.PartyState.SUBSCRIBE,
                    )
                    .order_by("-feed_party__created_at")
                )

            # 리스트 보기
            elif _type == Common.FeedListType.LIST:
                if not feed:
                    return Response(
                        Common.fooiy_standard_response(
                            False, 4000, api="party_feed_list", type=_type
                        ),
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    resize_type = Common.ImageRizeType.MEDIUM
                    created_at = FeedParty.objects.get(
                        feed=feed, party=party
                    ).created_at

                    feeds = (
                        Feed.objects.select_related("account", "shop", "menu")
                        .prefetch_related(
                            Prefetch(
                                "image",
                                queryset=Image.objects.only("image").order_by("order"),
                                to_attr="to_image",
                            )
                        )
                        .prefetch_related(
                            Prefetch(
                                "storage",
                                queryset=Storage.objects.filter(account=account),
                            )
                        )
                        .prefetch_related(
                            "like",
                        )
                        .filter(
                            feed_party__created_at__lte=created_at,
                        )
                        .filter(
                            feed_party__party=party,
                            feed_party__state=Common.PartyState.SUBSCRIBE,
                        )
                        .only(
                            "fooiyti",
                            "taste_evaluation",
                            "description",
                            "created_at",
                            "account__public_id",
                            "account__nickname",
                            "account__profile_image",
                            "shop__public_id",
                            "shop__name",
                            "shop__address",
                            "menu__name",
                            "menu__price",
                        )
                        .distinct()
                        .order_by("-feed_party__created_at")
                    )

            page_feeds = self.paginate_queryset(feeds)
            if resize_type == Common.ImageRizeType.SMALL:
                page_feeds = FeedsSerializerV2.FeedImageSerializer(
                    page_feeds, many=True
                ).data
            else:
                page_feeds = FeedsSerializerV2.FeedListSerializer(
                    page_feeds, context={"account": request.account}, many=True
                ).data
            payload["feed_list"] = self.get_paginated_response(page_feeds)
            if not page_feeds:
                payload["image"] = Image.objects.get(
                    type=Common.ArchivesImageType.NMF
                ).image.url

            return Response(
                Common.fooiy_standard_response(True, payload),
            )

        except Exception as e:
            return Response(
                Common.fooiy_standard_response(False, 5071, error=e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @method_decorator(Decorators.get_party_from_request(require=False))
    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @action(detail=False, methods=["get"])
    def map_picker(self, request):
        """
        # 피드 지도 피커 API
        """
        os = request.headers.get("os", None)
        other_account_id = request.query_params.get("other_account_id", None)
        _type = request.query_params.get("type", None)
        party = request.party
        payload = {}

        try:
            if _type not in [Common.FeedDomainType.Mypage, Common.FeedDomainType.Party]:
                return Response(
                    Common.fooiy_standard_response(
                        False, 4000, api="map_picker_api", type=_type
                    )
                )
            feeds = (
                Feed.objects.prefetch_related(
                    Prefetch(
                        "image",
                        queryset=Image.objects.only("image").order_by("order"),
                        to_attr="to_image",
                    )
                )
                .exclude(image__isnull=True)
                .only(
                    "longitude",
                    "latitude",
                    "created_at",
                )
                .order_by("latitude", "longitude", "-created_at")
            )
            if _type == Common.FeedDomainType.Mypage:
                if other_account_id:
                    account = AccountsHelpers.convert_public_id_to_account(
                        other_account_id
                    )
                else:
                    account = request.account

                feeds = feeds.filter(account=account)

            elif _type == Common.FeedDomainType.Party:
                feeds = feeds.filter(
                    feed_party__party=party,
                    feed_party__state=Common.PartyState.SUBSCRIBE,
                )

            if os == "android":
                payload["feed_list"] = FeedsHelpers.get_android_picker(feeds)
            if os == "ios":
                payload["feed_list"] = FeedsHelpers.get_ios_picker(feeds)

            return Response(
                Common.fooiy_standard_response(True, payload),
            )

        except Exception as e:
            return Response(
                Common.fooiy_standard_response(False, 5047, account=account, error=e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @method_decorator(Decorators.get_party_from_request(require=False))
    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @action(detail=False, methods=["get"])
    def map_detail(self, request):
        """
        # 피드 지도 상세 API
        """
        longitude = request.query_params.get("longitude", None)
        latitude = request.query_params.get("latitude", None)
        other_account_id = request.query_params.get("other_account_id", None)
        _type = request.query_params.get("type", None)
        party = request.party
        payload = {}

        try:
            if not (longitude and latitude) or _type not in [
                Common.FeedDomainType.Mypage,
                Common.FeedDomainType.Party,
            ]:
                return Response(
                    Common.fooiy_standard_response(
                        False, 4000, api="map_detail_api", type=_type
                    )
                )
            feeds = Feed.objects.filter(
                longitude=longitude,
                latitude=latitude,
            ).order_by("-created_at")
            if _type == Common.FeedDomainType.Mypage:
                if other_account_id:
                    account = AccountsHelpers.convert_public_id_to_account(
                        other_account_id
                    )
                else:
                    account = request.account
                feeds = feeds.filter(account=account)
            elif _type == Common.FeedDomainType.Party:
                if not party:
                    return Response(Common.fooiy_standard_response(False, 4000))
                feeds = feeds.filter(
                    feed_party__party=party,
                    feed_party__state=Common.PartyState.SUBSCRIBE,
                )

            shops = FeedsHelpers.get_shops_from_feeds(feeds)
            payload["shop_list"] = shops

            return Response(
                Common.fooiy_standard_response(True, payload),
            )

        except Exception as e:
            return Response(
                Common.fooiy_standard_response(False, 5049, account=account, error=e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"])
    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @method_decorator(Decorators.get_party_from_request(require=False))
    @method_decorator(ShopsHelpers.get_shop_from_request())
    def shop(self, request):
        """
        # 매장 피드 리스트 API
        """
        _type = request.query_params.get("type", None)
        other_account_id = request.query_params.get("other_account_id", None)
        party = request.party
        shop = request.shop
        payload = {}
        try:
            account = request.account
        except:
            account = None

        try:
            feeds = (
                Feed.objects.select_related("account", "shop", "menu")
                .prefetch_related(
                    Prefetch(
                        "image",
                        queryset=Image.objects.only("image").order_by("order"),
                        to_attr="to_image",
                    )
                )
                .prefetch_related(
                    Prefetch(
                        "storage",
                        queryset=Storage.objects.filter(account=account),
                    )
                )
                .prefetch_related(
                    "like",
                )
                .filter(shop=shop, is_exposure=True)
                .only(
                    "fooiyti",
                    "taste_evaluation",
                    "description",
                    "created_at",
                    "account__public_id",
                    "account__nickname",
                    "account__profile_image",
                    "shop__public_id",
                    "shop__name",
                    "shop__address",
                    "menu__name",
                    "menu__price",
                )
                .order_by("-created_at")
            )
            if _type == Common.FeedDomainType.Mypage:
                if other_account_id:
                    account = AccountsHelpers.convert_public_id_to_account(
                        other_account_id
                    )
                else:
                    account = request.account
                feeds = feeds.filter(account=account)

            elif _type == Common.FeedDomainType.Party:
                if not party:
                    return Response(Common.fooiy_standard_response(False, 4000))
                feeds = feeds.filter(
                    feed_party__party=party,
                    feed_party__state=Common.PartyState.SUBSCRIBE,
                )

            pagenate_feeds = self.paginate_queryset(feeds)
            pagenate_feeds = FeedsSerializerV2.FeedListSerializer(
                pagenate_feeds, context={"account": request.account}, many=True
            ).data
            payload["feed_list"] = self.get_paginated_response(pagenate_feeds)

            return Response(
                Common.fooiy_standard_response(True, payload),
            )

        except Exception as e:
            return Response(
                Common.fooiy_standard_response(False, 5028, error=e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    def list(self, request):
        """
        # 피드 리스트 API
        """
        category = request.query_params.get("category", None)
        address_depth1 = request.query_params.get("address_depth1", None)
        address_depth2 = request.query_params.get("address_depth2", None)
        payload = {}

        if address_depth2 == "전체":
            address_depth2 = None
        try:
            account = request.account
        except:
            account = None
        try:
            feeds = (
                Feed.objects.select_related("account", "shop", "menu")
                .prefetch_related(
                    Prefetch(
                        "image",
                        queryset=Image.objects.only("image").order_by("order"),
                        to_attr="to_image",
                    )
                )
                .prefetch_related(
                    Prefetch(
                        "storage",
                        queryset=Storage.objects.filter(account=account),
                    )
                )
                .prefetch_related(
                    "like",
                )
                .filter(
                    is_exposure=True,
                    menu__isnull=False,
                    shop__isnull=False,
                )
                .exclude(Q(account__state=Common.AccountState.WITHDRAWAL))
                .only(
                    "fooiyti",
                    "taste_evaluation",
                    "description",
                    "created_at",
                    "account__public_id",
                    "account__nickname",
                    "account__profile_image",
                    "shop__public_id",
                    "shop__name",
                    "shop__address",
                    "menu__name",
                    "menu__price",
                )
                .order_by("-created_at")
            )

            if category == Common.global_variables.category_cafe:
                feeds = feeds.filter(
                    shop__category__name=Common.global_variables.category_cafe
                )
            else:
                feeds = feeds.exclude(
                    Q(shop__category__name=Common.global_variables.category_cafe)
                    | Q(menu__category__in=["BEVERAGE", "LIQUOR"])
                )

            if address_depth1 and address_depth2:
                feeds = feeds.filter(
                    shop__address_depth1=address_depth1,
                    shop__address_depth2=address_depth2,
                )

            elif address_depth1:
                feeds = feeds.filter(
                    shop__address_depth1=address_depth1,
                )

            pagenate_feeds = self.paginate_queryset(feeds)
            if pagenate_feeds:
                pagenate_feeds = FeedsSerializerV2.FeedListSerializer(
                    pagenate_feeds, context={"account": request.account}, many=True
                ).data
                payload["feed_list"] = self.get_paginated_response(pagenate_feeds)
            else:
                payload["image"] = Image.objects.get(
                    type=Common.ArchivesImageType.NSI
                ).image.url

            return Response(
                Common.fooiy_standard_response(True, payload),
            )
        except Exception as e:
            return Response(
                Common.fooiy_standard_response(False, 5029, error=e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @method_decorator(FeedsHelpers.get_feed_from_request())
    @action(detail=False, methods=["patch"])
    def modify(self, request):
        """
        # 피드 수정 API
        """
        feed = request.feed
        description = request.data.get("description", None)
        taste_evaluation = request.data.get("taste_evaluation", 50)
        subscribe_parties = request.data.get("subscribe_parties", None)
        fooiyti_e = request.data.get("fooiyti_e", "50")
        fooiyti_i = request.data.get("fooiyti_i", "50")
        fooiyti_s = request.data.get("fooiyti_s", "50")
        fooiyti_n = request.data.get("fooiyti_n", "50")
        fooiyti_t = request.data.get("fooiyti_t", "50")
        fooiyti_f = request.data.get("fooiyti_f", "50")
        fooiyti_a = request.data.get("fooiyti_a", "50")
        fooiyti_c = request.data.get("fooiyti_c", "50")
        account = request.account
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

        try:
            if account != feed.account:
                return Response(Common.fooiy_standard_response(False, 4303))

            FeedsHelpers.update_feed_parties(feed, subscribe_parties)
            feed_fooiyti = FeedFooiyti.objects.filter(feed=feed)
            if not feed_fooiyti.exists():
                state = Common.FeedUpdateState.REGISTER
            else:
                state = Common.FeedUpdateState.UPDATE

            ShopsTasks.CalculateShopScore.calculate_shop_fooiyti(
                account, feed, fooiyti_list, state
            )
            ShopsTasks.CalculateShopScore.calculate_shop_score(
                feed, taste_evaluation, state
            )

            if state == Common.FeedUpdateState.REGISTER:
                feed_fooiyti = FeedFooiyti.objects.create(
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
            else:
                feed_fooiyti = feed_fooiyti.first()
                feed_fooiyti.fooiyti_e = fooiyti_e
                feed_fooiyti.fooiyti_i = fooiyti_i
                feed_fooiyti.fooiyti_s = fooiyti_s
                feed_fooiyti.fooiyti_n = fooiyti_n
                feed_fooiyti.fooiyti_t = fooiyti_t
                feed_fooiyti.fooiyti_f = fooiyti_f
                feed_fooiyti.fooiyti_a = fooiyti_a
                feed_fooiyti.fooiyti_c = fooiyti_c
                feed_fooiyti.save()

            # 푸이티아이 평가 수정 코드 추가

            if taste_evaluation:
                feed.taste_evaluation = taste_evaluation
            if description:
                feed.description = description

            feed.save(
                update_fields=[
                    "description",
                    "taste_evaluation",
                ]
            )
            return Response(Common.fooiy_standard_response(True))

        except Exception as e:
            return Response(
                Common.fooiy_standard_response(False, 5048, error=e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @method_decorator(FeedsHelpers.get_feed_from_request())
    @action(detail=False, methods=["get"])
    def report(self, request):
        """
        # 피드 신고 API
        """
        feed = request.feed
        account = request.account
        try:
            Common.slack_post_message(
                "#user_report",
                "",
                FeedsHelpers.get_notification_report_feed_attachments(account, feed),
            )

            return Response(Common.fooiy_standard_response(True))

        except Exception as e:
            return Response(
                Common.fooiy_standard_response(
                    False,
                    5072,
                    account=request.account,
                    feed=request.feed,
                    error=e,
                )
            )

    class StorageViewSet(
        mixins.ListModelMixin,
        mixins.UpdateModelMixin,
        GenericViewSet,
    ):
        http_method_names = ["get", "patch"]
        pagination_class = FeedPagination

        @method_decorator(AccountsHelpers.fooiy_account_guard(login=True))
        def list(self, request):
            """
            # 피드 보관 리스트 API
            """
            account = request.account
            address_depth1 = request.query_params.get("address_depth1", None)
            payload = {}

            try:
                storages = (
                    Storage.objects.select_related("feed")
                    .filter(
                        Q(account=account, state=Common.FeedState.SUBSCRIBE)
                        & ~Q(feed__isnull=True)
                        & ~Q(feed__shop__address_depth1__isnull=True)
                    )
                    .order_by("-id")
                )

                if address_depth1:
                    storages = storages.filter(
                        feed__shop__address_depth1=address_depth1
                    )

                pagenate_storages = self.paginate_queryset(storages)

                if pagenate_storages:
                    pagenate_feeds = []
                    for storage in pagenate_storages:
                        pagenate_feeds.append(
                            FeedsSerializerV2.FeedStorageSerializer(storage.feed).data
                        )
                    payload["storage_list"] = self.get_paginated_response(
                        pagenate_feeds
                    )
                else:
                    payload["image"] = Image.objects.get(
                        type=Common.ArchivesImageType.NSF
                    ).image.url

                return Response(Common.fooiy_standard_response(True, payload))

            except Exception as e:
                return Response(
                    Common.fooiy_standard_response(
                        False, 5053, account=account, error=e
                    ),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        @method_decorator(FeedsHelpers.get_feed_from_request())
        @method_decorator(AccountsHelpers.fooiy_account_guard(login=True))
        def patch(self, request):
            """
            # 피드 보관 및 취소 API
            """
            feed = request.feed
            account = request.account
            sender = account
            receiver = feed.account
            try:
                with transaction.atomic():
                    # 구독 및 구독 취소 상태 변경 시
                    storage = Storage.objects.filter(account=account, feed=feed)
                    if storage:
                        storage = storage[0]
                        if storage.state == Common.FeedState.SUBSCRIBE:
                            storage.state = Common.FeedState.UNSUBSCRIBE
                            pushnotifications = PushNotification.objects.filter(
                                feed=feed,
                                sender=account,
                                type=Common.PushNotificationType.STORAGE,
                            )
                            for pushnotification in pushnotifications:
                                pushnotification.delete()
                        else:
                            storage.state = Common.FeedState.SUBSCRIBE
                            ArchivesHelpers.push_notifications(
                                account=account,
                                sender=sender,
                                receiver=receiver,
                                feed=feed,
                                type=Common.PushNotificationType.STORAGE,
                            )

                        storage.save(update_fields=["state"])
                    else:
                        # 보관하지 않았을 때
                        if sender == receiver:
                            Storage.objects.create(account=account, feed=feed)
                        else:
                            Storage.objects.create(account=account, feed=feed)
                            ArchivesHelpers.push_notifications(
                                account=account,
                                sender=sender,
                                receiver=receiver,
                                feed=feed,
                                type=Common.PushNotificationType.STORAGE,
                            )

                    return Response(Common.fooiy_standard_response(True))

            except Exception as e:
                return Response(
                    Common.fooiy_standard_response(
                        False, 5051, account=account, feed=feed, error=e
                    ),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

    class LikeViewSet(
        mixins.ListModelMixin,
        mixins.UpdateModelMixin,
        GenericViewSet,
    ):
        http_method_names = ["patch"]

        @method_decorator(FeedsHelpers.get_feed_from_request())
        @method_decorator(AccountsHelpers.fooiy_account_guard(login=True))
        def patch(self, request):
            """
            # 피드 보관 및 취소 API
            """
            feed = request.feed
            account = request.account
            sender = account
            receiver = feed.account
            try:
                with transaction.atomic():
                    # 구독 및 구독 취소 상태 변경 시
                    like = Like.objects.filter(account=account, feed=feed)
                    if like:
                        like = like[0]
                        if like.state == Common.FeedState.SUBSCRIBE:
                            like.state = Common.FeedState.UNSUBSCRIBE
                            pushnotifications = PushNotification.objects.filter(
                                feed=feed,
                                sender=account,
                                type=Common.PushNotificationType.LIKE,
                            )
                            for pushnotification in pushnotifications:
                                pushnotification.delete()
                        else:
                            like.state = Common.FeedState.SUBSCRIBE
                            ArchivesHelpers.push_notifications(
                                account=account,
                                sender=sender,
                                receiver=receiver,
                                feed=feed,
                                type=Common.PushNotificationType.LIKE,
                            )

                        like.save(update_fields=["state"])
                    else:
                        # 보관하지 않았을 때
                        if sender == receiver:
                            Like.objects.create(account=account, feed=feed)
                        else:
                            Like.objects.create(account=account, feed=feed)
                            ArchivesHelpers.push_notifications(
                                account=account,
                                sender=sender,
                                receiver=receiver,
                                feed=feed,
                                type=Common.PushNotificationType.LIKE,
                            )

                    return Response(Common.fooiy_standard_response(True, ""))

            except Exception as e:
                return Response(
                    Common.fooiy_standard_response(
                        False, 5055, account=account, feed=feed, error=e
                    ),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
