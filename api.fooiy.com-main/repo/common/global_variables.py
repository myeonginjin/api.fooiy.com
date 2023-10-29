from fooiy.settings import MEDIA_URL
from common.enums import RankType

#######################
# 전역 변수 관리
#######################

withdrawn_member_nickname = "탈퇴한 회원"
# 지도 기본 지역(혜화)
default_longitude_left_bottom = "127.001141181595"
default_latitude_left_bottom = "37.5812861026278"
default_longitude_right_top = "127.003075297162"
default_latitude_right_top = "37.583890209576"
default_longitude = "127.002736308322"
default_latitude = "37.5833730477478"
default_address_depth1 = "서울"
default_address_depth2 = "종로구"
# 매장 카테고리 리스트
shop_category_list = [
    "CUTLET",
    "RAW/SUSHI",
    "JAPANESE",
    "CHINESE",
    "CHICKEN",
    "KOREAN",
    "SEAFOOD",
    "NOODLE",
    "SNACKBAR",
    "BURGER",
    "PIZZA",
    "WESTERN",
    "MEAT/ROAST",
    "PETTITOES/BOSSAM",
    "ASIAN",
    "TOAST/SANDWICH",
    "LUNCHBOX/PORRIDGE",
    "PUB",
    "SALAD",
    "BAKERY/CAFE",
]
# 매장 카테고리 딕셔너리
shop_category_dict = {
    "CUTLET": "돈까스",
    "RAW/SUSHI": "회/초밥",
    "JAPANESE": "일식",
    "CHINESE": "중식",
    "CHICKEN": "치킨",
    "KOREAN": "한식",
    "SEAFOOD": "해산물",
    "NOODLE": "국수",
    "SNACKBAR": "분식",
    "BURGER": "햄버거",
    "PIZZA": "피자",
    "WESTERN": "양식",
    "MEAT/ROAST": "고기/구이",
    "PETTITOES/BOSSAM": "족발/보쌈",
    "ASIAN": "아시안",
    "TOAST/SANDWICH": "토스트/샌드위치",
    "LUNCHBOX/PORRIDGE": "도시락/죽",
    "PUB": "요리주점",
    "SALAD": "샐러드",
    "BAKERY/CAFE": "베이커리/카페",
}
category_cafe = "BAKERY/CAFE"

# 메시지 추후 수정 예정
version_force_update_message = "반드시 업데이트를 해야 해요!"
version_normal_update_message = "최신 버전이 있어요! 업데이트할까요?"

taste_evaluation_base_url = f"{MEDIA_URL}archives/image/taste-evaluation/"

LARGEST_DEPTH = "1"
LOWEST_DEPTH = "4"
FOOIYTI_ORDER = "EISNTFAC"

rank_criteria = {
    RankType.PLATINUM: 100,
    RankType.GOLD: 60,
    RankType.SILVER: 30,
    RankType.BRONZE: 10,
}

LONGITUDE_KIOLMETER_RATIO = 0.015
LATITUDE_KIOLMETER_RATIO = 0.01
