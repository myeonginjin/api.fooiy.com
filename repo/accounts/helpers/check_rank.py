from django.db.models import Count, OuterRef, Subquery
from common import index as Common
from archives.helpers import index as ArchivesHelpers
from accounts.models import Account
from feeds.models import Feed
from archives.models import Image


class CheckRank:
    RANKER_ACCOUNT_NUMBER = 10

    @staticmethod
    def check_change_rank(account, type=None):
        ### 개척 기록 시 랭크 변동 체크 ###
        try:
            if type == Common.CheckChangeRankType.REGISTRATION:
                if (
                    account.feed.count() >= CheckRank.get_ranker().last().count
                    and not account.rank == Common.RankType.RANKER
                ):
                    dropped_ranker = CheckRank.get_ranker().last()
                    account.rank = Common.RankType.RANKER
                    account.save()

                    ### account -> ranker된 사람
                    Common.slack_post_message(
                        "dev", f"{account} 이 사람 랭커됨 : {account.feed.count()}"
                    )

                    ArchivesHelpers.push_notifications(
                        account=account,
                        receiver=account,
                        image=Image.objects.get(type="RI", order=0).image,
                        type=Common.PushNotificationType.RANK,
                    )

                    ### dropped_ranker -> ranker 떨어진 사람 푸시 추가
                    Common.slack_post_message(
                        "dev",
                        f"{dropped_ranker} 이 사람 랭커 떨어짐 : {dropped_ranker.feed.count()}",
                    )

                    ArchivesHelpers.push_notifications(
                        account=dropped_ranker,  # 딥링크를 위해 지우면 안됨
                        dropped_ranker=dropped_ranker,
                        receiver=dropped_ranker,
                        image=Image.objects.get(type="RI", order=5).image,
                        type=Common.PushNotificationType.RANK,
                    )

                    CheckRank.check_current_rank(dropped_ranker, True)
                elif not account.rank == Common.RankType.RANKER:
                    CheckRank.check_current_rank(account)

            elif type == Common.CheckChangeRankType.DEMOTION:

                new_ranker = CheckRank.get_new_ranker().first()

                if account.feed.count() < new_ranker.count:

                    CheckRank.check_current_rank(account, True)

                    ArchivesHelpers.push_notifications(
                        account=account,  # 딥링크를 위해 지우면 안됨
                        dropped_ranker=account,
                        receiver=account,
                        image=Image.objects.get(type="RI", order=5).image,
                        type=Common.PushNotificationType.RANK,
                    )

                    new_ranker.rank = Common.RankType.RANKER
                    new_ranker.save()

                    ArchivesHelpers.push_notifications(
                        account=new_ranker,
                        receiver=new_ranker,
                        image=Image.objects.get(type="RI", order=0).image,
                        type=Common.PushNotificationType.RANK,
                    )

        except Exception as e:
            Common.fooiy_standard_response(
                False, 5555, location="check_change_rank error", error=e
            )

    @staticmethod
    def check_current_rank(account, no_push=False):
        try:
            rank_criteria = Common.global_variables.rank_criteria
            order = 0
            if (
                account.feed.count()
                < Common.global_variables.rank_criteria[Common.RankType.BRONZE]
            ):
                account.rank = None
                account.save()
                return
            for rank_type in Common.RankType:
                if rank_type == Common.RankType.RANKER:
                    continue

                order += 1
                if account.feed.count() >= rank_criteria[rank_type]:
                    if account.rank == rank_type:
                        return

                    elif account.rank != rank_type:

                        account.rank = rank_type
                        account.save()
                        if no_push:
                            return

                        ### account 랭크 올랐다고 push 알림
                        Common.slack_post_message(
                            "dev",
                            f"{account} 그냥 랭크 오름 : {account.feed.count()} : {account.rank}",
                        )

                        ArchivesHelpers.push_notifications(
                            account=account,
                            dropped_ranker=None,
                            rank_type=account.rank,
                            receiver=account,
                            image=Image.objects.get(type="RI", order=order).image,
                            type=Common.PushNotificationType.RANK,
                        )

                        return

        except Exception as e:
            Common.fooiy_standard_response(
                False, 5555, location="check_ranker error", error=e
            )

    @staticmethod
    def get_ranker():
        return (
            Account.objects.annotate(count=Count("feed"))
            .filter(rank=Common.RankType.RANKER)
            .order_by("-count")
        )

    @staticmethod
    def get_new_ranker():
        return (
            Account.objects.annotate(count=Count("feed"))
            .filter(state=Common.AccountState.NORMAL)
            .exclude(rank=Common.RankType.RANKER)
            .order_by("-count")
        )

    @staticmethod
    def create_ranker():
        feeds = Feed.objects.filter(account=OuterRef("pk"))

        accounts = (
            Account.objects.annotate(count=Count("feed"))
            .annotate(
                created_at=Subquery(
                    feeds.order_by("-created_at").values("created_at")[:1]
                )
            )
            .filter(state="normal")
            .order_by("-count", "-created_at")
        )[:10]

        for account in accounts:
            account.rank = Common.RankType.RANKER

        Account.objects.bulk_update(accounts, ["rank"])
