from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from argon2 import PasswordHasher
import uuid
from common import index as Common

from feeds.models import FeedParty

# 성별 초이스
GENDER_TYPE = (
    ("M", "남성"),
    ("F", "여성"),
)

# 소셜 타입 초이스
SOCIAL_TYPE = (
    ("kakao", "카카오"),
    ("apple", "애플"),
)

# 계정 상태 초이스
ACCOUNT_STATE = (
    ("normal", "정상"),
    ("sleep", "휴면"),
    ("withdrawal", "탈퇴"),
)

FEED_STATE = (
    ("subscribe", "구독"),
    ("unsubscribe", "구독취소"),
)

RANK_TYPE = (
    ("ranker", "RANKER"),
    ("platinum", "PLATINUM"),
    ("gold", "GOLD"),
    ("silver", "SILVER"),
    ("bronze", "BRONZE"),
)

PARTY_STATE = (
    ("subscribe", "가입 중"),
    ("confirm", "검수"),
    ("unsubscribe", "미가입"),
    ("reject", "반려"),
    ("expulsion", "추방"),
)


# 휴면 이유 초이스
SLEEP_REASON = (
    ("새 번호 주인이 회원가입을 함", "새 번호 주인이 회원가입을 함"),
    ("새 번호 주인이 전화번호 변경을 함", "새 번호 주인이 전화번호 변경을 함"),
)


def profile_image_upload(instance, filename):
    return f"accounts/{instance.public_id}/profile-image/{uuid.uuid4().hex[:12].upper()}.{filename.split('.')[-1]}"


def party_image_upload(instance, filename):
    return f"accounts/party/{instance.id}/{uuid.uuid4().hex[:12].upper()}.{filename.split('.')[-1]}"


class AccountManager(BaseUserManager):
    def _create_user(self, phone_number=None, password=None, user_type=None, **kwargs):
        if user_type == "social_user":
            account = self.model(**kwargs)
        else:
            if not phone_number:
                raise ValueError("전화번호는 필수입니다")

            account = self.model(phone_number=phone_number, **kwargs)

            if user_type == "user":
                account.password = PasswordHasher().hash(password)
            elif user_type == "super_user":
                account.set_password(password)

        account.save(using=self._db)

    def create_social_user(self, **kwargs):
        kwargs.setdefault("is_admin", False)
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_superuser", False)
        return self._create_user(None, None, "social_user", **kwargs)

    def create_user(self, phone_number, password, **kwargs):
        kwargs.setdefault("is_admin", False)
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, "user", **kwargs)

    def create_superuser(self, phone_number, password, **kwargs):
        kwargs.setdefault("is_admin", True)
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        return self._create_user(phone_number, password, "super_user", **kwargs)


class Account(AbstractBaseUser, PermissionsMixin):
    objects = AccountManager()

    # 계정 pk
    id = models.AutoField(
        primary_key=True,
        unique=True,
        editable=False,
        verbose_name="계정 pk",
    )
    # 계정 공개 pk
    public_id = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="계정 공개 pk",
        db_index=True,
    )

    #############################
    # 장고 기본 유저 필드
    #############################
    # !Delete
    username = models.CharField(max_length=20, verbose_name="이름", blank=True, null=True)
    # !Delete
    last_name = models.CharField(max_length=20, verbose_name="성", blank=True, null=True)
    # !Delete
    first_name = models.CharField(
        max_length=20, verbose_name="이름", blank=True, null=True
    )
    password = models.CharField(
        max_length=100, verbose_name="바밀번호", blank=True, null=True
    )
    is_staff = models.BooleanField(default=False, verbose_name="스태프 권한 여부")
    is_active = models.BooleanField(default=True, verbose_name="계정 활성 여부")
    is_superuser = models.BooleanField(default=False, verbose_name="super 유저 권한 여부")
    is_admin = models.BooleanField(default=False, verbose_name="관리자 권한 여부")
    last_login = models.DateTimeField(auto_now_add=True, verbose_name="마지막 로그인 날짜")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="회원 가입 날짜")
    #############################

    # 소셜 타입
    social_type = models.CharField(
        max_length=10,
        choices=SOCIAL_TYPE,
        verbose_name="소셜 타입",
        blank=True,
        null=True,
    )

    # 소셜 id
    social_id = models.CharField(
        unique=True,
        max_length=50,
        verbose_name="소셜 id",
        blank=True,
        null=True,
        db_index=True,
    )

    # 전화번호
    phone_number = models.CharField(
        unique=True,
        max_length=20,
        verbose_name="전화번호",
        blank=True,
        null=True,
        db_index=True,
    )
    # !Delete
    old_phone_number = models.CharField(
        max_length=20, verbose_name="이전 전화번호", blank=True, null=True
    )
    # !Delete
    state = models.CharField(
        max_length=10,
        choices=ACCOUNT_STATE,
        verbose_name="계정 상태",
        blank=True,
        null=True,
    )
    # !Delete
    sleep_reason = models.CharField(
        max_length=20, choices=SLEEP_REASON, verbose_name="휴면 이유", blank=True, null=True
    )
    # 탈퇴 이유
    withdrawal_reason = models.CharField(
        max_length=300,
        verbose_name="탈퇴 이유",
        blank=True,
        null=True,
    )
    # !Delete
    date_sleep = models.DateTimeField(blank=True, null=True, verbose_name="휴면일")
    # 탈퇴일
    date_withdrawal = models.DateTimeField(blank=True, null=True, verbose_name="탈퇴일")
    # !Delete
    email = models.EmailField(
        unique=True,
        verbose_name="이메일",
        blank=True,
        null=True,
        db_index=True,
    )
    # 닉네임
    nickname = models.CharField(
        unique=True, max_length=20, verbose_name="닉네임", blank=True, null=True
    )
    # 성별
    gender = models.CharField(
        max_length=1,
        choices=GENDER_TYPE,
        blank=True,
        null=True,
        verbose_name="성별",
    )
    # 출생년도
    birth_year = models.PositiveSmallIntegerField(
        verbose_name="출생년도",
        help_text="ex) 1998",
        blank=True,
        null=True,
    )
    # 푸이티아이
    fooiyti = models.ForeignKey(
        "archives.Fooiyti",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="account",
    )
    fooiyti_e_percentage = models.FloatField(blank=True, null=True)
    fooiyti_i_percentage = models.FloatField(blank=True, null=True)
    fooiyti_n_percentage = models.FloatField(blank=True, null=True)
    fooiyti_s_percentage = models.FloatField(blank=True, null=True)
    fooiyti_t_percentage = models.FloatField(blank=True, null=True)
    fooiyti_f_percentage = models.FloatField(blank=True, null=True)
    fooiyti_c_percentage = models.FloatField(blank=True, null=True)
    fooiyti_a_percentage = models.FloatField(blank=True, null=True)

    # 푸이 계정 식별 토큰
    account_token = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="푸이 계정 식별 토큰",
        blank=True,
        null=True,
        db_index=True,
    )
    # OS
    os = models.CharField(max_length=10, verbose_name="OS", blank=True, null=True)
    # 기기 id
    device_id = models.CharField(
        max_length=50, verbose_name="기기 id", blank=True, null=True
    )
    # 앱 버전
    app_version = models.CharField(
        max_length=10, verbose_name="앱 버전", blank=True, null=True
    )
    # fcm 토큰
    fcm_token = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="fcm 토큰"
    )

    # 마케팅 정보 수신 동의 여부
    is_mkt_agree = models.BooleanField(
        blank=True, null=True, verbose_name="마케팅 정보 수신 동의 여부"
    )
    # 마케팅 정보 수신 동의 일자
    date_mkt_agree = models.DateTimeField(
        blank=True, null=True, verbose_name="마케팅 정보 수신 동의 일자"
    )
    # 위치 정보 이용 동의 여부
    is_loc_agree = models.BooleanField(
        default=True, null=True, verbose_name="위치 정보 이용 동의 여부"
    )
    # 위치 정보 이용 동의 일자
    date_loc_agree = models.DateTimeField(
        auto_now_add=True, blank=True, null=True, verbose_name="위치 정보 이용 동의 일자"
    )
    # 14세 이상 여부
    is_over_fourteen = models.BooleanField(
        default=True, null=True, verbose_name="14세 이상 여부"
    )

    # 프로필 이미지
    profile_image = models.ImageField(
        upload_to=profile_image_upload, null=True, blank=True, verbose_name="프로필 사진"
    )
    # 자기소개
    introduction = models.CharField(
        max_length=100, verbose_name="자기소개", blank=True, null=True
    )

    # !Delete
    pioneer_count = models.PositiveIntegerField(
        default=0,
        verbose_name="계정 개척 수",
    )

    # 계정 랭크
    rank = models.CharField(
        max_length=10, choices=RANK_TYPE, null=True, blank=True, verbose_name="계정 랭크"
    )

    # 유저 로그인 ID
    USERNAME_FIELD = "phone_number"
    # 가입 시 반드시 필요한 필드 설정
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "1.1 회원 기본 정보"
        verbose_name_plural = "1.1 회원 기본 정보"

    def __str__(self):
        if self.nickname:
            return self.nickname
        else:
            return "탈퇴한 회원"


# 피드 보관함
class Storage(models.Model):
    # 피드보관함 pk
    id = models.AutoField(
        primary_key=True,
        unique=True,
        editable=False,
        verbose_name="피드보관함 pk",
    )

    # 계정
    account = models.ForeignKey(
        "accounts.Account",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="storage",
    )
    # 피드
    feed = models.ForeignKey(
        "feeds.Feed",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="storage",
    )

    state = models.CharField(
        max_length=12,
        choices=FEED_STATE,
        default="subscribe",
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = [["account", "feed"]]
        verbose_name = "1.2 회원 피드 보관 정보"
        verbose_name_plural = "1.2 회원 피드 보관 정보"


# 피드 좋아요
class Like(models.Model):
    # 피드좋아요 pk
    id = models.AutoField(
        primary_key=True,
        unique=True,
        editable=False,
        verbose_name="피드좋아요 pk",
    )

    # 계정
    account = models.ForeignKey(
        "accounts.Account",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="like",
    )
    # 피드
    feed = models.ForeignKey(
        "feeds.Feed",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="like",
    )

    state = models.CharField(
        max_length=12,
        choices=FEED_STATE,
        default="subscribe",
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = [["account", "feed"]]
        verbose_name = "1.3 회원 피드 좋아요 정보"
        verbose_name_plural = "1.3 회원 피드 좋아요 정보"


# 파티 테이블
class Party(models.Model):
    # 파티 pk
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="파티 pk",
        db_index=True,
    )

    # 파티장
    owner = models.ForeignKey(
        "accounts.Account",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="party",
    )

    # 파티원 수
    account_count = models.IntegerField(
        blank=True, null=True, default=0, verbose_name="파티원 수"
    )
    # 파티 피드 수
    feed_count = models.IntegerField(
        blank=True, null=True, default=0, verbose_name="파티 피드 수"
    )

    # 파티명
    name = models.CharField(max_length=50, verbose_name="파티명", blank=True, null=True)
    # 파티 소개글
    introduction = models.CharField(
        max_length=100, verbose_name="파티 소개글", blank=True, null=True
    )
    # 파티 프로필 이미지
    party_image = models.ImageField(
        upload_to=party_image_upload, null=True, blank=True, verbose_name="파티 프로필 이미지"
    )
    # 생성일
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")

    def save(self, *args, **kwargs):
        self.account_count = AccountParty.objects.filter(
            party=self, state=Common.PartyState.SUBSCRIBE
        ).count()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "1.4 파티 정보"
        verbose_name_plural = "1.4 파티 정보"


# 유저 파티 중개 테이블
class AccountParty(models.Model):
    # 유저 파티 중개 테이블 pk
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="유저 파티 중개 테이블 pk",
        db_index=True,
    )

    # 계정
    account = models.ForeignKey(
        "accounts.Account",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="account_party",
    )
    # 파티
    party = models.ForeignKey(
        "accounts.Party",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="account_party",
    )

    state = models.CharField(
        max_length=12,
        choices=PARTY_STATE,
        default="confirm",
        null=True,
        blank=True,
    )
    # 생성일
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")

    class Meta:
        unique_together = [["account", "party"]]
        verbose_name = "1.4.1 유저, 파티 관계 정보"
        verbose_name_plural = "1.4.1 유저, 파티 관계 정보"
