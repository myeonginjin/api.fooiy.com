from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response

from fooiy import env
from common import index as Common

from functools import wraps
import jwt


def fooiy_account_guard(login=True):
    """
    # 푸이 계정 토큰 가드
    """

    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            try:
                account_token = request.headers.get("Authorization", None)
                if account_token == env.FOOIY_GUEST_TOKEN:
                    return func(request, *args, **kwargs)
                os = request.headers.get("os", None)
                device_id = request.headers.get("device-id", None)

                if account_token and os and device_id:
                    Account = get_user_model()

                    jwt.decode(
                        account_token,
                        env.FOOIY_JWT_SECRET_KEY,
                        algorithms=["HS256"],
                    )

                    account = Account.objects.get(account_token=account_token)

                    account.os = os
                    account.device_id = f"{os}-{device_id}"

                    account.save(update_fields=["os", "device_id"])

                    #### 중복 로그인 로직 ####
                    # if account.device_id != f"{os}-{device_id}":
                    #     return Response(
                    #         Common.fooiy_standard_response(
                    #             False,4998,
                    #             account_device_id=account.device_id,
                    #             request_device_id=f"{os}-{device_id}",
                    #         ),
                    #         status=status.HTTP_418_IM_A_TEAPOT,
                    #     )

                    request.account = account

                    if login and not account:
                        return Response(
                            Common.fooiy_standard_response(False, 4991),
                            status=status.HTTP_401_UNAUTHORIZED,
                        )
                else:
                    return Response(
                        Common.fooiy_standard_response(
                            False,
                            4999,
                            account_token=account_token,
                            os=os,
                            device_id=device_id,
                        ),
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
            except Exception as e:
                return Response(
                    Common.fooiy_standard_response(False, 5999, error=e),
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            return func(request, *args, **kwargs)

        return wrapper

    return decorator
