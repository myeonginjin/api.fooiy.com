from archives.models import Fooiyti, FooiytiQuestion
from common import index as Common

QUESTIONS_START_INDEX = 1
fooiyti_order = Common.global_variables.FOOIYTI_ORDER
FOOIYTI_ORDER_NUMBER = len(fooiyti_order)
ANSWER_1, ANSWER_2, ANSWER_3 = "0", "1", "2"


def calculate_fooiyti(fooiyti_answers):
    fooiyti_result = [0] * 8
    fooiyti_sum = [0] * 8
    question_number = QUESTIONS_START_INDEX
    fooiyti = ""
    fooiyti_questions = FooiytiQuestion.objects.filter(type="app")
    for answers in fooiyti_answers:
        fooiyti_question = fooiyti_questions.get(order=question_number)
        for answer in answers:
            if answer == ANSWER_1:
                fooiyti_result = [
                    fooiyti_result[idx] + fooiyti_question.result_1[fooiyti_order[idx]]
                    for idx in range(FOOIYTI_ORDER_NUMBER)
                ]
            elif answer == ANSWER_2:
                fooiyti_result = [
                    fooiyti_result[idx] + fooiyti_question.result_2[fooiyti_order[idx]]
                    for idx in range(FOOIYTI_ORDER_NUMBER)
                ]
            elif answer == ANSWER_3:
                fooiyti_result = [
                    fooiyti_result[idx] + fooiyti_question.result_3[fooiyti_order[idx]]
                    for idx in range(FOOIYTI_ORDER_NUMBER)
                ]
            else:
                fooiyti_result = [
                    fooiyti_result[idx] + fooiyti_question.result_4[fooiyti_order[idx]]
                    for idx in range(FOOIYTI_ORDER_NUMBER)
                ]

        question_number += 1
        fooiyti_sum = [
            fooiyti_sum[idx]
            + fooiyti_question.result_1[fooiyti_order[idx]]
            + fooiyti_question.result_2[fooiyti_order[idx]]
            + fooiyti_question.result_3[fooiyti_order[idx]]
            + fooiyti_question.result_4[fooiyti_order[idx]]
            for idx in range(FOOIYTI_ORDER_NUMBER)
        ]

    for i in range(FOOIYTI_ORDER_NUMBER):
        fooiyti_result[i] = fooiyti_result[i] / fooiyti_sum[i]

    for i in range(0, FOOIYTI_ORDER_NUMBER, 2):
        fooiyti_result[i + 1] = int(
            fooiyti_result[i + 1]
            / (fooiyti_result[i // 2 * 2] + fooiyti_result[i // 2 * 2 + 1])
            * 100
        )
        fooiyti_result[i] = 100 - fooiyti_result[i + 1]
        if fooiyti_result[i] >= fooiyti_result[i + 1]:
            fooiyti += fooiyti_order[i]
        else:
            fooiyti += fooiyti_order[i + 1]
    fooiyti = Fooiyti.objects.get(fooiyti=fooiyti)

    return {
        "fooiyti": fooiyti.fooiyti,
        "fooiyti_nickname": fooiyti.nickname,
        "fooiyti_ratio": {
            fooiyti_order[i]: fooiyti_result[i] for i in range(FOOIYTI_ORDER_NUMBER)
        },
        "description": fooiyti.description,
        "fooiyti_result_image": fooiyti.image.last().image.url,
    }
