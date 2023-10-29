from enum import Enum, auto


class StringEnum(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value


class LogLevel(StringEnum):
    """
    # 푸이 로그 레벨
    """

    INFO = auto()
    WARNING = auto()
    ERROR = auto()


class SocialType(StringEnum):
    """
    # 로그인 타입
    """

    KAKAO = "kakao"
    APPLE = "apple"
    NORMAL = "normal"


class FooiyOfficialAccount(StringEnum):
    """
    사용 불가 계정 닉네임
    """

    FOOIY_KOREAN_NICKNAME = "푸이"
    FOOIY_ENGLISH_NICKNAME = "fooiy"
    FOOIY_ACCOUNT_ID = "1"


class SleepReason(StringEnum):
    """
    # 휴면 이유
    """

    SIGNUP = "새 번호 주인이 회원가입을 함"
    CHANGE_PHONE_NUMBER = "새 번호 주인이 전화번호 변경을 함"


class FeedListType(StringEnum):
    """
    # 피드 리스트 타입
    """

    IMAGE = "image"
    LIST = "list"


class ArchivesImageType(StringEnum):
    """
    # 아카이브 이미지 타입
    """

    OB = auto()
    DPI = auto()
    NSI = auto()
    NSS = auto()
    NSF = auto()
    NMF = auto()
    P = auto()
    R = auto()
    F = auto()
    TE = auto()
    N = auto()
    AD = auto()
    FR = auto()
    RI = auto()


class FeedType(StringEnum):
    """
    # 피드 타입
    """

    PIONEER = "pioneer"
    RECORD = "record"


class PioneerState(StringEnum):
    """
    # 개척 상태
    """

    CONFIRM = auto()
    SUCCESS = auto()
    REJECT = auto()
    ERROR = auto()


class PioneerCheckType(StringEnum):
    """
    # 개척 검수 타입
    """

    SUCCESS = "pioneer-success"
    CAFE = "BAKERY/CAFE"
    PUB = auto()
    REJECT = "pioneer-reject"


class AccountState(StringEnum):
    """
    # 계정 상태
    """

    NORMAL = "normal"
    SLEEP = "sleep"
    WITHDRAWAL = "withdrawal"


class MenuCategory(StringEnum):
    """
    # 메뉴 카테고리
    """

    MAIN = auto()
    SET = auto()
    SIDE = auto()
    BEVERAGE = auto()
    LIQUOR = auto()


class FilterType(StringEnum):
    """
    # 필터 타입
    """

    MAP = auto()
    FEED = auto()


class RegEx(StringEnum):
    """
    # 정규식
    """

    PASSWORD = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d~!@#$%^&*()+|=]{8,16}$"
    NICKNAME = r"^[0-9A-Za-z가-힣][0-9A-Za-z가-힣._]{0,18}[0-9A-Za-z가-힣]$"


class NoticeType(StringEnum):
    """
    # 공지사항 종류
    """

    FORCE_UPDATE = auto()
    UPDATE = auto()
    EMERGENCY = auto()
    FOOIY = auto()


class AdvertisementType(StringEnum):
    """
    # 광고 타입
    """

    BANNER = auto()
    FEED = auto()


class ImageRizeType(StringEnum):
    """
    # 이미지 리사이즈 타입
    """

    SMALL = "small"
    MEDIUM = "medium"


class RankType(StringEnum):
    """
    # 계정 랭크 타입
    """

    RANKER = "ranker"
    PLATINUM = "platinum"
    GOLD = "gold"
    SILVER = "silver"
    BRONZE = "bronze"


class TasteEvaluationImageType(StringEnum):
    """
    # 맛 평가 이모지 타입
    """

    BORDER = "border"
    NO_BORDER = "no_border"


class PushNotificationType(StringEnum):
    """
    # 푸시 타입
    """

    PIONEER_SUCCESS = auto()
    PIONEER_REJECT = auto()
    STORAGE = auto()
    LIKE = auto()
    COMMENT = auto()
    RANK = auto()
    PARTY = auto()
    OVERALL_NOTICE = auto()


class FeedState(StringEnum):
    """
    # 피드 보관 및 좋아요 상태
    """

    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"


class FeedDomainType(StringEnum):
    """
    # 피드 보관 및 좋아요 상태
    """

    Mypage = "mypage"
    Party = "party"


class ShopMainCategory(StringEnum):
    """
    # 개척 등록 성공 유형
    """

    CAFE = "BAKERY/CAFE"
    PUB = auto()
    COMMON = auto()


class ShopFilter(StringEnum):
    """
    # 지도 리스트 매장 필터
    """

    PERSONALIZE = "personalize"
    POPULAR = "popular"


class SuggestionType(StringEnum):
    """
    # 문의 및 제보 타입
    """

    IMP = auto()
    FR = auto()
    BUG = auto()
    AC = auto()
    AD = auto()
    ETC = auto()
    TIP_OFF = auto()


class AmenuType(StringEnum):
    SELECT_MENU = "select_menu"
    A_MENU = "a_menu"


class PartyState(StringEnum):
    """
    # 파티 가입 상태
    """

    SUBSCRIBE = "subscribe"
    CONFIRM = "confirm"
    UNSUBSCRIBE = "unsubscribe"
    REJECT = "reject"
    EXPULSION = "expulsion"


class FeedUpdateState(StringEnum):
    """
    # 피드 수정 및 등록 상태
    """

    UPDATE = auto()
    REGISTER = auto()
    DELETE = auto()


class CommentState(StringEnum):
    """
    # 피드 수정 및 등록 상태
    """

    PARENT_COMMENT = auto()
    CHILD_COMMENT = auto()


class PushNavigationType(StringEnum):
    """
    # 푸시 네비게이션 타입
    """

    FEED = "feed"
    RANK = "rank"
    PARTY = "party"
    COMMENT = "comment"
    MY_PAGE = "my_page"
    OVERALL_NOTICE = "overall_notice"


class CheckChangeRankType(StringEnum):
    """
    # 랭크 변동 체크 타입
    """

    REGISTRATION = auto()
    DEMOTION = auto()


class ShopMapMarkerType(StringEnum):
    """
    # 음식점 지도 마커 타입
    """

    SPOT = "spot"
    LANDMARK = "landmark"
