from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.viewsets import (
    mixins,
    GenericViewSet,
)

from rest_framework.response import Response

from common import index as Common

from accounts.helpers import index as AccountsHelpers
from ...serializers.v2 import index as ArchiveSerializerV2
from ...models import Image

import logging

logger = logging.getLogger("api")


class ImageViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    # 아카이브 이미지 관련 뷰셋
    ---
    - archives/image (get) : 아카이브 이미지 API
    """

    serializer_class = ArchiveSerializerV2.ImageListSerializer
    http_method_names = ["get"]

    @method_decorator(AccountsHelpers.fooiy_account_guard())
    def list(self, request):
        """
        # 아카이브 이미지 리스트 API
        ---
        - ## query-params
            - ### type : 회원가입 타입 (온보딩 : OB)
        - ## payload
            - ### image_list : 아카이브 이미지 리스트
        """
        _type = request.query_params.get("type", None)

        try:
            images = Image.objects.filter(type=_type).order_by("order")

            return Response(
                Common.fooiy_standard_response(
                    True,
                    {
                        "image_list": [
                            image["image"]
                            for image in ArchiveSerializerV2.ImageListSerializer(
                                images, many=True
                            ).data
                        ],
                    },
                ),
            )

        except Exception as e:
            return Response(
                Common.fooiy_standard_response(False, 5008, type=_type, error=e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
