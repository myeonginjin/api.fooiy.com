from accounts.helpers import index as AccountHelpers
from common import index as Common
from accounts.models import AccountParty, Party
from feeds.models import FeedParty
from archives.helpers import index as ArchivesHelpers


def update_account_parties(party, confirm_accounts, confirm):
    party_state = AccountParty.objects.filter(
        party=party, account__public_id__in=confirm_accounts
    )

    party_state.update(state=confirm)

    if confirm == Common.PartyState.EXPULSION:
        FeedParty.objects.filter(
            party=party, feed__account__public_id__in=confirm_accounts
        ).update(state=Common.PartyState.UNSUBSCRIBE)

    party.save()

    if party_state:
        for party_accounts in party_state:

            ArchivesHelpers.push_notifications(
                receiver=party_accounts.account,
                party=party,
                state=confirm,
                type=Common.PushNotificationType.PARTY,
            )
