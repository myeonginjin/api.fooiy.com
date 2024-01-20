from django.db import transaction

from rest_framework import status
from rest_framework.response import Response

from common import index as Common
from archives.models import Image
from shops.models import ShopCategory
from feeds.models import Feed, FeedFooiyti
from feeds.helpers import index as FeedsHelpers
from archives.helpers import index as ArchivesHelpers
from shops import tasks as ShopsTasks


def shop_category_register(shop, categorys):
    try:
        for category in categorys:
            if category:
                shop_category = ShopCategory.objects.get(name=category)
                shop.category.add(shop_category)
        shop.save()
    except Exception as e:
        return Response(
            Common.fooiy_standard_response(False, 5003, error=e),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def feed_register(pioneer):
    try:
        with transaction.atomic():
            feed = Feed.objects.create(
                account=pioneer.account,
                fooiyti=pioneer.account.fooiyti,
                shop=pioneer.shop,
                menu=pioneer.menu,
                description=pioneer.comment,
                taste_evaluation=pioneer.taste_evaluation,
            )
            feed_fooiyti = FeedFooiyti.objects.create(
                feed=feed,
                fooiyti_e=pioneer.fooiyti_e,
                fooiyti_i=pioneer.fooiyti_i,
                fooiyti_s=pioneer.fooiyti_s,
                fooiyti_n=pioneer.fooiyti_n,
                fooiyti_t=pioneer.fooiyti_t,
                fooiyti_f=pioneer.fooiyti_f,
                fooiyti_a=pioneer.fooiyti_a,
                fooiyti_c=pioneer.fooiyti_c,
            )

            Image.objects.bulk_create(
                Image(
                    order=index,
                    type=Common.ArchivesImageType.F,
                    feed=feed,
                    menu=pioneer.menu,
                    image=image,
                    shop=pioneer.shop,
                    account=pioneer.account,
                )
                for index, image in enumerate(
                    Common.create_image_list(
                        pioneer.image_1,
                        pioneer.image_2,
                        pioneer.image_3,
                    )
                )
            )

            fooiyti_list = fooiyti_list = {
                "e": feed_fooiyti.fooiyti_e,
                "i": feed_fooiyti.fooiyti_i,
                "s": feed_fooiyti.fooiyti_s,
                "n": feed_fooiyti.fooiyti_n,
                "t": feed_fooiyti.fooiyti_t,
                "f": feed_fooiyti.fooiyti_f,
                "a": feed_fooiyti.fooiyti_a,
                "c": feed_fooiyti.fooiyti_c,
            }

            ShopsTasks.CalculateShopScore.calculate_shop_fooiyti(
                feed.account, feed, fooiyti_list, Common.FeedUpdateState.REGISTER
            )
            ShopsTasks.CalculateShopScore.calculate_shop_score(
                feed, feed.taste_evaluation, Common.FeedUpdateState.REGISTER
            )

        FeedsHelpers.update_feed_parties(feed, pioneer.subscribe_party)
        #### 개척 성공 푸시 발송 로직 ####
        ArchivesHelpers.push_notifications(
            pioneer=pioneer,
            receiver=pioneer.account,
            feed=feed,
            type=Common.PushNotificationType.PIONEER_SUCCESS,
        )

        Common.slack_post_message(
            "#request_pioneer",
            f"*[🎉 [{feed.shop.name}] {feed.menu.name} 개척 성공 🎉]*\n*개척자* : {pioneer.account}",
            FeedsHelpers.get_request_menu_slack_attachments(pioneer),
        )

        return True
    except Exception as e:
        pioneer.state = Common.PioneerState.ERROR
        pioneer.error_message = str(e)
        pioneer.save(update_fields=["state", "error_message"])

        return Response(
            Common.fooiy_standard_response(
                False, 5002, id=pioneer.id, shop=pioneer.shop_name, error=e
            ),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
