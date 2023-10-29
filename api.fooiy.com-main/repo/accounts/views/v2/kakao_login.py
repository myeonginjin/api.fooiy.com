from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view

from rest_framework.response import Response

from fooiy import env
from ...helpers import index as AccountsHelpers
from ...models import Account
from ...serializers.v2 import index as AccountSerializerV2
from archives.models import Image
from common import index as Common

import jwt, time

import logging

logger = logging.getLogger("api")


@api_view(["POST"])
def kakao_login(request):
    """
    # 카카오 로그인 API
    """
    social_id = request.data.get("social_id", None)
    os = request.data.get("os", None)
    app_version = request.data.get("app_version", None)
    device_id = request.data.get("device_id", None)
    fcm_token = request.data.get("fcm_token", None)

    if os and app_version and device_id and fcm_token:
        try:
            try:
                account = Account.objects.get(
                    social_type=Common.SocialType.KAKAO,
                    social_id=f"{Common.SocialType.KAKAO}-{social_id}",
                )
                account.is_active = True
                account.os = os
                account.app_version = app_version
                account.fcm_token = fcm_token
                account.device_id = f"{os}-{device_id}"
                account.last_login = timezone.now()

                account.save(
                    update_fields=[
                        "is_active",
                        "os",
                        "app_version",
                        "fcm_token",
                        "device_id",
                        "last_login",
                    ]
                )

                Common.slack_post_message(
                    "#notify_account",
                    f"[🙋‍♂️ *푸이 카카오 로그인* 🙋‍♀️]\n닉네임 : {account.nickname}, os : {os}, app_version : {app_version}",
                )

                return Response(
                    Common.fooiy_standard_response(
                        True,
                        {
                            "account_info": AccountSerializerV2.AccountDetailSerializer(
                                account
                            ).data,
                            "is_join": False,
                        },
                    ),
                )
            except Account.DoesNotExist:
                ##################################################
                # GENERATE account_token
                # ---------------------------
                # hash algorithm : HS256
                # user information : social_id, created_at
                ##################################################
                account_token = jwt.encode(
                    {"social_id": social_id, "created_at": time.time()},
                    env.FOOIY_JWT_SECRET_KEY,
                    algorithm="HS256",
                )
                default_profile_image = Image.objects.get(type="DPI").image

                Account.objects.create_social_user(
                    social_type=Common.SocialType.KAKAO,
                    social_id=f"{Common.SocialType.KAKAO}-{social_id}",
                    account_token=account_token,
                    os=os,
                    app_version=app_version,
                    fcm_token=fcm_token,
                    profile_image=default_profile_image,
                    device_id=f"{os}-{device_id}",
                    state=Common.AccountState.NORMAL,
                )

                account = Account.objects.get(
                    social_type=Common.SocialType.KAKAO,
                    social_id=f"{Common.SocialType.KAKAO}-{social_id}",
                )

                nickname = AccountsHelpers.create_random_nickname(account.id)
                account.nickname = nickname

                account.save(update_fields=["date_mkt_agree", "nickname"])

                Common.slack_post_message(
                    "#notify_account",
                    f"[🎉 *푸이 카카오 회원가입* 🎉]\n닉네임 : {nickname}, OS : {os}, 버전 : {app_version}",
                )

                return Response(
                    Common.fooiy_standard_response(
                        True,
                        {
                            "account_info": AccountSerializerV2.AccountDetailSerializer(
                                account
                            ).data,
                            "is_join": False,
                        },
                    ),
                    status=status.HTTP_201_CREATED,
                )
        except Exception as e:
            return Response(
                Common.fooiy_standard_response(
                    False, 5041, os=os, app_version=app_version, error=e
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    else:
        return Response(
            Common.fooiy_standard_response(
                False,
                4045,
                os=os,
                app_version=app_version,
                device_id=device_id,
                fcm_token=fcm_token,
            ),
            status=status.HTTP_400_BAD_REQUEST,
        )
