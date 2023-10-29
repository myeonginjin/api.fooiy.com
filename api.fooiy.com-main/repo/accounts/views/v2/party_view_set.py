from django.utils.decorators import method_decorator
from django.db import transaction

from rest_framework import status
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from accounts.helpers import index as AccountsHelpers
from archives.helpers import index as ArchivesHelpers
from common import index as Common
from archives.models import Image
from accounts.models import AccountParty, Party
from feeds.helpers import index as FeedsHelpers
from accounts.serializers.v2 import index as AccountSerializerV2
from accounts.helpers import index as AccountHelpers
from common.utils.decorators import Decorators

from re import fullmatch

import logging

logger = logging.getLogger("api")


class PartyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    http_method_names = ["get", "post", "delete", "patch"]
    queryset = AccountParty.objects.all()

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @method_decorator(FeedsHelpers.get_feed_from_request(require=False))
    def list(self, request):
        """
        # 가입한 파티 리스트
        """
        account = request.account
        feed = request.feed
        payload = {}

        try:
            parties = (
                AccountParty.objects.select_related("party")
                .filter(account=account, state=Common.PartyState.SUBSCRIBE)
                .exclude(party__isnull=True)
                .order_by("-created_at")
            )
            if parties:
                payload["party_list"] = AccountSerializerV2.AccountPartyListSerializer(
                    parties, context={"feed": feed}, many=True
                ).data
            else:
                payload["party_list"] = []

            return Response(Common.fooiy_standard_response(True, payload))
        except Exception as e:
            return Response(Common.fooiy_standard_response(False, 5063, error=e))

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    def create(self, request):
        """
        # 파티 생성 API
        """
        account = request.account
        party_name = request.data.get("party_name", None)
        introduction = request.data.get("introduction", None)
        party_image = request.FILES.get("party_image", None)

        try:
            if not (
                party_name
                and fullmatch(Common.RegEx.NICKNAME, party_name)
                and not (
                    Common.FooiyOfficialAccount.FOOIY_ENGLISH_NICKNAME in party_name
                    or Common.FooiyOfficialAccount.FOOIY_KOREAN_NICKNAME in party_name
                )
            ):
                return Response(
                    Common.fooiy_standard_response(False, 4001),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            with transaction.atomic():
                party = Party.objects.create(
                    owner=account,
                    name=party_name,
                    party_image=party_image,
                    introduction=introduction,
                )
                AccountParty.objects.create(
                    account=account, party=party, state=Common.PartyState.SUBSCRIBE
                )
                party.save()

            return Response(Common.fooiy_standard_response(True))
        except Exception as e:
            return Response(Common.fooiy_standard_response(False, 5064, error=e))

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @method_decorator(Decorators.get_party_from_request())
    @action(detail=False, methods=["get"])
    def info(self, request):
        """
        # 파티 정보 API
        """
        account = request.account
        party = request.party
        payload = {}
        try:
            payload["party_info"] = AccountSerializerV2.PartyInfoSerializer(
                party, context={"account": account}
            ).data

            return Response(Common.fooiy_standard_response(True, payload))
        except Exception as e:
            return Response(Common.fooiy_standard_response(False, 5065, error=e))

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @method_decorator(Decorators.get_party_from_request())
    @action(detail=False, methods=["post"])
    def join(self, request):
        """
        # 파티 가입 API
        """
        account = request.account
        party = request.party
        receiver = party.owner

        try:
            party_state = AccountParty.objects.filter(
                party=party, account=account
            ).first()
            if party_state:
                party_state.state = Common.PartyState.CONFIRM
                party_state.save(update_fields=["state"])
            else:
                AccountParty.objects.create(party=party, account=account)

            # 파티장한테 푸시
            ArchivesHelpers.push_notifications(
                account=account,
                receiver=receiver,
                party=party,
                state=Common.PartyState.CONFIRM,
                type=Common.PushNotificationType.PARTY,
            )
            return Response(Common.fooiy_standard_response(True))
        except Exception as e:
            return Response(Common.fooiy_standard_response(False, 5066, error=e))

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @method_decorator(Decorators.get_party_from_request())
    @action(detail=False, methods=["post"])
    def check_join(self, request):
        """
        # 파티 가입 검수 API
        """
        account = request.account
        party = request.party
        confirm_accounts = request.data.get("confirm_accounts", [])
        confirm = request.data.get("confirm", None)
        try:
            if account != party.owner:
                return Response(Common.fooiy_standard_response(False, 4303))
            if confirm not in [
                Common.PartyState.SUBSCRIBE,
                Common.PartyState.REJECT,
                Common.PartyState.EXPULSION,
            ]:
                return Response(Common.fooiy_standard_response(False, 4000))

            AccountHelpers.update_account_parties(party, confirm_accounts, confirm)

            return Response(Common.fooiy_standard_response(True))
        except Exception as e:
            return Response(Common.fooiy_standard_response(False, 5067, error=e))

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @method_decorator(Decorators.get_party_from_request())
    @action(detail=False, methods=["get"])
    def member_list(self, request):
        """
        # 파티원 정보 API
        """
        party = request.party
        _type = request.query_params.get("type", None)
        payload = {}

        try:
            if _type not in [Common.PartyState.SUBSCRIBE, Common.PartyState.CONFIRM]:
                return Response(Common.fooiy_standard_response(False, 4000))

            party_account = (
                AccountParty.objects.select_related("account")
                .filter(party=party, state=_type)
                .order_by("created_at")
            )

            payload["party_members"] = AccountSerializerV2.AccountPartyMemberSerializer(
                party_account, many=True
            ).data

            return Response(Common.fooiy_standard_response(True, payload))
        except Exception as e:
            return Response(Common.fooiy_standard_response(False, 5068, error=e))

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @method_decorator(Decorators.get_party_from_request())
    def patch(self, request):
        """
        # 파티 정보 변경 API
        """
        party_name = request.data.get("party_name", None)
        introduction = request.data.get("introduction", None)
        party_image = request.FILES.get("party_image", None)
        account = request.account
        party = request.party
        payload = {}

        try:
            if account != party.owner:
                return Response(Common.fooiy_standard_response(False, 4303))

            if party_name:
                if not (
                    fullmatch(Common.RegEx.NICKNAME, party_name)
                    and not (
                        Common.FooiyOfficialAccount.FOOIY_ENGLISH_NICKNAME in party_name
                        or Common.FooiyOfficialAccount.FOOIY_KOREAN_NICKNAME
                        in party_name
                    )
                ):
                    return Response(
                        Common.fooiy_standard_response(False, 4001),
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                party.name = party_name

            if introduction:
                # 띄어쓰기 하나 들어오면 없는것으로 프론트와 합의
                if introduction == " ":
                    party.introduction = None
                else:
                    party.introduction = introduction

            if party_image:
                party.party_image = party_image

            party.save(
                update_fields=[
                    "name",
                    "introduction",
                    "party_image",
                ]
            )

            payload["party_info"] = AccountSerializerV2.PartyInfoSerializer(
                party, context={"account": account}
            ).data

            return Response(Common.fooiy_standard_response(True, payload))

        except Exception as e:
            return Response(Common.fooiy_standard_response(False, 5069, error=e))
