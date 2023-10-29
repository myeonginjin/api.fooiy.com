from django.contrib import admin

class SearchSpotAdmin(admin.ModelAdmin):
    search_fields = ("type", "name", "address")
    list_display = [
        "id",
        "type",
        "name",
        "address",
    ]
    list_display_link = ["id"]
    ordering = ["-id"]
    list_per_page = 15

