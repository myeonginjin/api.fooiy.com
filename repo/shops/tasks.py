from .models import Shop
from common import index as Common
from feeds.models import Feed
from django.db.models.query import QuerySet
from shops.models import Menu
from django.db.models import Q, Avg

fooiyti_score_impact_group: dict = {
    "E": [
        "inta_score",
        "intc_score",
        "infa_score",
        "infc_score",
        "ista_score",
        "istc_score",
        "isfa_score",
        "isfc_score",
    ],
    "I": [
        "enta_score",
        "entc_score",
        "enfa_score",
        "enfc_score",
        "esta_score",
        "estc_score",
        "esfa_score",
        "esfc_score",
    ],
    "S": [
        "enta_score",
        "entc_score",
        "enfa_score",
        "enfc_score",
        "inta_score",
        "intc_score",
        "infa_score",
        "infc_score",
    ],
    "N": [
        "esta_score",
        "estc_score",
        "esfa_score",
        "esfc_score",
        "ista_score",
        "istc_score",
        "isfa_score",
        "isfc_score",
    ],
    "T": [
        "enfa_score",
        "enfc_score",
        "esfa_score",
        "esfc_score",
        "infa_score",
        "infc_score",
        "isfa_score",
        "isfc_score",
    ],
    "F": [
        "enta_score",
        "entc_score",
        "esta_score",
        "estc_score",
        "inta_score",
        "intc_score",
        "ista_score",
        "istc_score",
    ],
}


def fooiyti_scoring(fooiyti: str, taste_evaluation: int) -> dict:
    fooiyti_score: dict = {
        "enta_score": taste_evaluation,
        "entc_score": taste_evaluation,
        "enfa_score": taste_evaluation,
        "enfc_score": taste_evaluation,
        "esta_score": taste_evaluation,
        "estc_score": taste_evaluation,
        "esfa_score": taste_evaluation,
        "esfc_score": taste_evaluation,
        "inta_score": taste_evaluation,
        "intc_score": taste_evaluation,
        "infa_score": taste_evaluation,
        "infc_score": taste_evaluation,
        "ista_score": taste_evaluation,
        "istc_score": taste_evaluation,
        "isfa_score": taste_evaluation,
        "isfc_score": taste_evaluation,
    }

    if taste_evaluation != 50:
        for index, alphabet in enumerate(fooiyti[:3]):
            for fooiyti_score_key in fooiyti_score_impact_group[alphabet]:
                if taste_evaluation == 70 or taste_evaluation == 99:
                    fooiyti_score[fooiyti_score_key] -= (
                        taste_evaluation * (2 ** (3 - index)) // 100
                    )
                else:
                    fooiyti_score[fooiyti_score_key] += (
                        taste_evaluation * (2 ** (3 - index)) // 100
                    )

    return fooiyti_score


def recalculate_shop_score(shops: QuerySet[Shop]):
    for shop in shops:
        try:
            total_fooiyti_score: dict = {
                "enta_score": 0,
                "entc_score": 0,
                "enfa_score": 0,
                "enfc_score": 0,
                "esta_score": 0,
                "estc_score": 0,
                "esfa_score": 0,
                "esfc_score": 0,
                "inta_score": 0,
                "intc_score": 0,
                "infa_score": 0,
                "infc_score": 0,
                "ista_score": 0,
                "istc_score": 0,
                "isfa_score": 0,
                "isfc_score": 0,
            }

            feeds: list = list(Feed.objects.filter(shop=shop))

            for feed in feeds:
                fooiyti_score: dict = fooiyti_scoring(
                    feed.fooiyti, feed.taste_evaluation
                )

                for fooiyti_score_key, fooiyti_score_value in fooiyti_score.items():
                    total_fooiyti_score[fooiyti_score_key] += fooiyti_score_value

            average_score = 0
            is_yummy: bool = True
            for total_fooiyti_score_key in total_fooiyti_score.keys():
                total_fooiyti_score[total_fooiyti_score_key] = round(
                    total_fooiyti_score[total_fooiyti_score_key] / len(feeds)
                )
                setattr(
                    shop.shopscore,
                    total_fooiyti_score_key,
                    total_fooiyti_score[total_fooiyti_score_key],
                )

                average_score += total_fooiyti_score[total_fooiyti_score_key]
                if total_fooiyti_score[total_fooiyti_score_key] < 90:
                    is_yummy = False

            shop.shopscore.score = round(average_score / 16)
            shop.shopscore.feed_count = len(feeds)
            shop.shopscore.is_yummy = is_yummy

            shop.shopscore.save()
        except Exception as e:
            Common.slack_post_message(
                "#log_error",
                f"[매장 점수 재계산 배치 에러] {shop.name}, error : {e}",
            )


class CalculateShopScore:
    @staticmethod
    def calculate_shop_score(
        feed, score=None, FEED_UPDATE_STATE=Common.FeedUpdateState.REGISTER
    ):
        try:
            shop_score = feed.shop.shopscore
            if FEED_UPDATE_STATE == Common.FeedUpdateState.REGISTER:
                shop_score.score = int(
                    (shop_score.score * shop_score.feed_count + int(score))
                    / (shop_score.feed_count + 1)
                )
                shop_score.feed_count += 1
            elif FEED_UPDATE_STATE == Common.FeedUpdateState.UPDATE:
                shop_score.score = int(
                    (
                        shop_score.score * shop_score.feed_count
                        + int(score)
                        - feed.taste_evaluation
                    )
                    / (shop_score.feed_count)
                )
            else:
                shop_score.score = int(
                    (shop_score.score * shop_score.feed_count - feed.taste_evaluation)
                    / (shop_score.feed_count - 1)
                )
                shop_score.feed_count -= 1
            shop_score.save(update_fields=["score", "feed_count"])
        except Exception as e:
            Common.fooiy_standard_response(
                False,
                5555,
                location="calculate_shop_score error",
                type=FEED_UPDATE_STATE,
                error=e,
            )

    @staticmethod
    def calculate_percentage(fooiyti):
        fooiyti_percente_1 = int(fooiyti[1] / (fooiyti[0] + fooiyti[1]) * 100)
        return 100 - fooiyti_percente_1, fooiyti_percente_1

    @staticmethod
    def calculate_fooiyti_score(account, fooiyti_list):
        account_fooiyti = str(account.fooiyti).lower()
        fooiyti_order = Common.global_variables.FOOIYTI_ORDER.lower()
        fooiyti_length = len(account_fooiyti)
        results = {}

        def each_my_fooiyti(index):
            return getattr(account, f"fooiyti_{fooiyti_order[index]}_percentage")

        for index in range(fooiyti_length):
            if fooiyti_order[index * 2] == account_fooiyti[index]:
                current_my_index = index * 2
                contract_my_index = index * 2 + 1
            else:
                current_my_index = index * 2 + 1
                contract_my_index = index * 2

            # 내 푸이티아이와 같은 푸이티아이 평가를 선택했을 때
            if (
                fooiyti_list[fooiyti_order[current_my_index]]
                >= fooiyti_list[fooiyti_order[contract_my_index]]
            ):
                results[fooiyti_order[current_my_index]] = fooiyti_list[
                    fooiyti_order[current_my_index]
                ] * each_my_fooiyti(current_my_index)
                results[fooiyti_order[contract_my_index]] = fooiyti_list[
                    fooiyti_order[contract_my_index]
                ] * each_my_fooiyti(contract_my_index)
                (
                    results[fooiyti_order[current_my_index]],
                    results[fooiyti_order[contract_my_index]],
                ) = CalculateShopScore.calculate_percentage(
                    [
                        results[fooiyti_order[current_my_index]],
                        results[fooiyti_order[contract_my_index]],
                    ]
                )
            # 내 푸이티아이와 반대의 푸이티아이 평가를 선택했을 때
            else:
                results[fooiyti_order[current_my_index]] = fooiyti_list[
                    fooiyti_order[current_my_index]
                ]
                results[fooiyti_order[contract_my_index]] = fooiyti_list[
                    fooiyti_order[contract_my_index]
                ]
        return results

    @staticmethod
    def calculate_shop_fooiyti(
        account,
        feed,
        fooiyti_list=None,
        FEED_UPDATE_STATE=Common.FeedUpdateState.REGISTER,
    ):
        try:
            shop = feed.shop
            shop_fooiyti = shop.shopfooiyti
            current_feed_count = shop_fooiyti.feed_count
            if FEED_UPDATE_STATE == Common.FeedUpdateState.REGISTER:
                fooiyti_score = CalculateShopScore.calculate_fooiyti_score(
                    account, fooiyti_list
                )
                shop_fooiyti.feed_count += 1

            else:
                before_score = CalculateShopScore.calculate_fooiyti_score(
                    account,
                    {
                        "e": feed.feedfooiyti.fooiyti_e,
                        "i": feed.feedfooiyti.fooiyti_i,
                        "s": feed.feedfooiyti.fooiyti_s,
                        "n": feed.feedfooiyti.fooiyti_n,
                        "t": feed.feedfooiyti.fooiyti_t,
                        "f": feed.feedfooiyti.fooiyti_f,
                        "a": feed.feedfooiyti.fooiyti_a,
                        "c": feed.feedfooiyti.fooiyti_c,
                    },
                )
                if FEED_UPDATE_STATE == Common.FeedUpdateState.UPDATE:
                    after_score = CalculateShopScore.calculate_fooiyti_score(
                        account, fooiyti_list
                    )
                    fooiyti_score = {
                        "e": after_score["e"] - before_score["e"],
                        "i": after_score["i"] - before_score["i"],
                        "s": after_score["s"] - before_score["s"],
                        "n": after_score["n"] - before_score["n"],
                        "t": after_score["t"] - before_score["t"],
                        "f": after_score["f"] - before_score["f"],
                        "a": after_score["a"] - before_score["a"],
                        "c": after_score["c"] - before_score["c"],
                    }
                else:
                    fooiyti_score = {
                        "e": -before_score["e"],
                        "i": -before_score["i"],
                        "s": -before_score["s"],
                        "n": -before_score["n"],
                        "t": -before_score["t"],
                        "f": -before_score["f"],
                        "a": -before_score["a"],
                        "c": -before_score["c"],
                    }
                    shop_fooiyti.feed_count -= 1

            fooiyti_score = {
                "e": shop_fooiyti.e_percentage * current_feed_count
                + fooiyti_score["e"],
                "i": shop_fooiyti.i_percentage * current_feed_count
                + fooiyti_score["i"],
                "s": shop_fooiyti.s_percentage * current_feed_count
                + fooiyti_score["s"],
                "n": shop_fooiyti.n_percentage * current_feed_count
                + fooiyti_score["n"],
                "t": shop_fooiyti.t_percentage * current_feed_count
                + fooiyti_score["t"],
                "f": shop_fooiyti.f_percentage * current_feed_count
                + fooiyti_score["f"],
                "a": shop_fooiyti.a_percentage * current_feed_count
                + fooiyti_score["a"],
                "c": shop_fooiyti.c_percentage * current_feed_count
                + fooiyti_score["c"],
            }

            (
                shop_fooiyti.e_percentage,
                shop_fooiyti.i_percentage,
            ) = CalculateShopScore.calculate_percentage(
                [fooiyti_score["e"], fooiyti_score["i"]]
            )
            (
                shop_fooiyti.s_percentage,
                shop_fooiyti.n_percentage,
            ) = CalculateShopScore.calculate_percentage(
                [fooiyti_score["s"], fooiyti_score["n"]]
            )
            (
                shop_fooiyti.t_percentage,
                shop_fooiyti.f_percentage,
            ) = CalculateShopScore.calculate_percentage(
                [fooiyti_score["t"], fooiyti_score["f"]]
            )
            (
                shop_fooiyti.a_percentage,
                shop_fooiyti.c_percentage,
            ) = CalculateShopScore.calculate_percentage(
                [fooiyti_score["a"], fooiyti_score["c"]]
            )

            fooiyti = ""
            fooiyti += (
                "E" if shop_fooiyti.e_percentage >= shop_fooiyti.i_percentage else "I"
            )
            fooiyti += (
                "S" if shop_fooiyti.s_percentage >= shop_fooiyti.n_percentage else "N"
            )
            fooiyti += (
                "T" if shop_fooiyti.t_percentage >= shop_fooiyti.f_percentage else "F"
            )
            fooiyti += (
                "A" if shop_fooiyti.a_percentage >= shop_fooiyti.c_percentage else "C"
            )
            if shop_fooiyti.fooiyti != fooiyti:
                shop_fooiyti.fooiyti = fooiyti

            shop_fooiyti.save(
                update_fields=[
                    "feed_count",
                    "fooiyti",
                    "e_percentage",
                    "i_percentage",
                    "n_percentage",
                    "s_percentage",
                    "t_percentage",
                    "f_percentage",
                    "c_percentage",
                    "a_percentage",
                ]
            )
        except Exception as e:
            Common.fooiy_standard_response(
                False,
                5555,
                location="calculate_shop_fooiyti error",
                type=FEED_UPDATE_STATE,
                error=e,
            )


def change_menu_type():
    menus = Menu.objects.filter(
        Q(is_best=True)
        | Q(is_popular=True)
        | Q(is_best__isnull=True)
        | Q(is_popular__isnull=True)
    )

    for menu in menus:
        menu.is_best = False
        menu.is_popular = False

    Menu.objects.bulk_update(menus, ["is_best", "is_popular"])

    try:
        menus = Menu.objects.filter(
            Q(is_best=True)
            | Q(is_popular=True)
            | Q(is_best__isnull=True)
            | Q(is_popular__isnull=True)
        )

        if menus.exists() == False:
            Common.slack_post_message(
                "dev",
                "def() 'change_menu_type' > success",
            )

    except Exception as e:
        Common.fooiy_standard_response(
            False, 5555, location="change_menu_type error", error=e
        )


def change_cafe_menu_type():

    try:
        menus = Menu.objects.filter(shop__category__name="BAKERY/CAFE").exclude(
            Q(category="BEVERAGE") | Q(category="LIQUOR") | Q(category="MAIN")
        )
        if not menus:
            Common.slack_post_message(
                "dev",
                f" 'change_cafe_menu_type' > no exist menus",
            )

        if menus:
            for menu in menus:
                menu.category = Common.MenuCategory.MAIN

            Menu.objects.bulk_update(menus, ["category"])

        menus = Menu.objects.filter(shop__category__name="BAKERY/CAFE").exclude(
            Q(category="BEVERAGE") | Q(category="LIQUOR") | Q(category="MAIN")
        )

        if not menus:
            Common.slack_post_message(
                "dev",
                " 'change_cafe_menu_type' > success",
            )

        if menus:
            Common.slack_post_message(
                "dev",
                f"{menus} 'change_cafe_menu_type' > fail",
            )

    except Exception as e:
        Common.fooiy_standard_response(
            False, menus, 5555, location="change_cafe_menu_type error", error=e
        )


def calculate_shop_score_overall():

    try:

        shops = Shop.objects.all()

        for shop in shops:
            dic = Feed.objects.filter(shop=shop).aggregate(
                average_score=Avg("taste_evaluation")
            )

            if dic["average_score"]:
                score = int(dic["average_score"])
                shop.shopscore.score = score

            if not dic["average_score"]:
                score = 50
                shop.shopscore.score = score

        shop.shopscore.save(update_fields=["score"])

    except Exception as e:
        Common.fooiy_standard_response(
            False,
            5555,
            shop,
            dic,
            score,
            location="calculate_shop_score_overall error",
            error=e,
        )


def check_shop_score_overall():
    try:
        shops = Shop.objects.all()
        overall_cnt = 0
        nomal_shop_cnt = 0
        strange_shop_cnt = 0
        for shop in shops:
            score = shop.shopscore.score
            if score > 100:
                Common.slack_post_message(
                    "dev",
                    f" 'check_shop_score_overall'  {shop.name},{shop.shopscore.score}",
                )
                strange_shop_cnt += 1

            else:
                nomal_shop_cnt += 1

            overall_cnt += 1

        Common.slack_post_message(
            "dev",
            f" 'check_shop_score_overall' > success cnt :{overall_cnt}, strange_shop_cnt : {strange_shop_cnt}, nomal_shop_cnt : {nomal_shop_cnt}",
        )

    except Exception as e:
        Common.fooiy_standard_response(
            False,
            5555,
            shop,
            overall_cnt,
            strange_shop_cnt,
            location="calculate_shop_score_overall error",
            error=e,
        )
