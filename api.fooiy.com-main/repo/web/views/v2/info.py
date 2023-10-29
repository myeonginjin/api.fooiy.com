from django.shortcuts import render
from feeds.models import Feed
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from archives.models import Suggestion


def main(request):
    return render(
        request,
        "web/info.html",
    )


def feed_rank_list(request):
    # date = timedelta(days=7)
    feeds = (
        Feed.objects.annotate(count=Count("like"))
        # .filter(created_at__gte=timezone.now() - date)
        .order_by("-count")
    )[:100]

    images = [feed.image.first().image.url for feed in feeds]

    context = {"feeds": feeds, "images": images}

    return render(
        request,
        "web/feed_rank_list.html",
        context,
    )


def push_notifications(request):
    suggestions = (Suggestion.objects.all())[:10]
    context = {"suggestions": suggestions}

    return render(
        request,
        "web/push_notifications.html",
        context,
    )


def overall_push_notifications(request):
    return render(
        request,
        "web/overall_push_notifications.html",
    )
