from rest_framework import status
from rest_framework.response import Response
from functools import wraps

from common import index as Common
from feeds.models import FeedComment
from accounts.models import Party


class Decorators:
    def get_party_from_request(require=True) -> Party:
        """
        # 파티 아이디로 파티 가져오기
        """

        def decorator(func):
            @wraps(func)
            def wrapper(request, *args, **kwargs):
                party_id = request.data.get("party_id", None)
                if not party_id:
                    party_id = request.query_params.get("party_id", None)
                if not party_id:
                    try:
                        party_id = kwargs["pk"]
                    except:
                        if not require:
                            request.party = None
                            return func(request, *args, **kwargs)
                        return Response(
                            Common.fooiy_standard_response(
                                False,
                                4987,
                            ),
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                try:
                    request.party = Party.objects.get(id=party_id)

                except Party.DoesNotExist:
                    return Response(
                        Common.fooiy_standard_response(
                            False,
                            4987,
                        ),
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                except Exception as e:
                    return Response(
                        Common.fooiy_standard_response(False, 5993, error=e),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

                return func(request, *args, **kwargs)

            return wrapper

        return decorator
