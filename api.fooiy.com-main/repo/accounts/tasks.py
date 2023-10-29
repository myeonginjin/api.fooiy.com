from accounts.models import Account
from common import index as Common
from accounts.helpers import check_rank
from firebase_admin import messaging
from archives.models import PushNotification


def calculate_account_rank_overall():

    try:
        check_rank.CheckRank.create_ranker()

        rankers = Account.objects.filter(
            state=Common.AccountState.NORMAL, rank=Common.RankType.RANKER
        )

        if 10 == rankers.count():
            Common.slack_post_message(
                "dev",
                "def() 'calculate_account_rank_overall' > success",
            )

        else:
            Common.slack_post_message(
                "dev",
                f"def() 'calculate_account_rank_overall' > fail {rankers.count()}",
            )

        accounts = Account.objects.filter(state=Common.AccountState.NORMAL).exclude(
            rank=Common.RankType.RANKER
        )
        for account in accounts:
            rank_criteria = Common.global_variables.rank_criteria

            for rank_type in Common.RankType:
                if rank_type == Common.RankType.RANKER:
                    continue

                if account.feed.count() >= rank_criteria[rank_type]:
                    if account.rank == rank_type:
                        continue

                    elif account.rank != rank_type:

                        account.rank = rank_type

        Account.objects.bulk_update(accounts, ["rank"])

    except Exception as e:
        Common.fooiy_standard_response(
            False, 5555, location="calculate_account_rank_overall error", error=e
        )


def check_account_rank_overall():
    accounts = Account.objects.filter(state=Common.AccountState.NORMAL).exclude(
        rank=Common.RankType.RANKER
    )

    for account in accounts:
        rank_criteria = Common.global_variables.rank_criteria
        if account.rank == Common.RankType.PLATINUM:
            if not account.feed.count() >= rank_criteria[Common.RankType.PLATINUM]:
                Common.slack_post_message(
                    "dev",
                    f"def() 'check_account_rank_overall' > fail {account}",
                )
                check_rank.CheckRank.check_current_rank(account, no_push=True)

        elif account.rank == Common.RankType.GOLD:
            if not account.feed.count() >= rank_criteria[Common.RankType.GOLD]:
                Common.slack_post_message(
                    "dev",
                    f"def() 'check_account_rank_overall' > fail {account}",
                )
                check_rank.CheckRank.check_current_rank(account, no_push=True)

        elif account.rank == Common.RankType.SILVER:
            if not account.feed.count() >= rank_criteria[Common.RankType.SILVER]:
                Common.slack_post_message(
                    "dev",
                    f"def() 'check_account_rank_overall' > fail {account}",
                )
                check_rank.CheckRank.check_current_rank(account, no_push=True)

        elif account.rank == Common.RankType.BRONZE:
            if not account.feed.count() >= rank_criteria[Common.RankType.BRONZE]:
                Common.slack_post_message(
                    "dev",
                    f"def() 'check_account_rank_overall' > fail {account}",
                )
                check_rank.CheckRank.check_current_rank(account, no_push=True)


def overall_pushnotification():
    accounts = Account.objects.filter(state=Common.AccountState.NORMAL)
    title = "🔥 푸이 대규모 업데이트"
    body = "푸이가 새로운 기능과 함께 돌아왔어요. 지금 바로 푸이에서 만나보세요🔥"
    type = Common.PushNotificationType.OVERALL_NOTICE
    account_num = accounts.count()
    message_cnt = 0
    object_cnt = 0
    receiver = account

    try:
        for account in accounts:
            PushNotification.objects.create(
                receiver=receiver,
                type=type,
                title=title,
                content=body,
            )

            if not receiver.fcm_token == "0":
                message = messaging.Message(
                    notification=messaging.Notification(
                        title=title,
                        body=body,
                    ),
                    token=receiver.fcm_token,
                )
                messaging.send(message)

                message_cnt += 1
            object_cnt += 1
        Common.slack_post_message(
            "dev",
            f" 'overall_pushnotification' > success -- account_num :{account_num}, object_cnt : {object_cnt}, message_cnt : {message_cnt}",
        )

    except Exception as e:
        Common.fooiy_standard_response(
            False,
            5555,
            location="overall_pushnotification error",
            error=e,
        )
