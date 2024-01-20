from django.contrib import admin
from django.urls import path
from web.views.v2 import info
from django.conf.urls import include

urlpatterns = [
    path("", info.main, name="main"),
    path("feed/", info.feed_rank_list, name="feed_rank_list"),
    path("push/", info.push_notifications, name="push_notifications"),
    path(
        "overall_push/",
        info.overall_push_notifications,
        name="overall_push_notifications",
    ),
]

# urlpatterns = [
#     path("feed/", info.feed_rank_list, name="feed_rank_list"),
# ]

# urlpatterns = [
#     path("push/", info.push_notifications, name="push_notifications"),
# ]
