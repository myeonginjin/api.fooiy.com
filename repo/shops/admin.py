from unicodedata import category
from django.contrib import admin
from .models import Menu
from common import index as Common
from .models import Shop, ShopFooiyti
from .tasks import recalculate_shop_score


class MenuInline(admin.TabularInline):
    model = Menu
    exclude = ["is_best", "is_popular"]


class ShopFooiytiInline(admin.TabularInline):
    model = ShopFooiyti


class ShopAdmin(admin.ModelAdmin):
    search_fields = ["name", "category__name"]
    list_display = ["name", "is_exposure", "address", "created_at", "slug"]
    list_display_links = ["name"]
    ordering = ["-id"]
    raw_id_fields = ["account"]
    filter_horizontal = ("category", "badge")
    inlines = (
        ShopFooiytiInline,
        MenuInline,
    )
    list_per_page = 15
    actions = ["recalculate_shop_score", "recalculate_menu_price"]

    def recalculate_shop_score(modeladmin, request, queryset):
        queryset = Shop.objects.all()
        recalculate_shop_score(queryset)

        ##########################################
        # deprecated shop score algorithm
        ##########################################
        # for shop in list(queryset):
        #     records = Record.objects.filter(
        #         Q(shop=shop)
        #         & (
        #             Q(menu__category=Common.MenuCategory.MAIN)
        #             | Q(menu__category=Common.MenuCategory.SET)
        #         )
        #     ).aggregate(
        #         score=Sum("taste_evaluation"),
        #         count=Count("taste_evaluation"),
        #     )
        #     pioneers = Pioneer.objects.filter(
        #         Q(shop=shop)
        #         & (
        #             Q(menu__category=Common.MenuCategory.MAIN)
        #             | Q(menu__category=Common.MenuCategory.SET)
        #         )
        #     ).aggregate(score=Sum("taste_evaluation"), count=Count("taste_evaluation"))

        #     if records["count"] + pioneers["count"] >= 3:

        #         shop.shopscore.score = (
        #             (records["score"] + pioneers["score"])
        #             // (records["count"] + pioneers["count"])
        #             if records["count"]
        #             else (pioneers["score"]) // (pioneers["count"])
        #         )
        #         shop.shopscore.save()

    recalculate_shop_score.short_description = "(하나만 체크해도 동작)모든 매장의 점수 정보를 재계산합니다."

    def recalculate_menu_price(modeladmin, request, queryset):
        queryset = Shop.objects.all()
        for shop in list(queryset):
            menus = Menu.objects.filter(shop=shop, category=Common.MenuCategory.MAIN)
            min_price, max_price = shop.menu_min_price, shop.menu_min_price
            for menu in menus:
                if menu.price > max_price:
                    max_price = menu.price
                if menu.price < min_price:
                    min_price = menu.price
            if min_price != max_price:
                shop.menu_min_price = min_price
                shop.menu_max_price = max_price
                shop.save()

    recalculate_menu_price.short_description = (
        "(하나만 체크해도 동작)모든 매장의 메뉴 최소, 최대 가격을 재계산합니다."
    )


class ShopCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["id"]
    ordering = ["id"]
    list_per_page = 15


class ShopBadgeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["id"]
    ordering = ["id"]
    list_per_page = 15


class ShopScoreAdmin(admin.ModelAdmin):
    list_display = [
        "shop",
        "score",
        "feed_count",
        "is_yummy",
        "enta_score",
        "entc_score",
        "enfa_score",
        "enfc_score",
        "inta_score",
        "intc_score",
        "infa_score",
        "infc_score",
    ]
    list_display_links = ["shop"]
    ordering = ["-id"]
    list_per_page = 15


class ShopFooiytiAdmin(admin.ModelAdmin):
    list_display = [
        "shop",
        "fooiyti",
        "feed_count",
        "e_percentage",
        "i_percentage",
        "s_percentage",
        "n_percentage",
        "t_percentage",
        "f_percentage",
        "a_percentage",
        "c_percentage",
    ]
    list_display_links = ["shop"]
    raw_id_fields = ["shop"]
    ordering = ["-id"]
    list_per_page = 15


class MenuAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = [
        "name",
        "category",
        "price",
        "shop",
        "is_best",
        "is_popular",
    ]
    list_display_links = ["name"]
    raw_id_fields = ["shop"]
    ordering = ["-id"]
    list_per_page = 15
