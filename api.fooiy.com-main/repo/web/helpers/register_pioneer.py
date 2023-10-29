from django.db import transaction
from common import index as Common
from shops.helpers import index as ShopsHelpers
from shops.models import Shop, Menu, ShopScore, ShopFooiyti
from .feed_register import shop_category_register


def register_pioneer(
    pioneer,
    shop_name,
    address,
    menu_name,
    menu_price,
    menu_category,
    category1,
    category2,
    category3,
    _type,
):
    menu = None
    shop = Shop.objects.filter(
        slug=ShopsHelpers.get_shop_slug(name=shop_name, address=address)
    )
    # 매장이 존재
    with transaction.atomic():
        if shop.exists() or pioneer.shop:
            shop = shop.first() if shop.exists() else pioneer.shop
            trimed_menu_name = menu_name.replace(" ", "")
            menus = Menu.objects.filter(shop=shop)
            # 메뉴 개척되어있는지 확인
            for exist_menu in menus:
                if trimed_menu_name == exist_menu.name.replace(" ", ""):
                    menu = exist_menu
                    break
        else:
            # 타입이 카페 혹은 주점이면 카테고리 자동 설정
            if _type != Common.ShopMainCategory.COMMON:
                category1, category2, category3 = _type, None, None
            shop = Shop.objects.create(
                account=pioneer.account,
                menu_min_price=menu_price,
                name=shop_name,
                address=address,
                thumbnail=pioneer.image_1,
            )
            ShopScore.objects.create(shop=shop, score=0)
            ShopFooiyti.objects.create(shop=shop)
            shop_category_register(shop, [category1, category2, category3])

        if not menu:
            menu = Menu.objects.create(
                shop=shop,
                name=menu_name,
                price=menu_price,
                category=menu_category,
            )

        # 추가로 개척 정보에 담아줘야하는 것들
        pioneer.shop = shop
        pioneer.menu = menu
        pioneer.category1 = category1
        pioneer.category2 = category2
        pioneer.category3 = category3
        pioneer.menu_category = menu_category
        pioneer.state = Common.PioneerState.SUCCESS
        pioneer.save(
            update_fields=[
                "shop",
                "menu",
                "category1",
                "category2",
                "category3",
                "menu_category",
                "state",
            ]
        )

    return pioneer
