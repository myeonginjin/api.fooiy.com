from rest_framework import status
from rest_framework.response import Response
from functools import wraps

from common import index as Common
from feeds.models import FeedComment


def get_feed_comment_from_request(require=True) -> FeedComment:
    """
    # 피드댓글 아이디로 피드댓글 가져오기
    """

    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            comment_id = request.data.get("comment_id", None)
            if not comment_id:
                comment_id = request.query_params.get("comment_id", None)
            if not comment_id:
                try:
                    comment_id = kwargs["pk"]
                except:
                    if not require:
                        request.comment = None
                        return func(request, *args, **kwargs)
                    return Response(
                        Common.fooiy_standard_response(
                            False,
                            4989,
                        ),
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            try:
                comment = FeedComment.objects.get(id=comment_id)
                request.comment = comment

            except FeedComment.DoesNotExist:
                return Response(
                    Common.fooiy_standard_response(
                        False,
                        4990,
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except Exception as e:
                return Response(
                    Common.fooiy_standard_response(False, 5994, error=e),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return func(request, *args, **kwargs)

        return wrapper

    return decorator
