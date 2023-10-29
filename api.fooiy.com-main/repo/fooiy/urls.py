from django.urls import path, include
from django.conf.urls import include
from django.http import JsonResponse

from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from fooiy.settings import PHASE
from fooiy.admin import admin_site
from common.fooiy_response import custom404, custom500

from archives.views.v1 import index as ArchivesViewsV1
from accounts.views.v2 import index as AccountsViewsV2
from archives.views.v2 import index as ArchivesViewsV2
from feeds.views.v2 import index as FeedsViewsV2
from shops.views.v2 import index as ShopsViewsV2
from web.views.v2 import index as WebViewsV2
from search.views.v2 import index as SearchViewsV2


def health_check(request):
    return JsonResponse({"status": "available"})


schema_view = get_schema_view(
    openapi.Info(
        title="fooiy API Docs",
        default_version="v1",
        description="fooiy RESTful API 문서",
        terms_of_service="https://fooiy.com/policy/service.html/",
        contact=openapi.Contact(name="fooiy", email="fooiyofficial@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

handler404 = custom404
handler500 = custom500

# RESTful router
router_v1 = routers.SimpleRouter()
router_v1.register(
    r"archives/init",
    ArchivesViewsV1.InitViewSet,
    basename="archives/init",
)

router_v2 = routers.SimpleRouter()

router_v2.register(
    r"accounts",
    AccountsViewsV2.AccountsViewSet,
    basename="accounts",
)
router_v2.register(
    r"party/accounts",
    AccountsViewsV2.PartyViewSet,
    basename="party/accounts",
)
router_v2.register(
    r"archives/init", ArchivesViewsV2.InitViewSet, basename="archives/init"
)
router_v2.register(
    r"archives/notice", ArchivesViewsV2.NoticeViewSet, basename="archives/notice"
)
router_v2.register(
    r"archives/image", ArchivesViewsV2.ImageViewSet, basename="archives/image"
)
router_v2.register(
    r"archives/fooiyti", ArchivesViewsV2.FooiytiViewSet, basename="archives/fooiyti"
)
router_v2.register(
    r"archives/filter", ArchivesViewsV2.FilterViewSet, basename="archives/filter"
)
router_v2.register(
    r"archives/suggestion",
    ArchivesViewsV2.SuggestionViewSet,
    basename="archives/suggestion",
)

router_v2.register(
    r"feeds/pioneer", FeedsViewsV2.PioneerViewSet, basename="feeds/pioneer"
)
router_v2.register(r"feeds/record", FeedsViewsV2.RecordViewSet, basename="feeds/record")
router_v2.register(r"feeds/feed", FeedsViewsV2.FeedViewSet, basename="feeds/feed")
router_v2.register(
    r"feeds/feed/comment",
    FeedsViewsV2.FeedCommentViewSet,
    basename="feeds/feed/comment",
)
router_v2.register(
    r"feeds/feed/storage",
    FeedsViewsV2.FeedViewSet.StorageViewSet,
    basename="feeds/feed/storage",
)
router_v2.register(
    r"feeds/feed/like",
    FeedsViewsV2.FeedViewSet.LikeViewSet,
    basename="feeds/feed/like",
)
router_v2.register(r"shops/shop", ShopsViewsV2.ShopViewSet, basename="shops/shop")
router_v2.register(r"shops/menu", ShopsViewsV2.MenuViewSet, basename="shops/menu")
router_v2.register(
    r"shops/menu_clinic", ShopsViewsV2.MenuClinicViewSet, basename="shops/menu_clinic"
)
router_v2.register(r"web/pioneer", WebViewsV2.PioneerViewSet, basename="web/pioneer")
router_v2.register(
    r"search/account", SearchViewsV2.AccountsSearchViewSet, basename="search/account"
)
router_v2.register(
    r"search/shops", SearchViewsV2.ShopsSearchViewSet, basename="search/shops"
)
router_v2.register(
    r"search/spot", SearchViewsV2.SpotSearchViewSet, basename="search/spot"
)
router_v2.register(
    r"search/party", SearchViewsV2.PartiesSearchViewSet, basename="search/party"
)

router_v2.register(
    r"archives/push_notification",
    ArchivesViewsV2.PushNotificationViewSet,
    basename="archives/push_notification",
)
urlpatterns = [
    # health check
    path("health_check/", health_check, name="health_check"),
]

if PHASE in ["PROD", "DEV"]:
    urlpatterns += [
        # Social Login API
        path(
            "api/v2/accounts/kakao_login/",
            AccountsViewsV2.kakao_login,
            name="kakao_login",
        ),
        path(
            "api/v2/accounts/apple_login/",
            AccountsViewsV2.apple_login,
            name="apple_login",
        ),
        # 랭킹 계산 API
        path(
            "api/v2/accounts/calculate_account_ranker/",
            AccountsViewsV2.calculate_account_ranker,
            name="calculate_account_ranker",
        ),
        # Slack Command API
        path(
            "api/v2/archives/pioneer_status/",
            ArchivesViewsV2.pioneer_status,
            name="pioneer_status",
        ),
        path(
            "api/v2/archives/kpi/",
            ArchivesViewsV2.kpi,
            name="kpi",
        ),
        path(
            "api/v2/archives/fooiyti_ratio/",
            ArchivesViewsV2.fooiyti_ratio,
            name="fooiyti_ratio",
        ),
        # RESTful API
        path("api/v1/", include(router_v1.urls)),
        path("api/v2/", include(router_v2.urls)),
    ]

if PHASE in ["ADMIN", "DEV"]:
    urlpatterns += [
        # admin
        path("admin-fooiy/", admin_site.urls),
        # docs
        path(
            "info/",
            include("web.urls"),
            name="info",
        ),
        path(
            "swagger-fooiy<str:format>",
            schema_view.without_ui(cache_timeout=0),
            name="swaager-fooiy-json",
        ),
        path(
            "swagger-fooiy/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="swagger-fooiy",
        ),
        path(
            "redoc-fooiy/",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="redoc-fooiy",
        ),
    ]
