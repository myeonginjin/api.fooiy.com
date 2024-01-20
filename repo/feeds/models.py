from django.db import models
from django.utils import timezone
import uuid

from common import index as Common
from feeds.helpers.get_slack_attachments import get_notification_shop_slack_attachments
from shops.models import SHOP_CATEGORY, Menu, MENU_CATEGORY

# 개척 상태 초이스
PIONEER_STATE = (
    ("CONFIRM", "검수"),
    ("SUCCESS", "성공"),
    ("REJECT", "반려"),
    ("ERROR", "에러"),
)

# 피드 파티 상태 초이스
PARTY_STATE = (
    ("subscribe", "구독"),
    ("unsubscribe", "구독취소"),
)

# 개척 반려 이유 초이스
PIONEER_REJECT_REASON = (
    ("should be main menu for first shop", "메인 혹은 세트 메뉴만 등록 가능하여 개척이 반려되었어요."),
    ("does not suitable comment", "부적절한 코멘트 사용으로 개척이 반려되었어요."),
    ("does not exist shop", "등록하신 음식점을 찾을 수 없어 개척이 반려되었어요."),
    ("does not suitable image", "사진 등록 규정에 맞지 않아 개척이 반려되었어요."),
    ("already exist pioneered", "이미 개척 완료된 음식이므로 기록으로 등록되었습니다."),
    ("pioneer is only able to one menu", "한 번에 한 메뉴만 등록 가능하여 개척이 반려되었어요."),
    ("does not satisfy fooiy rule", "푸이 내부 규정에 의해 개척이 반려되었어요."),
)

# 푸이티아이 초이스
FOOIYTI_TYPE = (
    ("ENTC", "ENTC"),
    ("ENTA", "ENTA"),
    ("ENFA", "ENFA"),
    ("ENFC", "ENFC"),
    ("ESTC", "ESTC"),
    ("ESTA", "ESTA"),
    ("ESFA", "ESFA"),
    ("ESFC", "ESFC"),
    ("INTC", "INTC"),
    ("INTA", "INTA"),
    ("INFA", "INFA"),
    ("INFC", "INFC"),
    ("ISTC", "ISTC"),
    ("ISTA", "ISTA"),
    ("ISFA", "ISFA"),
    ("ISFC", "ISFC"),
)

# 피드 타입
FEED_TYPE = (
    ("PIONEER", "개척"),
    ("RECORD", "기록"),
)


def feeds_pioneer_image_upload_url(instance, filename):
    return f"feeds/pioneer/{instance.account.public_id}/{instance.id}/{uuid.uuid4().hex[:12].upper()}.{filename.split('.')[-1]}"


# 피드 테이블
class Feed(models.Model):
    # 피드 pk
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="피드 pk",
    )
    # 피드 작성자
    account = models.ForeignKey(
        "accounts.Account",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="feed",
        db_index=True,
    )
    # 매장 정보
    shop = models.ForeignKey(
        "shops.Shop",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="feed",
        db_index=True,
    )
    # 메뉴 정보
    menu = models.ForeignKey(
        Menu,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="feed",
        db_index=True,
    )
    # 피드 작성자 푸이티아이
    fooiyti = models.CharField(
        max_length=4,
        verbose_name="피드 작성자 푸이티아이",
        choices=FOOIYTI_TYPE,
        blank=True,
        null=True,
    )
    # 피드 설명
    description = models.CharField(
        max_length=500,
        verbose_name="피드 설명",
        blank=True,
        null=True,
    )
    # 맛 평가
    taste_evaluation = models.PositiveSmallIntegerField(
        default=50,
        verbose_name="맛 평가",
        help_text="좋다 : 99, 보통 : 50, 싫다 : 0",
    )
    # 피드 타입
    type = models.CharField(
        choices=FEED_TYPE,
        max_length=15,
        null=True,
        blank=True,
        verbose_name="피드 타입",
    )
    # 피드 공개 여부
    is_exposure = models.BooleanField(
        default=True, null=True, blank=True, verbose_name="피드 공개 여부"
    )

    # 생성일
    created_at = models.DateTimeField(default=timezone.now, verbose_name="생성일")

    # 경도
    longitude = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="경도",
    )
    # 위도
    latitude = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="위도",
    )

    class Meta:
        verbose_name = "4.3 피드 정보"
        verbose_name_plural = "4.3 피드 정보"

    def save(self, *args, **kwargs):
        try:
            self.longitude = self.shop.longitude
            self.latitude = self.shop.latitude
            super().save(*args, **kwargs)
        except:
            Common.slack_post_message(
                "#notification_shop",
                "",
                get_notification_shop_slack_attachments(self.shop),
            )


class FeedFooiyti(models.Model):
    feed = models.OneToOneField(
        Feed,
        on_delete=models.CASCADE,
        null=True,
    )
    fooiyti_e = models.SmallIntegerField(blank=True, null=True, default=50)
    fooiyti_i = models.SmallIntegerField(blank=True, null=True, default=50)
    fooiyti_n = models.SmallIntegerField(blank=True, null=True, default=50)
    fooiyti_s = models.SmallIntegerField(blank=True, null=True, default=50)
    fooiyti_t = models.SmallIntegerField(blank=True, null=True, default=50)
    fooiyti_f = models.SmallIntegerField(blank=True, null=True, default=50)
    fooiyti_c = models.SmallIntegerField(blank=True, null=True, default=50)
    fooiyti_a = models.SmallIntegerField(blank=True, null=True, default=50)

    class Meta:
        verbose_name = "4.3.1 피드 푸이티아이"
        verbose_name_plural = "4.3.1 피드 푸이티아이"


class FeedComment(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="피드 댓글 pk",
    )
    feed = models.ForeignKey(
        Feed,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="feed_comment",
        db_index=True,
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="feed_comment",
        verbose_name="상위 댓글 정보",
    )
    writer = models.ForeignKey(
        "accounts.Account",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="feed_comment",
        db_index=True,
    )
    content = models.CharField(
        max_length=500,
        verbose_name="댓글 내용",
        blank=True,
        null=True,
    )
    order = models.PositiveIntegerField(
        default=1000,
        null=True,
        blank=True,
        verbose_name="댓글 순서",
    )
    is_reported = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="신고된 댓글",
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name="댓글 작성일")

    class Meta:
        verbose_name = "4.3.1 피드 댓글"
        verbose_name_plural = "4.3.1 피드 댓글"


# 피드 파티 중개 테이블
class FeedParty(models.Model):
    # 피드 파티 중개 테이블 pk
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="피드 파티 중개 테이블 pk",
        db_index=True,
    )

    # 피드
    feed = models.ForeignKey(
        "feeds.Feed",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="feed_party",
    )
    # 파티
    party = models.ForeignKey(
        "accounts.Party",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="feed_party",
    )

    state = models.CharField(
        max_length=12,
        choices=PARTY_STATE,
        default="subscribe",
        null=True,
        blank=True,
    )
    # 생성일
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")

    class Meta:
        unique_together = [["feed", "party"]]
        verbose_name = "4.3.2 피드, 파티 관계 정보"
        verbose_name_plural = "4.3.2 피드, 파티 관계 정보"


# 기록 테이블
class Record(models.Model):
    # 기록 pk
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="기록 pk",
    )

    # 기록 작성자
    account = models.ForeignKey(
        "accounts.Account",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="record",
        db_index=True,
    )

    # 매장 정보
    shop = models.ForeignKey(
        "shops.Shop",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="record",
        db_index=True,
    )

    # 메뉴 정보
    menu = models.ForeignKey(
        Menu,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="record",
        db_index=True,
    )

    """
        먹은 메뉴 소감
    """
    # 기록 코멘트
    comment = models.CharField(
        max_length=500,
        verbose_name="기록 작성자 코멘트",
        blank=True,
        null=True,
        help_text="ex) 여기 진짜 맛있어요!",
    )
    # 맛 평가
    taste_evaluation = models.PositiveSmallIntegerField(
        default=50,
        verbose_name="맛 평가",
        help_text="좋다 : 100, 보통 : 50, 싫다 : 0",
    )
    # 기록 작성자 푸이티아이
    fooiyti = models.CharField(
        max_length=4,
        verbose_name="기록 작성자 푸이티아이",
        choices=FOOIYTI_TYPE,
        blank=True,
        null=True,
    )

    # 기록 공개 여부
    is_exposure = models.BooleanField(
        default=True, null=True, blank=True, verbose_name="기록 공개 여부"
    )

    # 생성일
    created_at = models.DateTimeField(default=timezone.now, verbose_name="생성일")

    class Meta:
        verbose_name = "4.1 기록 정보"
        verbose_name_plural = "4.1 기록 정보"


# 개척 테이블
class Pioneer(models.Model):
    # 개척 pk
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="개척 pk",
    )

    # 개척자
    account = models.ForeignKey(
        "accounts.Account",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="pioneer",
        db_index=True,
        verbose_name="개척자",
    )

    """
        먹은 메뉴 정보
    """
    # 메뉴 정보
    menu = models.ForeignKey(
        Menu,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="pioneer",
        db_index=True,
    )
    # 메뉴 이름
    menu_name = models.CharField(
        max_length=50,
        verbose_name="메뉴 명",
        blank=True,
        null=True,
        help_text="ex) 맵도리탕",
    )
    # 메뉴 가격
    menu_price = models.PositiveIntegerField(
        null=True, default=0, verbose_name="메뉴 가격", help_text="ex) 12500"
    )
    # 메뉴 카테고리
    menu_category = models.CharField(
        max_length=10,
        choices=MENU_CATEGORY,
        blank=True,
        null=True,
        verbose_name="메뉴 카테고리",
    )
    # 대표 메뉴 여부
    is_best_menu = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name="대표 메뉴 여부",
        help_text="매장의 대표메뉴 인지",
    )

    """
        먹은 메뉴 소감
    """
    # 개척 코멘트
    comment = models.CharField(
        max_length=500,
        verbose_name="기록 작성자 코멘트",
        blank=True,
        null=True,
        help_text="ex) 여기 진짜 맛있어요!",
    )
    # 맛 평가
    taste_evaluation = models.PositiveSmallIntegerField(
        null=True,
        default=50,
        verbose_name="맛 평가",
        help_text="좋다 : 100, 보통 : 50, 싫다 : 0",
    )
    # 개척 작성자 푸이티아이
    fooiyti = models.CharField(
        max_length=4,
        verbose_name="개척 작성자 푸이티아이",
        choices=FOOIYTI_TYPE,
        blank=True,
        null=True,
    )

    # 개척 사진
    image_1 = models.ImageField(
        upload_to=feeds_pioneer_image_upload_url,
        blank=True,
        null=True,
        verbose_name="개척 이미지",
    )
    image_2 = models.ImageField(
        upload_to=feeds_pioneer_image_upload_url,
        blank=True,
        null=True,
        verbose_name="개척 이미지",
    )
    image_3 = models.ImageField(
        upload_to=feeds_pioneer_image_upload_url,
        blank=True,
        null=True,
        verbose_name="개척 이미지",
    )
    image_4 = models.ImageField(
        upload_to=feeds_pioneer_image_upload_url,
        blank=True,
        null=True,
        verbose_name="개척 이미지",
    )
    image_5 = models.ImageField(
        upload_to=feeds_pioneer_image_upload_url,
        blank=True,
        null=True,
        verbose_name="개척 이미지",
    )

    """
        매장 관련
    """
    # 매장
    shop = models.ForeignKey(
        "shops.Shop",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="pioneer",
        db_index=True,
        verbose_name="매장",
    )
    # 매장명
    shop_name = models.CharField(
        max_length=50,
        verbose_name="매장명",
        blank=True,
        null=True,
        help_text="ex) 맵도리탕 수원화서점",
    )
    # 매장 카테고리1
    category1 = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="매장 카테고리1",
        choices=SHOP_CATEGORY,
    )
    # 매장 카테고리2
    category2 = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="매장 카테고리2",
        choices=SHOP_CATEGORY,
    )
    # 매장 카테고리3
    category3 = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="매장 카테고리3",
        choices=SHOP_CATEGORY,
    )
    # 매장 주소
    address = models.CharField(
        max_length=200,
        verbose_name="매장 주소",
        blank=True,
        null=True,
    )

    """
        개척 정보 관련
    """
    # 개척 상태
    state = models.CharField(
        default="CONFIRM",
        max_length=7,
        null=True,
        verbose_name="개척 상태",
        choices=PIONEER_STATE,
    )

    # 에러 메시지
    error_message = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="에러 메시지",
    )

    fooiyti_e = models.PositiveSmallIntegerField(blank=True, null=True, default=50)
    fooiyti_i = models.PositiveSmallIntegerField(blank=True, null=True, default=50)
    fooiyti_n = models.PositiveSmallIntegerField(blank=True, null=True, default=50)
    fooiyti_s = models.PositiveSmallIntegerField(blank=True, null=True, default=50)
    fooiyti_t = models.PositiveSmallIntegerField(blank=True, null=True, default=50)
    fooiyti_f = models.PositiveSmallIntegerField(blank=True, null=True, default=50)
    fooiyti_c = models.PositiveSmallIntegerField(blank=True, null=True, default=50)
    fooiyti_a = models.PositiveSmallIntegerField(blank=True, null=True, default=50)

    # 구독신청한 파티
    subscribe_party = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name="구독신청한 파티",
    )

    # 생성일
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    # 검수 완료일
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="검수 완료일")

    # 반려 사유
    reject_reason = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        verbose_name="개척 반려 사유",
        choices=PIONEER_REJECT_REASON,
        help_text="개척 반려시 반드시 선택해 주세요! 주의) 유저에게 푸시 메시지로 나갑니다!",
    )

    class Meta:
        verbose_name = "4.2 개척 정보"
        verbose_name_plural = "4.2 개척 정보"
