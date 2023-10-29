from rest_framework import status
from rest_framework.response import Response

from common import index as Common
from ..models import Account


def convert_public_id_to_account(account_id):
    """
    # 계정 퍼블릭 아이디로 account 들고 오기
    """

    try:
        account = Account.objects.get(public_id=account_id)
        return account

    except Account.DoesNotExist:
        return Response(
            Common.fooiy_standard_response(
                False,4994,error='dose not exist account from account_id'
            ),
            status=status.HTTP_400_BAD_REQUEST,
        )

    except Exception as e:
        return Response(
            Common.fooiy_standard_response(
                False,5997,error=e
            ),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
