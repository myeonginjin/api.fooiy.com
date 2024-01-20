from random import choices
from django.db import models

import uuid
from common import index as Common

# 아카이브 이미지 타입 초이스
ARCHIVE_IMAGE_TYPE = (
    ("OB", "온보딩"),
    ("DPI", "기본 프로필 이미지"),
    ("NSI", "주변 매장 없을 때 이미지"),
    ("NSS", "검색 매장 없을 때 이미지"),
    ("NSF", "보관함이 비었을 때 이미지"),
    ("NMF", "마이페이지 피드가 없을 때 이미지"),
    ("P", "개척"),
    ("R", "기록"),
    ("F", "피드"),
    ("TE", "맛 평가"),
    ("N", "공지사항"),
    ("AD", "광고"),
    ("FR", "푸이티아이 결과"),
    ("RI", "랭커 푸시 알림 이미지"),
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
# 푸이티아이 검사 초이스
FOOIYTI_TEST_TYPE = (
    ("web", "웹"),
    ("app", "어플"),
)

# 아카이브 이미지 타입 초이스
ADVERTISEMENT_TYPE = (
    ("BANNER", "배너"),
    ("FEED", "피드"),
)


# 문의 타입 초이스
SUGGESTION_TYPE = (
    ("IMP", "개선 사항"),
    ("FR", "기능 추가 요청"),
    ("BUG", "버그 신고"),
    ("AC", "계정 관련"),
    ("AD", "광고 제의"),
    ("ETC", "기타 피드백"),
    ("TIP_OFF", "메뉴판 정보 오류 제보"),
)


# 아카이브 이미지 타입 초이스
ADVERTISEMENT_TYPE = (
    ("BANNER", "배너"),
    ("FEED", "피드"),
)


# 푸시 타입 초이스
PUSHNOTIFICATION_TYPE = (
    ("PIONEER", "개척"),
    ("STORAGE", "보관"),
    ("LIKE", "좋아요"),
    ("COMMENT", "댓글"),
    ("RANK", "랭크"),
    ("PARTY", "파티"),
    ("OVERALL_NOTICE", "전체공지"),
)

# 맛 평가 이미지 타입
TASTE_EVALUATION_IMAGE_TYPE = (("border", "테두리 있는 이모지"), ("no_border", "테두리 없는 이모지"))


def archives_image_upload_url(instance, filename):
    if instance.type == Common.ArchivesImageType.OB:
        return f"archives/image/onboarding/{instance.id}.{filename.split('.')[-1]}"
    elif instance.type == Common.ArchivesImageType.DPI:
        return f"archives/image/default/profile-image.{filename.split('.')[-1]}"
    elif instance.type == Common.ArchivesImageType.NSI:
        return f"archives/image/no-shop-image.{filename.split('.')[-1]}"
    elif instance.type == Common.ArchivesImageType.NSS:
        return f"archives/image/no-shop-search-image.{filename.split('.')[-1]}"
    elif instance.type == Common.ArchivesImageType.NSF:
        return f"archives/image/no-storage-feed-image.{filename.split('.')[-1]}"
    elif instance.type == Common.ArchivesImageType.NMF:
        return f"archives/image/no-mypage-feed-image.{filename.split('.')[-1]}"
    elif instance.type == Common.ArchivesImageType.P:
        return f"feeds/pioneer/{instance.account.public_id}/{instance.pioneer.id}/{uuid.uuid4().hex[:12].upper()}.{filename.split('.')[-1]}"
    elif instance.type == Common.ArchivesImageType.R:
        return f"feeds/record/{instance.account.public_id}/{instance.record.id}/{uuid.uuid4().hex[:12].upper()}.{filename.split('.')[-1]}"
    elif instance.type == Common.ArchivesImageType.F:
        return f"feeds/record/{instance.account.public_id}/{instance.feed.id}/{uuid.uuid4().hex[:12].upper()}.{filename.split('.')[-1]}"
    elif instance.type == Common.ArchivesImageType.TE:
        return f"archives/image/taste-evaluation/{instance.taste_evaluation.type}/{instance.taste_evaluation.score}.{filename.split('.')[-1]}"
    elif instance.type == Common.ArchivesImageType.N:
        return f"archives/image/notice/{instance.id}.{filename.split('.')[-1]}"
    elif instance.type == Common.ArchivesImageType.AD:
        return f"archives/image/advertisement/{instance.id}.{filename.split('.')[-1]}"
    elif instance.type == Common.ArchivesImageType.FR:
        return f"archives/image/fooiyti-result/{instance.id}.{filename.split('.')[-1]}"
    elif instance.type == Common.ArchivesImageType.RI:
        return f"archives/image/ranker-image/{instance.order}/{instance.id}.{filename.split('.')[-1]}"


def pushnotification_image_upload_url(instance, filename):
    return f"pushnotification/{instance.type}/{instance.receiver.public_id}/{instance.id}.{filename.split('.')[-1]}"


# 이미지 테이블
class Image(models.Model):
    # 이미지 pk
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="이미지 pk",
    )
    # 정렬 순서
    order = models.PositiveSmallIntegerField(
        default=1, verbose_name="정렬 순서", help_text="ex) 1"
    )
    # 이미지 타입
    type = models.CharField(
        max_length=5,
        choices=ARCHIVE_IMAGE_TYPE,
        null=False,
        verbose_name="이미지 타입",
        default="",
    )
    # 계정
    account = models.ForeignKey(
        "accounts.Account",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="image",
    )
    # 매장
    shop = models.ForeignKey(
        "shops.Shop",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="image",
    )
    # 개척
    pioneer = models.ForeignKey(
        "feeds.Pioneer",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="image",
    )
    # 기록
    record = models.ForeignKey(
        "feeds.Record",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="image",
    )
    # 피드
    feed = models.ForeignKey(
        "feeds.Feed",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="image",
    )
    # 메뉴
    menu = models.ForeignKey(
        "shops.Menu",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="image",
    )
    # 메뉴
    taste_evaluation = models.ForeignKey(
        "TasteEvaluation",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="image",
    )
    # 공지 사항
    notice = models.ForeignKey(
        "Notice",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="image",
    )
    # 공지 사항
    advertisement = models.ForeignKey(
        "Advertisement",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="image",
    )
    # 푸이티아이
    fooiyti = models.ForeignKey(
        "Fooiyti",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="image",
    )

    # 이미지
    image = models.ImageField(
        upload_to=archives_image_upload_url, blank=True, null=False, verbose_name="이미지"
    )

    # 생성일
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")

    class Meta:
        verbose_name = "3.1 아카이브 이미지 정보"
        verbose_name_plural = "3.1 아카이브 이미지 정보"


# 푸이티아이 테이블
class Fooiyti(models.Model):
    # 푸이티아이 pk
    id = models.AutoField(
        primary_key=True,
        unique=True,
        editable=False,
        verbose_name="푸이티아이 pk",
    )
    # 푸이티아이
    fooiyti = models.CharField(
        max_length=4,
        choices=FOOIYTI_TYPE,
        blank=True,
        null=True,
        verbose_name="푸이티아이",
    )
    # 푸이티아이 별명
    nickname = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="푸이티아이 별명",
    )
    # 푸이티아이 설명
    description = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="푸이티아이 설명",
    )

    class Meta:
        verbose_name = "3.2 푸이티아이 정보"
        verbose_name_plural = "3.2 푸이티아이 정보"

    def __str__(self):
        return self.fooiyti


# 푸이티아이 질문지 테이블
class FooiytiQuestion(models.Model):
    # 푸이티아이 질문지 pk
    id = models.AutoField(
        primary_key=True,
        unique=True,
        editable=False,
        verbose_name="푸이티아이 질문지 pk",
    )
    # 정렬 순서
    order = models.PositiveSmallIntegerField(
        default=1, verbose_name="정렬 순서", help_text="ex) 1"
    )
    # 질문
    question = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="질문",
    )

    # 답 복수 선택 가능
    is_multi_answer = models.BooleanField(default=False, verbose_name="답 복수 선택 가능")
    # 답 후보 1
    answer_1 = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="답 후보 1",
    )
    # 답 결과 1
    result_1 = models.JSONField(
        null=True,
        blank=True,
        verbose_name="답 결과 1",
    )
    # 답 후보 2
    answer_2 = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="답 후보 2",
    )
    # 답 결과 2
    result_2 = models.JSONField(
        null=True,
        blank=True,
        verbose_name="답 결과 2",
    )
    # 답 후보 3
    answer_3 = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="답 후보 3",
    )
    # 답 결과 3
    result_3 = models.JSONField(
        null=True,
        blank=True,
        verbose_name="답 결과 3",
    )
    # 답 후보 4
    answer_4 = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="답 후보 4",
    )
    # 답 결과 4
    result_4 = models.JSONField(
        null=True,
        blank=True,
        verbose_name="답 결과 4",
    )

    type = models.CharField(
        max_length=3,
        choices=FOOIYTI_TEST_TYPE,
        null=True,
        blank=True,
        verbose_name="웹 | 앱",
    )

    class Meta:
        verbose_name = "3.3 푸이티아이 질문지 정보"
        verbose_name_plural = "3.3 푸이티아이 질문지 정보"


# 맛 평가 테이블
class TasteEvaluation(models.Model):
    # 맛 평가 pk
    id = models.AutoField(
        primary_key=True,
        unique=True,
        editable=False,
        verbose_name="맛 평가 pk",
    )

    # 이미지 타입
    type = models.CharField(
        choices=TASTE_EVALUATION_IMAGE_TYPE,
        max_length=10,
        null=True,
        blank=True,
    )

    # 점수
    score = models.PositiveSmallIntegerField(
        default=10, verbose_name="점수", help_text="ex) 10"
    )

    class Meta:
        verbose_name = "3.4 맛 평가 정보"
        verbose_name_plural = "3.4 맛 평가 정보"


# 공지사항 정보 테이블
class Notice(models.Model):
    # 공지사항 정보 pk
    id = models.AutoField(
        primary_key=True,
        unique=True,
        editable=False,
        verbose_name="공지사항 정보 pk",
    )
    # 공지사항 제목
    title = models.CharField(
        max_length=30,
        verbose_name="공지사항 제목",
        blank=True,
        null=True,
        help_text="긴급 공지 사용 시 작성",
    )
    # 공지사항 내용
    content = models.CharField(
        max_length=200,
        verbose_name="공지사항 내용",
        blank=True,
        null=True,
        help_text="긴급 공지 사용 시 작성",
    )
    # 긴급공지 여부
    is_emergency = models.BooleanField(
        default=False, null=True, blank=True, verbose_name="긴급공지 여부"
    )
    # 공지사항 순서
    order = models.PositiveSmallIntegerField(
        null=True, blank=True, verbose_name="공지사항 순서", default=100
    )
    # 공지사항 공개 여부
    is_exposure = models.BooleanField(
        default=True, null=True, blank=True, verbose_name="공지사항 공개 여부"
    )
    # 공지사항 시작일
    date_event_start = models.DateTimeField(
        null=True, blank=True, verbose_name="공지사항 시작일"
    )
    # 공지사항 종료일
    date_event_finish = models.DateTimeField(
        null=True, blank=True, verbose_name="공지사항 종료일"
    )

    class Meta:
        verbose_name = "3.5 공지사항 정보"
        verbose_name_plural = "3.5 공지사항 정보"


# 버전 정보 테이블
class Version(models.Model):
    # 버전
    version = models.CharField(
        max_length=15,
        verbose_name="버전",
        blank=True,
        null=True,
    )
    # os
    os = models.CharField(
        max_length=10,
        verbose_name="OS",
        blank=True,
        null=True,
    )
    # 변경 내역
    change_history = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name="변경 내역",
    )
    # 강제 업데이트 필요 유무
    is_update_required = models.BooleanField(
        default=False,
        verbose_name="강제 업데이트 필요 유무",
    )
    # 버전 업데이트 일시
    date_updated = models.DateTimeField(
        auto_now_add=True,
        verbose_name="버전 업데이트 일시",
    )

    class Meta:
        verbose_name = "3.6 버전 정보"
        verbose_name_plural = "3.6 버전 정보"


# 광고 테이블
class Advertisement(models.Model):
    # 광고 pk
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="광고 pk",
    )

    # 광고 유형
    type = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        choices=ADVERTISEMENT_TYPE,
        verbose_name="광고 유형",
    )

    # 광고주
    advertiser = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="광고주",
        help_text="내부 광고 : 푸이",
    )

    # 타이틀
    title = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        verbose_name="광고 타이틀",
    )

    # 광고 공개 여부
    is_exposure = models.BooleanField(
        default=True, null=True, blank=True, verbose_name="광고 공개 여부"
    )

    # 생성일
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")

    class Meta:
        verbose_name = "3.7 광고 정보"
        verbose_name_plural = "3.7 광고 정보"


# 문의 테이블
class Suggestion(models.Model):
    # 문의 pk
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="문의 pk",
    )

    # 문의 유형
    type = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        choices=SUGGESTION_TYPE,
        verbose_name="문의 유형",
    )

    # 문의자
    account = models.ForeignKey(
        "accounts.Account",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="suggestion",
        verbose_name="문의자",
        db_index=True,
    )

    # 내용
    content = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="내용",
    )

    # 생성일
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")

    class Meta:
        verbose_name = "3.8 문의 정보"
        verbose_name_plural = "3.8 문의 정보"


# 주소 클러스터 테이블
class AddressCluster(models.Model):
    # 뎁스 pk
    id = models.AutoField(
        primary_key=True,
        unique=True,
        editable=False,
        verbose_name="주소 클러스터 pk",
    )

    # 상위 뎁스 정보
    parent_depth = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="address_depth",
        verbose_name="상위 뎁스 정보",
    )

    # 뎁스
    depth = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name="뎁스",
    )

    # 뎁스 명
    name = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name="뎁스 명",
    )

    # 경도
    longitude = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="경도",
        db_index=True,
    )
    # 위도
    latitude = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="위도",
        db_index=True,
    )

    # 매장 수
    count = models.PositiveIntegerField(
        default=0,
        verbose_name="매장 수",
    )

    class Meta:
        verbose_name = "3.9 주소 클러스터 정보"
        verbose_name_plural = "3.9 주소 클러스터 정보"

    def __str__(self):
        return self.name


# 푸시 알림 테이블
class PushNotification(models.Model):
    # 푸시 알림 pk
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="푸시 알림 pk",
    )

    # 푸시 알림 계정
    account = models.ForeignKey(
        "accounts.Account",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="push_notification",
        verbose_name="푸시 알림 계정",
    )

    # 푸시 보내는 계정
    sender = models.ForeignKey(
        "accounts.Account",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="sender",
        verbose_name="푸시 보내는 계정",
    )

    # 푸시 받는 계정
    receiver = models.ForeignKey(
        "accounts.Account",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="receiver",
        verbose_name="푸시 받는 계정",
    )

    # 피드
    feed = models.ForeignKey(
        "feeds.Feed",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="push_notification",
        verbose_name="피드",
    )

    # 파티
    party = models.ForeignKey(
        "accounts.Party",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="push_notification",
        verbose_name="파티",
    )

    # 개척
    pioneer = models.ForeignKey(
        "feeds.Pioneer",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="push_notification",
        verbose_name="개척",
    )

    # 타입
    type = models.CharField(
        choices=PUSHNOTIFICATION_TYPE,
        max_length=20,
        null=True,
        verbose_name="푸시 타입",
        default="PIONEER",
    )

    # 푸시 알림 제목
    title = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="푸시 알림 제목",
    )
    # 푸시 알림 내용
    content = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        verbose_name="푸시 알림 내용",
    )

    # 이미지
    image = models.ImageField(
        upload_to=pushnotification_image_upload_url,
        blank=True,
        null=True,
        verbose_name="이미지",
    )

    # 생성일
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")

    class Meta:
        verbose_name = "3.10 푸시 알림 정보"
        verbose_name_plural = "3.10 푸시 알림 정보"
