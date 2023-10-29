from django import forms
from django.contrib import admin, messages
from django.db import transaction

from common import index as Common
from archives.models import Image
from shops.models import Shop, Menu, ShopScore, ShopFooiyti
from feeds.models import PIONEER_REJECT_REASON, FeedFooiyti, FeedParty
from archives.helpers import index as ArchivesHelpers
from accounts.helpers import index as AccountsHelpers
from web.helpers import index as WebHelpers


class FeedFooiytiInline(admin.TabularInline):
    model = FeedFooiyti


class FeedPartyInline(admin.TabularInline):
    model = FeedParty


class FeedImageInline(admin.TabularInline):
    model = Image
    exclude = [
        "account",
        "pioneer",
        "record",
        "taste_evaluation",
        "notice",
        "advertisement",
        "fooiyti",
    ]
    extra = 0


class FeedAdmin(admin.ModelAdmin):
    search_fields = ("id", "account__nickname", "shop__name", "menu__name")
    list_display = [
        "id",
        "shop",
        "account",
        "menu",
        "description",
        "taste_evaluation",
        "is_exposure",
        "created_at",
    ]
    list_display_link = ["id"]
    ordering = ["-created_at"]
    list_per_page = 15
    raw_id_fields = ["shop", "account", "menu"]
    inlines = (FeedFooiytiInline, FeedPartyInline, FeedImageInline)

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("created_at",)
        form = super(FeedAdmin, self).get_form(request, obj, **kwargs)
        return form


class FeedCommentAdmin(admin.ModelAdmin):
    search_fields = ("id", "writer__nickname", "content", "feed__id", "parent__id")
    list_display = [
        "id",
        "writer",
        "parent",
        "order",
        "created_at",
    ]
    list_display_link = ["id"]
    ordering = ["-created_at"]
    list_per_page = 15
    raw_id_fields = ["feed", "parent", "writer"]


class RecordAdmin(admin.ModelAdmin):
    search_fields = ("shop__name", "menu__name")
    list_display = [
        "id",
        "shop",
        "account",
        "menu",
        "comment",
        "taste_evaluation",
        "is_exposure",
        "created_at",
    ]
    list_display_link = ["id"]
    ordering = ["-created_at"]
    list_per_page = 15
    raw_id_fields = ["shop", "account", "menu"]

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("created_at",)
        form = super(RecordAdmin, self).get_form(request, obj, **kwargs)
        return form


class PioneerAdmin(admin.ModelAdmin):
    search_fields = ("shop_name", "menu_name")
    list_display = [
        "shop_name",
        "state",
        "menu_name",
        "menu_price",
        "account",
        "comment",
        "address",
        "created_at",
    ]
    list_display_link = ["shop_name"]
    ordering = ["-created_at"]
    list_per_page = 15
    raw_id_fields = ["account", "shop", "menu"]

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("updated_at",)
        form = super(PioneerAdmin, self).get_form(request, obj, **kwargs)
        return form

    def save_model(self, request, obj, form, change):
        _type = None
        if request.POST.get(Common.PioneerCheckType.SUCCESS):
            _type = Common.ShopMainCategory.COMMON
        elif request.POST.get(Common.PioneerCheckType.PUB):
            _type = Common.ShopMainCategory.PUB
        elif request.POST.get(Common.PioneerCheckType.CAFE):
            _type = Common.ShopMainCategory.CAFE

        if _type:
            category1, category2, category3 = (
                obj.category1,
                obj.category2,
                obj.category3,
            )
            obj.address = Common.synchronize_address(obj.address)
            try:
                pioneer = WebHelpers.register_pioneer(
                    pioneer=obj,
                    shop_name=obj.shop_name,
                    address=obj.address,
                    menu_name=obj.menu_name,
                    menu_price=obj.menu_price,
                    menu_category=obj.menu_category,
                    category1=category1,
                    category2=category2,
                    category3=category3,
                    _type=_type,
                )

                #### 개척 등록 및 푸시 알림 로직 ####
                if WebHelpers.feed_register(pioneer):
                    #### 계정 랭크 변화 확인 및 푸시 로직 ####
                    AccountsHelpers.CheckRank.check_change_rank(
                        account=pioneer.account,
                        type=Common.CheckChangeRankType.REGISTRATION,
                    )
                    Common.fooiy_standard_response(True)

            except Exception as e:
                obj.state = Common.PioneerState.ERROR
                obj.error_message = str(e)
                obj.save(update_fields=["state", "error_message"])

                Common.fooiy_standard_response(False, 5030, id=obj.id, error=e)

        if request.POST.get(Common.PioneerCheckType.REJECT):
            obj.state = Common.PioneerState.REJECT

            if not obj.reject_reason:
                raise forms.ValidationError(f"[요청 실패] 개척 반려 시 반드시 개척 반려 사유를 기입해주세요!")

            Common.slack_post_message(
                "#request_pioneer",
                f"*[🚫 {obj.shop_name}] {obj.menu_name}  개척 반려 🚫]*\n*반려사유* : {dict(PIONEER_REJECT_REASON)[obj.reject_reason]}",
            )

            ### 개척 반려 푸시 발송 로직 ####
            ArchivesHelpers.push_notifications(
                pioneer=obj,
                receiver=obj.account,
                type=Common.PushNotificationType.PIONEER_REJECT,
            )
            messages.info(request, "개척 반려 처리 되었습니다!")

        super().save_model(request, obj, form, change)
