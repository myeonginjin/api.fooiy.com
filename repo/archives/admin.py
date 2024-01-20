from django import forms
from django.contrib import admin
from .models import Image, AddressCluster
from shops.models import Shop


class ImageAdmin(admin.ModelAdmin):
    search_fields = ("id", "type", "shop__name", "feed__id", "account__nickname")
    list_display = ["id", "type", "image", "order", "created_at"]
    list_display_link = ["id"]
    ordering = ["-created_at"]
    raw_id_fields = [
        "account",
        "shop",
        "pioneer",
        "record",
        "menu",
        "taste_evaluation",
        "notice",
        "advertisement",
        "fooiyti",
    ]
    list_per_page = 15


class FooiytiImageInline(admin.TabularInline):
    model = Image
    extra = 0
    fields = ["type", "image"]

    def formfield_for_choice_field(self, db_field, request=None, **kwargs):
        if db_field.name == "type":
            kwargs["choices"] = (("FR", "푸이티아이 결과"),)
        return db_field.formfield(**kwargs)


class FooiytiAdmin(admin.ModelAdmin):
    list_display = [
        "fooiyti",
        "nickname",
        "description",
    ]
    list_display_link = ["fooiyti"]
    ordering = ["fooiyti"]
    inlines = (FooiytiImageInline,)
    list_per_page = 16


class FooiytiQuestionAdmin(admin.ModelAdmin):
    list_display = [
        "order",
        "question",
        "answer_1",
        "answer_2",
        "answer_3",
        "answer_4",
        "is_multi_answer",
    ]
    list_display_link = ["order"]
    ordering = ["order"]
    list_per_page = 15


class TasteEvaluationImageInline(admin.TabularInline):
    model = Image
    extra = 0
    fields = ["type", "image"]

    def formfield_for_choice_field(self, db_field, request=None, **kwargs):
        if db_field.name == "type":
            kwargs["choices"] = (("TE", "맛 평가"),)
        return db_field.formfield(**kwargs)


class TasteEvaluationAdmin(admin.ModelAdmin):
    list_display = ["score"]
    list_display_link = ["score"]
    ordering = ["id"]
    inlines = (TasteEvaluationImageInline,)
    list_per_page = 15

    def save_model(self, request, obj, form, change):
        if int(request.POST["image-TOTAL_FORMS"]) - int(
            request.POST["image-INITIAL_FORMS"]
        ) != len(request.FILES):
            raise forms.ValidationError("[등록 실패] 이미지 등록 시 이미지를 업로드 해주세요!")

        return super().save_model(request, obj, form, change)


class NoticeImageInline(admin.TabularInline):
    model = Image
    extra = 0
    fields = ["type", "image"]

    def formfield_for_choice_field(self, db_field, request=None, **kwargs):
        if db_field.name == "type":
            kwargs["choices"] = (("N", "공지사항"),)
        return db_field.formfield(**kwargs)


class NoticeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "order",
        "is_exposure",
        "date_event_start",
        "date_event_finish",
    ]
    list_display_link = ["id"]
    ordering = ["id"]
    list_per_page = 15
    inlines = (NoticeImageInline,)

    def save_model(self, request, obj, form, change):
        if int(request.POST["image-TOTAL_FORMS"]) - int(
            request.POST["image-INITIAL_FORMS"]
        ) != len(request.FILES):
            raise forms.ValidationError("[등록 실패] 이미지 등록 시 이미지를 업로드 해주세요!")

        return super().save_model(request, obj, form, change)


class VersionAdmin(admin.ModelAdmin):
    list_display = ["version", "os", "is_update_required", "date_updated"]
    list_display_link = ["version"]
    ordering = ["-id"]
    list_per_page = 15


class AdvertisementImageInline(admin.TabularInline):
    model = Image
    extra = 0
    fields = ["type", "image"]

    def formfield_for_choice_field(self, db_field, request=None, **kwargs):
        if db_field.name == "type":
            kwargs["choices"] = (("AD", "광고"),)
        return db_field.formfield(**kwargs)


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "advertiser",
        "type",
        "is_exposure",
        "created_at",
    ]
    list_display_link = ["title"]
    ordering = ["-created_at"]
    list_per_page = 15
    inlines = (AdvertisementImageInline,)

    def save_model(self, request, obj, form, change):
        if int(request.POST["image-TOTAL_FORMS"]) - int(
            request.POST["image-INITIAL_FORMS"]
        ) != len(request.FILES):
            raise forms.ValidationError("[등록 실패] 이미지 등록 시 이미지를 업로드 해주세요!")

        return super().save_model(request, obj, form, change)


class SuggestionAdmin(admin.ModelAdmin):
    list_display = ["id", "type", "account", "content", "created_at"]
    list_display_link = ["id"]
    ordering = ["-created_at"]
    raw_id_fields = ["account"]
    list_per_page = 15


class AddressClusterAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "parent_depth", "depth", "count"]
    list_display_link = ["id"]
    ordering = ["id"]
    list_per_page = 15
    actions = ["recalculate_shop_count"]

    def recalculate_shop_count(modeladmin, request, queryset):
        queryset = AddressCluster.objects.all()
        for address_cluster in list(queryset):
            if address_cluster.depth == 1:
                address_cluster.count = Shop.objects.filter(
                    address_depth1=address_cluster.name
                ).count()
            else:
                address_cluster.count = Shop.objects.filter(
                    address_depth1=address_cluster.parent_depth.name,
                    address_depth2=address_cluster.name,
                ).count()
            address_cluster.save()

    recalculate_shop_count.short_description = "(하나만 체크해도 동작)모든 주소의 매장수를 재계산합니다."


class PushNotificationAdmin(admin.ModelAdmin):
    list_display = ["receiver", "sender", "title", "created_at"]
    list_display_link = ["receiver"]
    ordering = ["-created_at"]
    raw_id_fields = ["receiver", "sender", "pioneer", "feed"]
    search_fields = ["receiver", "sender", "title", "content"]
    list_per_page = 15
