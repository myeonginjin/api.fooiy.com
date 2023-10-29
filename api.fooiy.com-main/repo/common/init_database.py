from archives.models import FooiytiQuestion, Fooiyti, AddressCluster
from shops.models import ShopCategory
from accounts.models import Account
from feeds.models import Pioneer
from common import index as Common
from archives.address_depth import index as AddressDepth


class InitDatabase:
    def insert_fooiyti_questions():
        # 1번 질문
        FooiytiQuestion.objects.create(
            order=1,
            question="음식으로 스트레스를 해소한다면 어떻게 하시나요?",
            is_multi_answer=False,
            answer_1="매운 음식",
            result_1={"E": 7, "I": 0, "S": 0, "N": 0, "F": 0, "T": 0, "A": 0, "C": 0},
            answer_2="단 음식",
            result_2={"E": 0, "I": 1, "S": 0, "N": 0, "F": 0, "T": 0, "A": 0, "C": 5},
            answer_3="그냥 많이 먹음",
            result_3={"E": 0, "I": 0, "S": 0, "N": 0, "F": 0, "T": 0, "A": 0, "C": 0},
            answer_4="먹는 걸로 풀지 않음",
            result_4={"E": 0, "I": 0, "S": 0, "N": 0, "F": 0, "T": 0, "A": 0, "C": 0},
        )

        # 2번 질문
        FooiytiQuestion.objects.create(
            order=2,
            question="배가 고파 편의점에 가서 라면을 하나 사려 합니다. 어떤 걸 살까요?",
            is_multi_answer=False,
            answer_1="신라면",
            result_1={"E": 5, "I": 0, "S": 1, "N": 0, "F": 0, "T": 0, "A": 0, "C": 0},
            answer_2="불닭볶음면",
            result_2={"E": 10, "I": 0, "S": 1, "N": 0, "F": 0, "T": 0, "A": 0, "C": 0},
            answer_3="사리곰탕",
            result_3={"E": 0, "I": 5, "S": 5, "N": 0, "F": 0, "T": 2, "A": 3, "C": 0},
            answer_4="짜파게티",
            result_4={"E": 0, "I": 2, "S": 1, "N": 0, "F": 2, "T": 0, "A": 0, "C": 0},
        )

        # 3번 질문
        FooiytiQuestion.objects.create(
            order=3,
            question="국밥에 추가로 넣고 싶은 것을 알려주세요.",
            is_multi_answer=True,
            answer_1="다데기",
            result_1={"E": 2, "I": 0, "S": 1, "N": 0, "F": 0, "T": 1, "A": 0, "C": 0},
            answer_2="새우젓 / 소금",
            result_2={"E": 0, "I": 0, "S": 5, "N": 0, "F": 0, "T": 0, "A": 0, "C": 0},
            answer_3="후추",
            result_3={"E": 1, "I": 0, "S": 0, "N": 0, "F": 0, "T": 2, "A": 0, "C": 0},
            answer_4="안 넣는다",
            result_4={"E": 0, "I": 4, "S": 0, "N": 4, "F": 0, "T": 0, "A": 0, "C": 0},
        )

        # 4번 질문
        FooiytiQuestion.objects.create(
            order=4,
            question="라면을 끓이려고 합니다.\n도마에 손질된 재료가 놓아져 있습니다.\n당신이 넣고 싶은 재료를 골라주세요.",
            is_multi_answer=True,
            answer_1="치즈",
            result_1={"E": 0, "I": 3, "S": 0, "N": 0, "F": 5, "T": 0, "A": 0, "C": 2},
            answer_2="콩나물",
            result_2={"E": 0, "I": 4, "S": 0, "N": 4, "F": 0, "T": 1, "A": 5, "C": 0},
            answer_3="고추 / 마늘",
            result_3={"E": 3, "I": 0, "S": 0, "N": 0, "F": 0, "T": 1, "A": 3, "C": 0},
            answer_4="안 넣는다",
            result_4={"E": 0, "I": 0, "S": 0, "N": 0, "F": 0, "T": 0, "A": 0, "C": 0},
        )

        # 5번 질문
        FooiytiQuestion.objects.create(
            order=5,
            question="친구 혹은 연인과 파스타집에 갔습니다.\n어떤 파스타를 드실 건가요?",
            is_multi_answer=False,
            answer_1="까르보나라",
            result_1={"E": 0, "I": 2, "S": 0, "N": 0, "F": 7, "T": 0, "A": 0, "C": 0},
            answer_2="토마토",
            result_2={"E": 0, "I": 0, "S": 0, "N": 0, "F": 0, "T": 3, "A": 0, "C": 4},
            answer_3="알리오올리오",
            result_3={"E": 0, "I": 2, "S": 1, "N": 0, "F": 4, "T": 10, "A": 1, "C": 0},
            answer_4="로제",
            result_4={"E": 0, "I": 0, "S": 0, "N": 0, "F": 4, "T": 0, "A": 0, "C": 2},
        )

        # 6번 질문
        FooiytiQuestion.objects.create(
            order=6,
            question="당신은 해외여행 중입니다.\n기내식에서 나온 모닝빵에 곁들일 것을 하나만 골라주세요.",
            is_multi_answer=False,
            answer_1="버터",
            result_1={"E": 0, "I": 0, "S": 0, "N": 0, "F": 4, "T": 0, "A": 1, "C": 0},
            answer_2="누텔라",
            result_2={"E": 0, "I": 0, "S": 0, "N": 0, "F": 5, "T": 0, "A": 0, "C": 8},
            answer_3="딸기잼",
            result_3={"E": 0, "I": 0, "S": 0, "N": 0, "F": 0, "T": 0, "A": 0, "C": 5},
            answer_4="안 바른다",
            result_4={"E": 0, "I": 0, "S": 0, "N": 1, "F": 0, "T": 5, "A": 1, "C": 0},
        )

        # 7번 질문
        FooiytiQuestion.objects.create(
            order=7,
            question='친구들에게 "너 좀 ~~ (이)다"라는 소리를 들어보신 적이 있나요?\n(가장 많이 들은 거 하나)',
            is_multi_answer=False,
            answer_1="초딩 입맛",
            result_1={"E": 0, "I": 0, "S": 1, "N": 0, "F": 0, "T": 0, "A": 0, "C": 10},
            answer_2="아재 입맛",
            result_2={"E": 0, "I": 0, "S": 0, "N": 0, "F": 0, "T": 3, "A": 10, "C": 0},
            answer_3="맵찔이",
            result_3={"E": 0, "I": 10, "S": 0, "N": 0, "F": 0, "T": 0, "A": 0, "C": 0},
            answer_4="한 번도 안 들어봤다",
            result_4={"E": 3, "I": 0, "S": 0, "N": 0, "F": 0, "T": 0, "A": 0, "C": 0},
        )

        # 8번 질문
        FooiytiQuestion.objects.create(
            order=8,
            question="오늘은 당신의 생일입니다.\n받고 싶은 생일상을 골라주세요.",
            is_multi_answer=False,
            answer_1="햄버거, 치킨",
            result_1={"E": 0, "I": 0, "S": 1, "N": 0, "F": 3, "T": 0, "A": 0, "C": 8},
            answer_2="국밥, 수육",
            result_2={"E": 0, "I": 0, "S": 0, "N": 0, "F": 0, "T": 2, "A": 6, "C": 0},
            answer_3="엽기떡볶이, 볼케이노",
            result_3={"E": 7, "I": 0, "S": 0, "N": 0, "F": 0, "T": 0, "A": 0, "C": 0},
            answer_4="스테이크, 파스타",
            result_4={"E": 0, "I": 3, "S": 0, "N": 0, "F": 3, "T": 0, "A": 0, "C": 0},
        )

        # 9번 질문
        FooiytiQuestion.objects.create(
            order=9,
            question="당신은 어쩌다 보니 과자 마케팅 부서에 취업을 했습니다.\n만들고 싶은 과자 꾸러미 세트를 골라주세요.",
            is_multi_answer=True,
            answer_1="뻥이요, 맛동산, 오징어땅콩",
            result_1={"E": 0, "I": 4, "S": 0, "N": 1, "F": 0, "T": 3, "A": 8, "C": 0},
            answer_2="매운새우깡, 썬칩, 신당동떡볶이",
            result_2={"E": 2, "I": 0, "S": 2, "N": 0, "F": 0, "T": 0, "A": 0, "C": 2},
            answer_3="포카칩, 치토스, 프링글스",
            result_3={"E": 0, "I": 2, "S": 3, "N": 0, "F": 0, "T": 0, "A": 0, "C": 2},
            answer_4="버터와플, 버터링, 허니버터칩",
            result_4={"E": 0, "I": 2, "S": 0, "N": 2, "F": 2, "T": 0, "A": 0, "C": 2},
        )

        # 10번 질문
        FooiytiQuestion.objects.create(
            order=10,
            question="선호하는 냉면을 골라주세요.",
            is_multi_answer=False,
            answer_1="물냉면",
            result_1={"E": 0, "I": 4, "S": 0, "N": 0, "F": 0, "T": 0, "A": 0, "C": 0},
            answer_2="비빔냉면",
            result_2={"E": 4, "I": 0, "S": 0, "N": 0, "F": 0, "T": 0, "A": 0, "C": 0},
            answer_3="평양냉면",
            result_3={"E": 0, "I": 3, "S": 0, "N": 3, "F": 0, "T": 0, "A": 4, "C": 0},
            answer_4="냉면이 싫어요",
            result_4={"E": 0, "I": 0, "S": 0, "N": 0, "F": 0, "T": 0, "A": 0, "C": 0},
        )

        # 11번 질문
        FooiytiQuestion.objects.create(
            order=11,
            question="오랜만에 여행을 갔습니다.\n저녁에 고기 파티를 하는데 무엇과 함께 고기를 드실 건가요?",
            is_multi_answer=False,
            answer_1="상추",
            result_1={"E": 0, "I": 0, "S": 0, "N": 0, "F": 0, "T": 0, "A": 1, "C": 0},
            answer_2="깻잎",
            result_2={"E": 0, "I": 0, "S": 0, "N": 0, "F": 0, "T": 0, "A": 1, "C": 0},
            answer_3="명이나물",
            result_3={"E": 0, "I": 0, "S": 0, "N": 0, "F": 0, "T": 0, "A": 1, "C": 0},
            answer_4="야채가 싫어요",
            result_4={"E": 0, "I": 0, "S": 0, "N": 0, "F": 0, "T": 0, "A": 0, "C": 10},
        )

    def insert_fooiyti():
        Fooiyti.objects.create(
            fooiyti="ENTA",
            nickname="젠틀하지만 얼얼한 무우",
            description="매운데 싱거운 담백한 어른",
        )
        Fooiyti.objects.create(
            fooiyti="ENTC",
            nickname="건강한 칠리 잼민이",
            description="매운데 싱거운 담백한 초딩",
        )
        Fooiyti.objects.create(
            fooiyti="ENFA",
            nickname="이목구비가 뚜렷한 고민 많은 청양고추",
            description="매운데 싱거운 느끼한 어른",
        )
        Fooiyti.objects.create(
            fooiyti="ENFC",
            nickname="치근덕대는 핫 치킨",
            description="매운데 싱거운 느끼한 초딩",
        )
        Fooiyti.objects.create(
            fooiyti="ESTA",
            nickname="소금 톡톡 볼케이노 닭 가슴살",
            description="매운데 담백한 느끼한 어른",
        )
        Fooiyti.objects.create(
            fooiyti="ESTC",
            nickname="화끈하게 절여진 쏘야",
            description="매운데 짠 담백한 초딩",
        )
        Fooiyti.objects.create(
            fooiyti="ESFA",
            nickname="삶에 찌든 고지방 김치",
            description="매운데 짠 느끼한 어른",
        )
        Fooiyti.objects.create(
            fooiyti="ESFC",
            nickname="화산 폭발 치즈 떡볶이",
            description="매운데 짠 느끼한 초딩",
        )
        Fooiyti.objects.create(
            fooiyti="INTA",
            nickname="물에 씻은 건강한 무우",
            description="순한 싱거운 담백한 어른",
        )
        Fooiyti.objects.create(
            fooiyti="INTC",
            nickname="젠틀한 어린 고구마",
            description="순한 싱거운 담백한 초딩",
        )
        Fooiyti.objects.create(
            fooiyti="INFA",
            nickname="성숙한 고지방 감자",
            description="순한 싱거운 느끼한 어른",
        )
        Fooiyti.objects.create(
            fooiyti="INFC",
            nickname="과묵한 달걀 피자",
            description="순한 싱거운 느끼한 초딩",
        )
        Fooiyti.objects.create(
            fooiyti="ISTA",
            nickname="바닷속 건강한 고등어",
            description="순한 짠 담백 어른",
        )
        Fooiyti.objects.create(
            fooiyti="ISTC",
            nickname="욕심 없는 후라이드치킨",
            description="순한 짠 담백한 초딩",
        )
        Fooiyti.objects.create(
            fooiyti="ISFA",
            nickname="할 일 많은 바닷속 삼겹살",
            description="순한 짠 느끼한 어른",
        )
        Fooiyti.objects.create(
            fooiyti="ISFC",
            nickname="소금 톡톡 치즈 감자",
            description="순한 짠 느끼한 초딩",
        )

    def insert_shop_category():
        ShopCategory.objects.create(name="CUTLET")
        ShopCategory.objects.create(name="RAW/SUSHI")
        ShopCategory.objects.create(name="JAPANESE")
        ShopCategory.objects.create(name="CHINESE")
        ShopCategory.objects.create(name="CHICKEN")
        ShopCategory.objects.create(name="KOREAN")
        ShopCategory.objects.create(name="SEAFOOD")
        ShopCategory.objects.create(name="NOODLE")
        ShopCategory.objects.create(name="SNACKBAR")
        ShopCategory.objects.create(name="BURGER")
        ShopCategory.objects.create(name="PIZZA")
        ShopCategory.objects.create(name="WESTERN")
        ShopCategory.objects.create(name="MEAT/ROAST")
        ShopCategory.objects.create(name="PETTITOES/BOSSAM")
        ShopCategory.objects.create(name="ASIAN")
        ShopCategory.objects.create(name="TOAST/SANDWICH")
        ShopCategory.objects.create(name="LUNCHBOX/PORRIDGE")
        ShopCategory.objects.create(name="PUB")
        ShopCategory.objects.create(name="SALAD")
        ShopCategory.objects.create(name="BAKERY/CAFE")

    def insert_address_cluster():
        for address_depth1 in AddressDepth.KOREA:
            parent_depth = AddressCluster.objects.create(
                depth=1,
                name=address_depth1["name"],
                longitude=address_depth1["subregion"][0]["location"]["longitude"],
                latitude=address_depth1["subregion"][0]["location"]["latitude"],
            )
            for address_depth2 in address_depth1["subregion"]:
                if address_depth2["name"] == "전체":
                    continue
                AddressCluster.objects.create(
                    depth=2,
                    parent_depth=parent_depth,
                    name=address_depth2["name"],
                    longitude=address_depth2["location"]["longitude"],
                    latitude=address_depth2["location"]["latitude"],
                )

    # 개척 수 인잇 코드
    def calculate_pioneer_count():
        accounts = Account.objects.all()
        for account in accounts:
            account.pioneer_count = Pioneer.objects.filter(
                account=account, state=Common.PioneerState.SUCCESS
            ).count()
            account.save()
