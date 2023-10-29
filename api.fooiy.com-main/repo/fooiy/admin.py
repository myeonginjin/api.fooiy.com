from django.contrib.admin.sites import AdminSite
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin

from accounts.models import Account, Storage, Like, Party
from accounts.admin import AccountAdmin, StorageAdmin, LikeAdmin, PartyAdmin
from shops.models import Shop, ShopCategory, ShopBadge, ShopScore, Menu, ShopFooiyti
from shops.admin import (
    ShopAdmin,
    ShopCategoryAdmin,
    ShopBadgeAdmin,
    ShopScoreAdmin,
    MenuAdmin,
    ShopFooiytiAdmin,
)
from archives.models import (
    Image,
    Fooiyti,
    FooiytiQuestion,
    TasteEvaluation,
    Notice,
    Version,
    Advertisement,
    Suggestion,
    AddressCluster,
    PushNotification,
)
from archives.admin import (
    ImageAdmin,
    FooiytiAdmin,
    FooiytiQuestionAdmin,
    TasteEvaluationAdmin,
    NoticeAdmin,
    VersionAdmin,
    AdvertisementAdmin,
    SuggestionAdmin,
    AddressClusterAdmin,
    PushNotificationAdmin,
)
from feeds.models import Record, Pioneer, Feed, FeedComment
from feeds.admin import RecordAdmin, PioneerAdmin, FeedAdmin, FeedCommentAdmin
from search.models import SearchSpot
from search.admin import SearchSpotAdmin

admin_site = AdminSite()

admin_site.site_title = "fooiy CS ADMIN"
admin_site.site_header = "fooiy CS ADMIN"

admin_site.enable_nav_sidebar = False

# ======= auth ======= #
admin_site.register(Site)
admin_site.register(Group, GroupAdmin)

# ======= accounts ======= #
admin_site.register(Account, AccountAdmin)
admin_site.register(Storage, StorageAdmin)
admin_site.register(Like, LikeAdmin)
admin_site.register(Party, PartyAdmin)

# ======= shops ======= #
admin_site.register(Shop, ShopAdmin)
admin_site.register(ShopCategory, ShopCategoryAdmin)
admin_site.register(ShopBadge, ShopBadgeAdmin)
admin_site.register(ShopScore, ShopScoreAdmin)
admin_site.register(ShopFooiyti, ShopFooiytiAdmin)
admin_site.register(Menu, MenuAdmin)

# ======= archives ======= #
admin_site.register(Image, ImageAdmin)
admin_site.register(Fooiyti, FooiytiAdmin)
admin_site.register(FooiytiQuestion, FooiytiQuestionAdmin)
admin_site.register(TasteEvaluation, TasteEvaluationAdmin)
admin_site.register(Notice, NoticeAdmin)
admin_site.register(Version, VersionAdmin)
admin_site.register(Advertisement, AdvertisementAdmin)
admin_site.register(Suggestion, SuggestionAdmin)
admin_site.register(AddressCluster, AddressClusterAdmin)
admin_site.register(PushNotification, PushNotificationAdmin)

# ======= feeds ======= #
admin_site.register(Record, RecordAdmin)
admin_site.register(Pioneer, PioneerAdmin)
admin_site.register(Feed, FeedAdmin)
admin_site.register(FeedComment, FeedCommentAdmin)

# ======= search ======= #
admin_site.register(SearchSpot, SearchSpotAdmin)
