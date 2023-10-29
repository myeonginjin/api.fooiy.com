from shops.serializers.v2 import index as ShopsSerailizerV2
from common import index as Common


def make_a_menu(menus, shop_category=None):
    result = {}

    common_order_a_menu = [
        Common.MenuCategory.MAIN,
        Common.MenuCategory.SET,
        Common.MenuCategory.SIDE,
        Common.MenuCategory.BEVERAGE,
        Common.MenuCategory.LIQUOR,
        None,
    ]

    cafe_order_a_menu = [
        Common.MenuCategory.BEVERAGE,
        Common.MenuCategory.LIQUOR,
        Common.MenuCategory.MAIN,
    ]

    pub_order_a_menu = [
        Common.MenuCategory.MAIN,
        Common.MenuCategory.SET,
        Common.MenuCategory.SIDE,
        Common.MenuCategory.LIQUOR,
        Common.MenuCategory.BEVERAGE,
    ]

    if shop_category == Common.ShopMainCategory.CAFE:
        order_a_menu = cafe_order_a_menu
    elif shop_category == Common.ShopMainCategory.PUB:
        order_a_menu = pub_order_a_menu
    else:
        order_a_menu = common_order_a_menu

    for menu_category in order_a_menu:
        result[menu_category] = ShopsSerailizerV2.MenuListSerializer(
            menus.filter(category=menu_category).exclude(category__isnull=True),
            many=True,
        ).data

    return result
