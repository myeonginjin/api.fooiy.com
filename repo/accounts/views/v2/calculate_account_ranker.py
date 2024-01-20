from rest_framework.decorators import api_view

from ...models import Account
from common import index as Common
from archives.helpers import index as ArchivesHelpers

from rest_framework.response import Response


@api_view(["GET"])
def calculate_account_ranker(request):
    # ranker_count = 3
    # before_rankers = cache.get(f"accounts:ranker", "")
    # accounts = list(
    #     str(public_id[0])
    #     for public_id in Account.objects.filter(state=Common.AccountState.NORMAL)
    #     .order_by("-pioneer_count", "date_joined")
    #     .values_list("public_id")[:ranker_count]
    # )

    # if accounts != before_rankers and not before_rankers:
    #     # 랭커가 된 사람 푸쉬
    #     for account in accounts:
    #         if account not in before_rankers:
    #             account = Account.objects.get(public_id=account)
    #             ArchivesHelpers.send_push_notifications(
    #                 title=f"🎉{account.nickname}님! 축하드립니다🎉",
    #                 body=f"{Common.RankType.RANKER.upper()} 등급이 되었습니다. 푸이에서 확인해보세요💛",
    #                 receiver=account,
    #             )
    #     # 랭커를 빼앗긴 사람 푸쉬
    #     for before_ranker in before_rankers:
    #         if before_ranker not in accounts:
    #             account = Account.objects.get(public_id=before_ranker)
    #             ArchivesHelpers.send_push_notifications(
    #                 title=f"🙌푸이에서 {account.nickname}님을 기다리고 있어요🙌",
    #                 body=f"개척을 통해 다시 푸이 랭킹에 도전해보세요🔥",
    #                 receiver=account,
    #             )

    # cache.set(
    #     f"accounts:ranker",
    #     accounts,
    #     timeout=None,
    # )

    return Response(
        Common.fooiy_standard_response(
            True,
            {"success"},
        ),
    )
