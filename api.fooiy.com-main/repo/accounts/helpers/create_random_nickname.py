import random, time

adjective_list = [
    "달달구리한",
    "버터맛_나는",
    "치즈맛",
    "쫄깃쫄깃한",
    "바삭바삭한",
    "매운",
    "풍미가_좋은",
    "신선한",
    "촉촉한",
    "짠",
    "시큼한",
    "매콤한",
    "톡_쏘는",
    "단",
    "고소한",
    "진한",
    "단짠단짠",
    "새콤한",
    "달짝지근한",
    "구수한",
    "향이_좋은",
]

food_list = [
    "초계탕",
    "평양냉면",
    "물냉면",
    "진주냉면",
    "간짜장",
    "사천짜장",
    "삼선짜장",
    "볶음짬뽕",
    "우동",
    "닭갈비",
    "갈비",
    "장조림",
    "돼지갈비",
    "삼겹살",
    "제육볶음",
    "보쌈",
    "족발",
    "순대",
    "떡볶이",
    "닭강정",
    "백숙",
    "간장치킨",
    "물회",
    "초밥",
    "장어구이",
    "회덮밥",
    "감자전",
    "해물파전",
    "순대국밥",
    "갈비탕",
    "설렁탕",
    "삼계탕",
    "김치찌개",
    "된장찌개",
    "동태찌개",
    "고등어조림",
    "갈치조림",
    "튀김만두",
    "야채튀김",
    "오징어튀김",
    "회오리감자",
    "쫄면",
    "라면",
    "양념게장",
    "간장게장",
    "김밥",
    "핫도그",
    "돈까스",
    "피자",
    "육회비빔밥",
]

number_to_alphabet_dict = {
    "0": "a",
    "1": "n",
    "2": "d",
    "3": "f",
    "4": "v",
    "5": "m",
    "6": "i",
    "7": "e",
    "8": "w",
    "9": "o",
}


def create_random_nickname(id):
    id = str(id + 17053892)
    seq = ""
    flag = int(time.time() % 2)

    for index, number in enumerate(id):
        if flag:
            if not index % 2:
                seq += number_to_alphabet_dict[number]
            else:
                seq += number
        else:
            if not index % 2:
                seq += number
            else:
                seq += number_to_alphabet_dict[number]

    return random.choice(adjective_list) + "_" + random.choice(food_list) + seq
