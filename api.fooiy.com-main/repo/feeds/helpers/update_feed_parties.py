from django.db.models import F

from feeds.models import FeedParty
from accounts.models import AccountParty, Party
from common import index as Common
from re import split


def update_feed_parties(feed, subscribe_parties):
    if not subscribe_parties:
        subscribe_parties = []
    if type(subscribe_parties) == type("string"):
        subscribe_parties = split(r",", subscribe_parties)

    subscribe_parties = Party.objects.filter(id__in=subscribe_parties)
    unsubscribe_feed_parties = FeedParty.objects.filter(feed=feed).exclude(
        party_id__in=subscribe_parties
    )
    for unsubscribe_feed_party in unsubscribe_feed_parties:
        if unsubscribe_feed_party.state != Common.PartyState.UNSUBSCRIBE:
            unsubscribe_feed_party.state = Common.PartyState.UNSUBSCRIBE
            unsubscribe_feed_party.party.feed_count -= 1
            unsubscribe_feed_party.party.save(update_fields=["feed_count"])
    if unsubscribe_feed_parties:
        FeedParty.objects.bulk_update(unsubscribe_feed_parties, ["state"])

    for subscribe_party in subscribe_parties:
        feed_party = FeedParty.objects.filter(feed=feed, party=subscribe_party)
        if feed_party:
            feed_party = feed_party.first()
            if feed_party.state != Common.PartyState.SUBSCRIBE:
                feed_party.state = Common.PartyState.SUBSCRIBE
                feed_party.save(update_fields=["state"])
                feed_party.party.feed_count += 1
        else:
            feed_party = FeedParty.objects.create(feed=feed, party=subscribe_party)
            feed_party.party.feed_count += 1
        feed_party.party.save(update_fields=["feed_count"])
