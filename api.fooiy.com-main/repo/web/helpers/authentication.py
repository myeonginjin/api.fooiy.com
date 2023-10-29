from rest_framework import status
from rest_framework.response import Response

from fooiy import env
from common import index as Common

from functools import wraps


def fooiy_web_guard():
    """
    # 푸이 웹 가드
    """

    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if "Authorization" not in request.headers:
                return Response(
                    Common.fooiy_standard_response(
                        False,
                        4995,
                    ),
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            fooiy_web_token = request.headers["Authorization"]

            if fooiy_web_token != env.FOOIY_GUEST_TOKEN:
                return Response(
                    Common.fooiy_standard_response(
                        False, 4995, fooiy_web_token=fooiy_web_token
                    ),
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            return func(request, *args, **kwargs)

        return wrapper

    return decorator
