from django.contrib import admin
from archives.helpers import index as ArchivesHelpers


class AccountAdmin(admin.ModelAdmin):
    search_fields = ("nickname", "username")
    list_display = [
        "id",
        "nickname",
        "state",
        "gender",
        "birth_year",
        "fooiyti",
        "pioneer_count",
        "social_type",
        "os",
        "app_version",
        "date_joined",
    ]
    list_display_links = ["id"]
    list_per_page = 15
    ordering = ["-id"]
    actions = ["recalculate_account_rank"]

    def save_model(self, request, obj, form, change):
        if request.POST.get("push-notification"):
            title = request.POST.get("title")
            content = request.POST.get("content")
            ArchivesHelpers.send_push_notifications(
                title=title, body=content, receiver=obj
            )
        else:
            return super().save_model(request, obj, form, change)


class StorageAdmin(admin.ModelAdmin):
    search_fields = ("account__nickname", "feed__shop__name")
    list_display = [
        "id",
        "account",
        "feed",
    ]
    list_display_links = ["id"]
    raw_id_fields = ["account", "feed"]
    list_per_page = 15
    ordering = ["-id"]


class LikeAdmin(admin.ModelAdmin):
    search_fields = ("account__nickname", "feed__shop__name")
    list_display = [
        "id",
        "account",
        "feed",
    ]
    list_display_links = ["id"]
    raw_id_fields = ["account", "feed"]
    list_per_page = 15
    ordering = ["-id"]


class PartyAdmin(admin.ModelAdmin):
    search_fields = ("name", "owner__nickname")
    list_display = [
        "name",
        "owner",
        "account_count",
        "feed_count",
        "created_at",
    ]
    list_display_links = ["name"]
    ordering = ["-created_at"]
