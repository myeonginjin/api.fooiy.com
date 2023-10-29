from rest_framework import status
from rest_framework.response import Response
from functools import wraps

from common import index as Common
from shops.models import Shop


def get_shop_from_request(require=True) -> Shop:
    """
    # 매장 퍼블릭 아이디로 매장 가져오기
    """

    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if "shop_id" in request.query_params:
                shop_id = request.query_params.get("shop_id", None)
            else:
                shop_id = request.data.get("shop_id", None)

            try:
                shop = Shop.objects.get(public_id=shop_id)

                request.shop = shop
            except Shop.DoesNotExist:
                if not require:
                    request.shop = None
                    return func(request, *args, **kwargs)
                return Response(
                    Common.fooiy_standard_response(False, 4997),
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except Exception as e:
                return Response(
                    Common.fooiy_standard_response(
                        False,
                        5998,
                        error=e,
                    ),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return func(request, *args, **kwargs)

        return wrapper

    return decorator
