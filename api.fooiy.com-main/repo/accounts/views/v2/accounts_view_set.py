from django.utils import timezone
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from fooiy import env
from accounts.helpers import index as AccountsHelpers
from common import index as Common
from archives.models import Image, Fooiyti
from ...models import Account
from ...serializers.v2 import index as AccountSerializerV2
from ...helpers import index as AccountHelpers

from re import fullmatch

import logging

logger = logging.getLogger("api")


class AccountPagination(Common.FooiyPagenation):
    default_limit = 500


class AccountsViewSet(mixins.DestroyModelMixin, GenericViewSet):
    """
    # 계정관련 뷰셋
    ---
    - accounts/logout (post) : 로그아웃 API
    - accounts/ (delete) : 회원 탈퇴 API
    - accounts/profile/ (patch) : 프로필 변경 API
    - accounts/info (get) : 계정 정보 API
    - accounts/ranking (get) : 계정 랭킹 API
    """

    queryset = Account.objects.all()
    serializer_class = AccountSerializerV2.AccountDetailSerializer
    http_method_names = ["get", "post", "delete", "patch"]
    pagination_class = AccountPagination

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @action(detail=False, methods=["post"])
    def logout(self, request):
        """
        # 로그아웃 API
        ---
        - ## header
            - ### Authorization : 푸이 계정 토큰
            - ### os : os
            - ### device-id : device uuid
        """
        account = request.account

        try:
            account.is_active = False

            account.save(update_fields=["is_active"])

            Common.slack_post_message(
                "#notify_account",
                f"[👋 *푸이 로그아웃* 👟]\n닉네임 : {account.nickname}, 소셜 타입 : {account.social_type}, OS : {account.os}, app_version : {account.app_version}",
            )

            return Response(
                Common.fooiy_standard_response(
                    True,
                ),
            )
        except Exception as e:
            return Response(
                Common.fooiy_standard_response(
                    False, 5005, account_id=account.id, error=e
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    def destroy(self, request, pk=None):
        """
        # 회원 탈퇴 API
        ---
        - ## header
            - ### Authorization : 푸이 계정 토큰
            - ### os : os
            - ### device-id : device uuid
        - ## path
            - ### public_id : 탈퇴할 계정 public_id
        - ## query-params
            - ### reason : 탈퇴 이유
        """
        reason = request.query_params.get("reason", None)

        try:
            account = request.account
            nickname = account.nickname
            social_type = account.social_type
            os = account.os
            app_version = account.app_version

            account.phone_number = None
            account.email = None
            account.nickname = None
            account.social_type = None
            account.social_id = None
            account.account_token = None
            account.state = Common.AccountState.WITHDRAWAL
            account.withdrawal_reason = reason
            account.date_withdrawal = timezone.now()
            account.is_active = False
            account.fcm_token = None

            try:
                account.profile_image = Image.objects.get(type="DPI").image
            except Exception as e:
                return Response(
                    Common.fooiy_standard_response(
                        False, 5044, account_id=account.id, reason=reason, error=e
                    ),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            account.save(
                update_fields=[
                    "phone_number",
                    "email",
                    "nickname",
                    "social_type",
                    "social_id",
                    "account_token",
                    "state",
                    "withdrawal_reason",
                    "date_withdrawal",
                    "is_active",
                    "profile_image",
                    "fcm_token",
                ]
            )

            Common.slack_post_message(
                "#notify_account",
                f"[✈️ *푸이 회원탈퇴* 😇]\n닉네임 : {nickname}, 소셜 타입 : {social_type}, OS : {os}, app_version : {app_version}\n가입날짜 : {account.date_joined}\n탈퇴 이유 : {reason}",
            )

            return Response(
                Common.fooiy_standard_response(
                    True,
                ),
            )

        except Exception as e:
            return Response(
                Common.fooiy_standard_response(
                    False, 5006, account_id=account.id, reason=reason, error=e
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @action(detail=False, methods=["patch"])
    def profile(self, request):
        """
        # 프로필 변경 API
        ---
        - ## header
            - ### Authorization : 푸이 계정 토큰
            - ### os : os
            - ### device-id : device uuid
        - ## body (optional 필드들입니다)
            - ### nickname : (nullable) 변경할 닉네임 (최대 20자)
            - ### introduction : (nullable) 변경할 자기소개 (최대 100자)
            - ### gender : (nullable) 변경할 성별 (string, M : 남성 || F : 여성)
            - ### birth_year : (nullable) 변경할 출생년도 (number, ex.1998)
            - ### fooiyti : (nullable) 변경할 푸이티아이
            - ### fooiyti_e_percentage : (nullable) 푸이티아이 E 퍼센트
            - ### fooiyti_i_percentage : (nullable) 푸이티아이 I 퍼센트
            - ### fooiyti_n_percentage : (nullable) 푸이티아이 N 퍼센트
            - ### fooiyti_s_percentage : (nullable) 푸이티아이 S 퍼센트
            - ### fooiyti_t_percentage : (nullable) 푸이티아이 T 퍼센트
            - ### fooiyti_f_percentage : (nullable) 푸이티아이 F 퍼센트
            - ### fooiyti_c_percentage : (nullable) 푸이티아이 C 퍼센트
            - ### fooiyti_a_percentage : (nullable) 푸이티아이 A 퍼센트
            - ### profile_image : (nullable) 변경할 프로필 사진
            - ### is_mkt_agree : (nullable) 마케팅 수신 동의 변경 (true or false)
        - ## payload
            - ### account_info : 업데이트 된 계정 정보
        """

        nickname = request.data.get("nickname", None)
        introduction = request.data.get("introduction", None)
        gender = request.data.get("gender", None)
        birth_year = request.data.get("birth_year", None)
        fooiyti = request.data.get("fooiyti", None)
        fooiyti_e_percentage = request.data.get("fooiyti_e_percentage", None)
        fooiyti_i_percentage = request.data.get("fooiyti_i_percentage", None)
        fooiyti_n_percentage = request.data.get("fooiyti_n_percentage", None)
        fooiyti_s_percentage = request.data.get("fooiyti_s_percentage", None)
        fooiyti_t_percentage = request.data.get("fooiyti_t_percentage", None)
        fooiyti_f_percentage = request.data.get("fooiyti_f_percentage", None)
        fooiyti_c_percentage = request.data.get("fooiyti_c_percentage", None)
        fooiyti_a_percentage = request.data.get("fooiyti_a_percentage", None)
        profile_image = request.FILES.get("profile_image", None)
        fcm_token = request.data.get("fcm_token", None)
        is_mkt_agree = request.data.get("is_mkt_agree", None)

        account = request.account

        try:
            if nickname:
                if fullmatch(Common.RegEx.NICKNAME, nickname) and not (
                    Common.FooiyOfficialAccount.FOOIY_ENGLISH_NICKNAME in nickname
                    or Common.FooiyOfficialAccount.FOOIY_KOREAN_NICKNAME in nickname
                    or Account.objects.filter(nickname=nickname).exists()
                ):
                    account.nickname = nickname
                else:
                    return Response(
                        Common.fooiy_standard_response(
                            False,
                            4016,
                            account_public_id=account.public_id,
                            nickname=nickname,
                        ),
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            if gender:
                account.gender = gender

            if birth_year:
                account.birth_year = birth_year

            if introduction:
                # 띄어쓰기 하나 들어오면 없는것으로 프론트와 합의
                if introduction == " ":
                    account.introduction = None
                else:
                    account.introduction = introduction

            if fooiyti:
                account.fooiyti = Fooiyti.objects.get(fooiyti=fooiyti)

            if is_mkt_agree:
                is_mkt_agree = Common.convert_request_to_boolean[is_mkt_agree]

                if is_mkt_agree:
                    account.is_mkt_agree = True
                    account.date_mkt_agree = timezone.now()
                else:
                    account.is_mkt_agree = False

            if (
                fooiyti_e_percentage
                and fooiyti_i_percentage
                and fooiyti_n_percentage
                and fooiyti_s_percentage
                and fooiyti_t_percentage
                and fooiyti_f_percentage
                and fooiyti_c_percentage
                and fooiyti_a_percentage
            ):
                account.fooiyti_e_percentage = fooiyti_e_percentage
                account.fooiyti_i_percentage = fooiyti_i_percentage
                account.fooiyti_n_percentage = fooiyti_n_percentage
                account.fooiyti_s_percentage = fooiyti_s_percentage
                account.fooiyti_t_percentage = fooiyti_t_percentage
                account.fooiyti_f_percentage = fooiyti_f_percentage
                account.fooiyti_c_percentage = fooiyti_c_percentage
                account.fooiyti_a_percentage = fooiyti_a_percentage

            if profile_image:
                account.profile_image = profile_image

            if fcm_token:
                account.fcm_token = fcm_token

            account.save(
                update_fields=[
                    "nickname",
                    "introduction",
                    "gender",
                    "birth_year",
                    "fooiyti",
                    "fooiyti_e_percentage",
                    "fooiyti_i_percentage",
                    "fooiyti_n_percentage",
                    "fooiyti_s_percentage",
                    "fooiyti_t_percentage",
                    "fooiyti_f_percentage",
                    "fooiyti_c_percentage",
                    "fooiyti_a_percentage",
                    "profile_image",
                    "fcm_token",
                    "is_mkt_agree",
                    "date_mkt_agree",
                ]
            )

            return Response(
                Common.fooiy_standard_response(
                    True,
                    {
                        "account_info": AccountSerializerV2.AccountDetailSerializer(
                            account
                        ).data,
                    },
                ),
            )

        except Exception as e:
            return Response(
                Common.fooiy_standard_response(
                    False, 5007, account_id=account.id, error=e
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @action(detail=False, methods=["get"])
    def info(self, request):
        """
        # 계정 정보 API
        ---
        - ## header
            - ### Authorization : 푸이 계정 토큰
            - ### os : os
            - ### device-id : device uuid
        - ## query-params
            - ### other_account_id (nullable) : 다른 사람의 public_id (다른 사람 마이페이지 들어갈 경우)
        - ## payload
            - ### account_info : 계정 정보
            - ### other_account_info : 다른 사람 계정 정보
        """

        other_account_id = request.query_params.get("other_account_id", None)

        try:
            if other_account_id:
                other_account = AccountsHelpers.convert_public_id_to_account(
                    other_account_id
                )

                return Response(
                    Common.fooiy_standard_response(
                        True,
                        {
                            "account_info": AccountSerializerV2.OtherAccountDetailSerializer(
                                other_account
                            ).data,
                        },
                    ),
                )
            else:
                account = request.account

                return Response(
                    Common.fooiy_standard_response(
                        True,
                        {
                            "account_info": AccountSerializerV2.AccountDetailSerializer(
                                account
                            ).data,
                        },
                    ),
                )

        except Exception as e:
            return Response(
                Common.fooiy_standard_response(
                    False, 5027, account_id=account.id, error=e
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    @action(detail=False, methods=["get"])
    def ranking(self, request):
        """
        # 계정 랭킹 API
        """
        payload = {}

        try:
            rankers = AccountHelpers.CheckRank.get_ranker()
            payload["ranker_list"] = AccountSerializerV2.AccountListSerializer(
                rankers, many=True
            ).data

            return Response(Common.fooiy_standard_response(True, payload))
        except Exception as e:
            return Response(
                Common.fooiy_standard_response(False, 5050, error=e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
