from django.db import models
from common import index as Common

SEARCH_SPOT_TYPE = (
    ("landmark", "랜드마크"),
    ("university", "대학교"),
    ("subway", "지하철역"),
    ("district", "행정지역"),
)
# 위치 검색 테이블
class SearchSpot(models.Model):
    id = models.AutoField(
        primary_key=True,
        unique=True,
        editable=False,
        db_index=True,
        verbose_name="위치 검색 pk"
    )
    type = models.CharField(
        choices=SEARCH_SPOT_TYPE,
        max_length=10,
        null=True,
        blank=True,
        verbose_name="위치 타입"
    )
    name = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="위치 명"
    )
    address = models.CharField(
        max_length=200,
        verbose_name="매장 주소",
        blank=True,
        null=True,
    )
    longitude = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="경도",
        db_index=True,
        help_text="매장 주소 저장 시 자동으로 채워짐",
    )
    latitude = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="위도",
        db_index=True,
        help_text="매장 주소 저장 시 자동으로 채워짐",
    )

    class Meta:
        verbose_name = "5.1 위치 검색 정보"
        verbose_name_plural = "5.1 위치 검색 정보"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.address = Common.synchronize_address(self.address)
        if not self.longitude:
            self.longitude,self.latitude= Common.convert_address_to_coordinate(self.address)
        super().save(*args, **kwargs)

