from django.http import JsonResponse
from django.db.models import Q

from rest_framework.decorators import api_view
from datetime import date, timedelta

from fooiy.settings import DEBUG
from common import index as Common
from feeds.models import Pioneer
from accounts.models import Account
from feeds.models import Record
from shops.models import Shop
from ...models import Fooiyti


@api_view(["POST"])
def pioneer_status(request):
    """
    # 개척 현황 슬랙 커맨드
    """
    pionners = Pioneer.objects.all()
    today_pioneers = pionners.filter(created_at__gte=date.today())
    confirming_pioneers = pionners.filter(
        Q(state=Common.PioneerState.CONFIRM) | Q(state=Common.PioneerState.ERROR)
    ).order_by("created_at")

    confirming_list_first = []
    for confirming_pioneer in confirming_pioneers[:10]:
        confirming_list_first.append(
            {
                "type": "mrkdwn",
                "text": f"<http://dev-api.fooiy.com/admin-fooiy/feeds/pioneer/{confirming_pioneer.id}/change/|{confirming_pioneer.shop_name}({confirming_pioneer.menu_name})>"
                if DEBUG
                else f"<https://fooiy.com/pioneer-check/{confirming_pioneer.id}|{confirming_pioneer.shop_name}({confirming_pioneer.menu_name})>",
            }
        )

    confirming_list_second = []
    for confirming_pioneer in confirming_pioneers[10:20]:
        confirming_list_second.append(
            {
                "type": "mrkdwn",
                "text": f"<http://dev-api.fooiy.com/admin-fooiy/feeds/pioneer/{confirming_pioneer.id}/change/|{confirming_pioneer.shop_name}({confirming_pioneer.menu_name})>"
                if DEBUG
                else f"<https://fooiy.com/pioneer-check/{confirming_pioneer.id}|{confirming_pioneer.shop_name}({confirming_pioneer.menu_name})>",
            }
        )

    blocks = {
        "response_type": "in_channel",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*[✅ 개척 현황]*\n오늘 총 개척 {today_pioneers.count()}건, 성공 {today_pioneers.filter(state=Common.PioneerState.SUCCESS).count()}건, 반려 {today_pioneers.filter(state=Common.PioneerState.REJECT).count()}건, 에러 {today_pioneers.filter(state=Common.PioneerState.ERROR).count()}건",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"🚨 검수 진행중 : {confirming_pioneers.count()}건",
                },
            },
            {"type": "divider"},
        ],
    }

    if confirming_list_first:
        blocks["blocks"].append({"type": "section", "fields": confirming_list_first})

    if confirming_list_second:
        blocks["blocks"].append({"type": "section", "fields": confirming_list_second})

    return JsonResponse(blocks, safe=False)


@api_view(["POST"])
def kpi(request):
    """
    # KPI 슬랙 커맨드
    """

    yesterday = (date.today() - timedelta(days=1), date.today())

    yesterday_accounts = Account.objects.filter(
        date_joined__range=yesterday, state=Common.AccountState.NORMAL
    )
    kakao_accounts = yesterday_accounts.filter(social_type="kakao")
    apple_accounts = yesterday_accounts.filter(social_type="apple")

    yesterday_pioneers = Pioneer.objects.filter(created_at__range=yesterday)
    success_pioneers = yesterday_pioneers.filter(state=Common.PioneerState.SUCCESS)
    reject_pioneers = yesterday_pioneers.filter(state=Common.PioneerState.REJECT)

    yesterday_records = Record.objects.filter(created_at__range=yesterday)

    yesterday_shops = Shop.objects.filter(created_at__range=yesterday)

    blocks = {
        "response_type": "in_channel",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*[📈 {str(date.today() - timedelta(days=1))} 일간 KPI]*",
                },
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"🅺 Kakao 회원가입 : {kakao_accounts.count()}건",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"🅰️ Apple 회원가입 : {apple_accounts.count()}건",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"🥳 개척 성공 : {success_pioneers.count()}건",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"😫 개척 반려 : {reject_pioneers.count()}건",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"📖 일간 기록 : {yesterday_records.count()}건",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"🏪 일간 등록 매장 : {yesterday_shops.count()}건",
                },
            },
        ],
    }

    return JsonResponse(blocks, safe=False)


@api_view(["POST"])
def fooiyti_ratio(request):
    """
    # 푸이티아이 비율 슬랙 커맨드
    """

    fooiyti_infos = Fooiyti.objects.all()

    accounts = Account.objects.filter(state=Common.AccountState.NORMAL)
    accounts_count = accounts.count()

    blocks = {
        "response_type": "in_channel",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*[👨‍👩‍👧‍👦 푸이티아이 비율]*\n전체 회원 : {accounts_count}명",
                },
            },
            {"type": "divider"},
        ],
    }

    for fooiyti_info in fooiyti_infos:
        fooiyti_accounts = accounts.filter(fooiyti=fooiyti_info)
        fooiyti_accounts_count = fooiyti_accounts.count()

        blocks["blocks"].append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{fooiyti_info.fooiyti} ({fooiyti_info.nickname}) : {fooiyti_accounts_count}명({round((fooiyti_accounts_count / accounts_count) * 100, 2)}%)",
                },
            },
        )

    return JsonResponse(blocks, safe=False)
