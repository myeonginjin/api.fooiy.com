from django.db import models, transaction
from django.utils.text import slugify

import uuid

from common import index as Common

# 매장 카테고리 초이스
SHOP_CATEGORY = (
    ("CUTLET", "돈까스"),
    ("RAW/SUSHI", "회/초밥"),
    ("JAPANESE", "일식"),
    ("CHINESE", "중식"),
    ("CHICKEN", "치킨"),
    ("KOREAN", "한식"),
    ("SEAFOOD", "해산물"),
    ("NOODLE", "국수"),
    ("SNACKBAR", "분식"),
    ("BURGER", "햄버거"),
    ("PIZZA", "피자"),
    ("WESTERN", "양식"),
    ("MEAT/ROAST", "고기/구이"),
    ("PETTITOES/BOSSAM", "족발/보쌈"),
    ("ASIAN", "아시안"),
    ("TOAST/SANDWICH", "토스트/샌드위치"),
    ("LUNCHBOX/PORRIDGE", "도시락/죽"),
    ("PUB", "요리주점"),
    ("SALAD", "샐러드"),
    ("BAKERY/CAFE", "베이커리/카페"),
)
# 메뉴 카테고리 초이스
MENU_CATEGORY = (
    ("MAIN", "메인"),
    ("SET", "세트"),
    ("SIDE", "사이드"),
    ("BEVERAGE", "음료"),
    ("LIQUOR", "주류"),
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
# 위도, 경도 미터당 비율
LONGITUDE_METER_RATIO = 0.000015
LATITUDE_METER_RATIO = 0.00001


def thumbnail_upload_url(instance, filename):
    return f"shops/{str(instance.public_id)}/thumbnail/{uuid.uuid4().hex[:12].upper()}.{filename.split('.')[-1]}"


def menu_image_upload_url(instance, filename):
    return f"shops/{str(instance.shop.public_id)}/menu-image/{uuid.uuid4().hex[:12].upper()}.{filename.split('.')[-1]}"


# 매장 정보 테이블
class Shop(models.Model):
    # 매장 pk
    id = models.AutoField(
        primary_key=True,
        unique=True,
        editable=False,
        verbose_name="매장 pk",
    )

    # 매장 공개 pk
    public_id = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="매장 공개 pk",
    )

    """
        개척자 정보
    """
    # 매장 개척자
    account = models.ForeignKey(
        "accounts.Account",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="shop",
        verbose_name="개척자",
        db_index=True,
    )

    """
        매장 기본 정보
    """
    # 매장명
    name = models.CharField(
        max_length=50,
        verbose_name="매장명",
        blank=True,
        null=True,
        help_text="ex) 맵도리탕 수원화서점",
    )
    # 매장 노출 여부
    is_exposure = models.BooleanField(default=True, blank=True, verbose_name="매장 노출 여부")
    # 메뉴 최소 가격
    menu_min_price = models.PositiveIntegerField(
        verbose_name="메뉴 최소 가격",
        blank=True,
        null=True,
    )
    # 메뉴 최대 가격
    menu_max_price = models.PositiveIntegerField(
        verbose_name="메뉴 최대 가격",
        blank=True,
        null=True,
    )

    """
        매장 주소
    """
    # 매장 주소
    address = models.CharField(
        max_length=200,
        verbose_name="매장 주소",
        blank=True,
        null=True,
    )
    # 매장 행정 구역1(도, 광역시, 자치시)
    address_depth1 = models.CharField(
        max_length=15,
        verbose_name="매장 행정 구역1(도, 광역시, 자치시)",
        blank=True,
        null=True,
        help_text="매장 주소 저장 시 자동으로 채워짐",
    )
    # 매장 행정 구역2(시, 구, 군)
    address_depth2 = models.CharField(
        max_length=15,
        verbose_name="매장 행정 구역2(시, 구, 군)",
        blank=True,
        null=True,
        help_text="매장 주소 저장 시 자동으로 채워짐",
    )
    # 매장 행정 구역3(읍, 면, 동)
    address_depth3 = models.CharField(
        max_length=15,
        verbose_name="매장 행정 구역2(읍, 면, 동)",
        blank=True,
        null=True,
        help_text="매장 주소 저장 시 자동으로 채워짐",
    )
    # 경도
    longitude = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="경도",
        db_index=True,
        help_text="매장 주소 저장 시 자동으로 채워짐",
    )
    # 위도
    latitude = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="위도",
        db_index=True,
        help_text="매장 주소 저장 시 자동으로 채워짐",
    )

    # 카테고리
    category = models.ManyToManyField(
        "ShopCategory", blank=True, verbose_name="카테고리", help_text="여러개 선택 가능"
    )
    # 배지
    badge = models.ManyToManyField(
        "ShopBadge", blank=True, verbose_name="배지", help_text="여러개 선택 가능"
    )

    # 생성일
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")

    # 슬러그
    slug = models.SlugField(
        blank=True,
        null=True,
        allow_unicode=True,
        unique=True,
        verbose_name="슬러그",
        db_index=True,
    )

    # 썸네일
    thumbnail = models.ImageField(
        upload_to=thumbnail_upload_url, blank=True, null=True, verbose_name="썸네일"
    )

    class Meta:
        verbose_name = "2.1 매장 정보"
        verbose_name_plural = "2.1 매장 정보"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not (self.longitude and self.latitude):
            self.longitude, self.latitude = Common.convert_address_to_coordinate(
                self.address
            )
            (
                self.address_depth1,
                self.address_depth2,
                self.address_depth3,
            ) = Common.convert_coordinate_to_address(self.longitude, self.latitude)
        if not self.slug:
            trimed_name = self.name.replace(" ", "")

            self.slug = slugify(
                f"{trimed_name} {self.address_depth1} {self.address_depth2} {self.address_depth3}",
                allow_unicode=True,
            )

        super().save(*args, **kwargs)


class ShopCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "2.1.1 매장 정보 (카테고리)"
        verbose_name_plural = "2.1.1 매장 정보 (카테고리)"


class ShopBadge(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "2.1.2 매장 정보 (배지)"
        verbose_name_plural = "2.1.2 매장 정보 (배지)"


# 매장 점수 테이블
class ShopScore(models.Model):
    shop = models.OneToOneField(
        Shop,
        on_delete=models.CASCADE,
        null=True,
    )
    # 매장 피드 평균 점수
    score = models.PositiveSmallIntegerField(
        default=50,
        verbose_name="매장 피드 평균 점수",
    )
    # 피드 개수
    feed_count = models.PositiveIntegerField(
        verbose_name="피드 개수",
        blank=True,
        null=True,
        default=0,
    )
    # 푸이슐랭 여부
    is_yummy = models.BooleanField(
        default=False,
        verbose_name="푸이슐랭 여부",
    )

    # ENTA 점수
    enta_score = models.SmallIntegerField(
        default=50,
        verbose_name="ENTA 점수",
    )
    # ENTC 점수
    entc_score = models.SmallIntegerField(
        default=50,
        verbose_name="ENTC 점수",
    )
    # ENFA 점수
    enfa_score = models.SmallIntegerField(
        default=50,
        verbose_name="ENFA 점수",
    )
    # ENFC 점수
    enfc_score = models.SmallIntegerField(
        default=50,
        verbose_name="ENFC 점수",
    )

    # ESTA 점수
    esta_score = models.SmallIntegerField(
        default=50,
        verbose_name="ESTA 점수",
    )
    # ESTC 점수
    estc_score = models.SmallIntegerField(
        default=50,
        verbose_name="ESTC 점수",
    )
    # ESFA 점수
    esfa_score = models.SmallIntegerField(
        default=50,
        verbose_name="ESFA 점수",
    )
    # ESFC 점수
    esfc_score = models.SmallIntegerField(
        default=50,
        verbose_name="ESFC 점수",
    )

    # INTA 점수
    inta_score = models.SmallIntegerField(
        default=50,
        verbose_name="INTA 점수",
    )
    # INTC 점수
    intc_score = models.SmallIntegerField(
        default=50,
        verbose_name="INTC 점수",
    )
    # INFA 점수
    infa_score = models.SmallIntegerField(
        default=50,
        verbose_name="INFA 점수",
    )
    # INFC 점수
    infc_score = models.SmallIntegerField(
        default=50,
        verbose_name="INFC 점수",
    )

    # ISTA 점수
    ista_score = models.SmallIntegerField(
        default=50,
        verbose_name="ISTA 점수",
    )
    # ISTC 점수
    istc_score = models.SmallIntegerField(
        default=50,
        verbose_name="ISTC 점수",
    )
    # ISFA 점수
    isfa_score = models.SmallIntegerField(
        default=50,
        verbose_name="ISFA 점수",
    )
    # ISFC 점수
    isfc_score = models.SmallIntegerField(
        default=50,
        verbose_name="ISFC 점수",
    )

    class Meta:
        verbose_name = "2.1.3 매장 정보 (점수)"
        verbose_name_plural = "2.1.3 매장 정보 (점수)"


# 매장 푸이티아이
class ShopFooiyti(models.Model):
    shop = models.OneToOneField(
        Shop,
        on_delete=models.CASCADE,
        null=True,
    )
    fooiyti = models.CharField(
        choices=FOOIYTI_TYPE,
        blank=True,
        null=True,
        max_length=4,
        verbose_name="FOOIYTI",
    )
    feed_count = models.PositiveIntegerField(
        verbose_name="푸이티아이 평가 개수",
        blank=True,
        null=True,
        default=0,
    )
    e_percentage = models.SmallIntegerField(blank=True, null=True, default=50)
    i_percentage = models.SmallIntegerField(blank=True, null=True, default=50)
    s_percentage = models.SmallIntegerField(blank=True, null=True, default=50)
    n_percentage = models.SmallIntegerField(blank=True, null=True, default=50)
    t_percentage = models.SmallIntegerField(blank=True, null=True, default=50)
    f_percentage = models.SmallIntegerField(blank=True, null=True, default=50)
    a_percentage = models.SmallIntegerField(blank=True, null=True, default=50)
    c_percentage = models.SmallIntegerField(blank=True, null=True, default=50)

    class Meta:
        verbose_name = "2.1.4 매장 정보 (푸이티아이)"
        verbose_name_plural = "2.1.4 매장 정보 (푸이티아이)"

    def __str__(self):
        return self.shop.name

    def save(self, *args, **kwargs):
        shop_fooiyti = ""
        shop_fooiyti += "E" if self.e_percentage >= self.i_percentage else "I"
        shop_fooiyti += "S" if self.s_percentage >= self.n_percentage else "N"
        shop_fooiyti += "T" if self.t_percentage >= self.f_percentage else "F"
        shop_fooiyti += "A" if self.a_percentage >= self.c_percentage else "C"
        if self.fooiyti != shop_fooiyti:
            self.fooiyti = shop_fooiyti
        super().save(*args, **kwargs)


# 매장 메뉴 테이블
class Menu(models.Model):
    # 메뉴 pk
    id = models.AutoField(
        primary_key=True,
        unique=True,
        editable=False,
        verbose_name="메뉴 pk",
    )
    shop = models.ForeignKey(
        Shop,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="menu",
        verbose_name="매장",
        db_index=True,
    )

    # 이름
    name = models.CharField(
        max_length=50,
        verbose_name="이름",
        blank=True,
        null=True,
        help_text="ex) 무뼈 닭발",
    )
    # 가격
    price = models.PositiveIntegerField(
        default=0,
        verbose_name="가격",
        help_text="ex) 12500",
    )

    # 대표 메뉴 여부
    is_best = models.BooleanField(
        null=True,
        blank=True,
        default=False,
        verbose_name="대표 메뉴 여부",
        help_text="매장의 대표메뉴 인지",
    )
    # 인기 메뉴 여부
    is_popular = models.BooleanField(
        null=True,
        blank=True,
        default=False,
        verbose_name="인기 메뉴 여부",
        help_text="매장의 인기 메뉴인지",
    )

    # 카테고리
    category = models.CharField(
        max_length=10,
        choices=MENU_CATEGORY,
        blank=True,
        null=True,
        verbose_name="카테고리",
    )

    class Meta:
        verbose_name = "2.2 매장 메뉴 정보"
        verbose_name_plural = "2.2 매장 메뉴 정보"

    def __str__(self):
        return self.name
