from common import index as Common


def get_shops_from_feeds(feeds):
    shops = []
    check_shop = []
    for feed in feeds:
        if feed.shop.public_id not in check_shop:
            shop = feed.shop
            check_shop.append(shop.public_id)
            shops.append(
                {
                    "public_id": shop.public_id,
                    "image": feed.image.filter(order=0)[0].image.url,
                    "feed_count": feeds.filter(shop=shop).count(),
                    "shop_name": shop.name,
                    "menu_price": f"{shop.menu_min_price:,}원~{shop.menu_max_price:,}원"
                    if shop.menu_max_price
                    else f"{shop.menu_min_price:,}원",
                    "category_list": [
                        Common.global_variables.shop_category_dict[category.name]
                        for category in shop.category.all()
                    ],
                    "address": shop.address,
                }
            )

    return shops
