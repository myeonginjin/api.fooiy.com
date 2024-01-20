from rest_framework import status
from rest_framework.response import Response
from functools import wraps

from common import index as Common
from feeds.models import Feed


def get_feed_from_request(require=True) -> Feed:
    """
    # 피드 아이디로 피드 가져오기
    """

    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            feed_id = request.data.get("feed_id", None)
            if not feed_id:
                feed_id = request.query_params.get("feed_id", None)
            if not feed_id:
                try:
                    feed_id = kwargs["pk"]
                except:
                    if not require:
                        request.feed = None
                        return func(request, *args, **kwargs)
                    return Response(
                        Common.fooiy_standard_response(
                            False,
                            4992,
                        ),
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            try:
                feed = Feed.objects.get(id=feed_id)
                request.feed = feed

            except Feed.DoesNotExist:
                return Response(
                    Common.fooiy_standard_response(
                        False,
                        4993,
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except Exception as e:
                return Response(
                    Common.fooiy_standard_response(False, 5995, error=e),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return func(request, *args, **kwargs)

        return wrapper

    return decorator
