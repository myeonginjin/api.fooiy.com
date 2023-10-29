from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.viewsets import (
    mixins,
    GenericViewSet,
)

from rest_framework.response import Response
from rest_framework.decorators import action

from common import index as Common
from accounts.helpers import index as AccountsHelpers
from archives.helpers import index as ArchivesHelpers
from ...serializers.v2 import index as ArchiveSerializerV2
from ...models import Image, FooiytiQuestion

import logging

logger = logging.getLogger("api")


class FooiytiViewSet(mixins.CreateModelMixin, GenericViewSet):
    """
    # 푸이티아이 관련 뷰셋
    ---
    - archives/fooiyti/question (get) : 푸이티아이 질문지 리스트 API
    - archives/fooiyti/result (get) : 푸이티아이 결과 API
    """

    serializer_class = ArchiveSerializerV2.ImageListSerializer
    http_method_names = ["get"]

    @method_decorator(AccountsHelpers.fooiy_account_guard(login=False))
    @action(detail=False, methods=["get"])
    def question(self, request):
        """
        # 푸이티아이 질문지 리스트 API
        """
        _type = request.query_params.get("type", "app")
        try:
            queryset = (
                FooiytiQuestion.objects.filter(type=_type)
                .only("question", "answer_1", "answer_2", "answer_3", "answer_4")
                .order_by("order")
            )

            fooiyti_questions = []

            for fooiyti in queryset:
                answers = [
                    fooiyti.answer_1,
                    fooiyti.answer_2,
                    fooiyti.answer_3,
                    fooiyti.answer_4,
                ]

                fooiyti_questions.append(
                    {
                        "question": fooiyti.question,
                        "is_multi_answer": fooiyti.is_multi_answer,
                        "answers": answers,
                    }
                )

            return Response(
                Common.fooiy_standard_response(
                    True,
                    {
                        "fooiyti_questions": fooiyti_questions,
                    },
                ),
            )
        except Exception as e:
            return Response(
                Common.fooiy_standard_response(False, 5009, error=e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @method_decorator(AccountsHelpers.fooiy_account_guard(login=False))
    @action(detail=False, methods=["get"])
    def result(self, request):
        """
        # 푸이티아이 결과 API
        ---
        - ## query_params
            - ### fooiyti_answers : 푸이티아이 답안
                - {"fooiyti_answers" = [[1],[4],[1,3] ...]} (이중배열에 인덱스별로 답안 몇번인지)
        - ## payload
            - ### fooiyti_result : 푸이티아이 결과
        """
        fooiyti_answers = request.query_params.get("fooiyti_answers", "")

        fooiyti_answers_list = [[] for _ in range(FooiytiQuestion.objects.count() // 2)]

        for answer_index, fooiy_answer in enumerate(fooiyti_answers.split("]")):
            for answer_number in fooiy_answer:
                if answer_number.isdigit():
                    fooiyti_answers_list[answer_index].append(answer_number)

        if fooiyti_answers:
            try:
                return Response(
                    Common.fooiy_standard_response(
                        True,
                        {
                            "fooiyti_result": ArchivesHelpers.calculate_fooiyti(
                                fooiyti_answers_list
                            )
                        },
                    )
                )
            except Exception as e:
                return Response(Common.fooiy_standard_response(False, 5014, error=e))

        else:
            return Response(
                Common.fooiy_standard_response(
                    False, 4021, fooiyti_answers=fooiyti_answers
                )
            )
