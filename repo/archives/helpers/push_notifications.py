from firebase_admin import messaging
from common import index as Common
from archives.models import PushNotification
from feeds.models import PIONEER_REJECT_REASON


def push_notifications(
    receiver,
    title=None,
    body=None,
    account=None,
    dropped_ranker=None,
    rank_type=None,
    state=None,
    type=None,
    sender=None,
    pioneer=None,
    feed=None,
    content=None,
    party=None,
    image=None,
):
    try:
        if receiver.is_active:
            navigation = ""
            navigation_id = ""

            if type == Common.PushNotificationType.RANK:
                navigation = Common.PushNavigationType.MY_PAGE
                navigation_id = account.public_id

                if rank_type:
                    title = f"👑 {rank_type.upper()} 등급이 되었어요!"
                    body = f"{account.nickname}님, 축하드려요!\n푸이에서 바로 확인해보세요."
                    image = image

                elif dropped_ranker:
                    title = f"🔥 {dropped_ranker.nickname}님을 기다리고 있어요!"
                    body = f"{dropped_ranker.nickname}님보다 맛집을 더 많이 방문한 유저가 나타났어요.\n피드를 등록하고 다시 푸이 랭킹에 도전해보세요!"
                    image = image

                elif not rank_type and not dropped_ranker:
                    title = f"👑 푸이 랭커가 되었어요!"
                    body = f"{account.nickname}님, 축하드려요!\n푸이 랭킹에서 바로 확인해보세요."
                    image = image

            elif type == Common.PushNotificationType.PARTY:
                navigation = Common.PushNavigationType.PARTY
                navigation_id = party.id

                if state == Common.PartyState.CONFIRM:
                    title = f"📝 파티에 가입하고 싶어요."
                    body = (
                        f"{account.nickname}님이 {party.name} 가입 신청을 했어요!\n지금 바로 확인해보세요!"
                    )
                    image = party.party_image

                elif state == Common.PartyState.SUBSCRIBE:
                    title = f"🥳 파티원이 되었어요!"
                    body = (
                        f"{receiver}님, 축하드려요! {party.name}에 가입되었어요. 파티에 첫 게시물을 작성해보세요!"
                    )
                    image = party.party_image

                elif state == Common.PartyState.REJECT:
                    title = f"💧 다른 파티를 찾아볼까요?"
                    body = f"가입 신청한 {party.name}에 가입하지 못했어요.\n다른 파티에 가입하거나 파티를 직접 생성할 수 있어요."
                    image = party.party_image

                elif state == Common.PartyState.EXPULSION:
                    title = f"💧 다른 파티를 찾아볼까요?"
                    body = (
                        f"더 이상 {party.name}에 함께할 수 없어요.\n다른 파티에 가입하거나 파티를 직접 생성할 수 있어요."
                    )
                    image = party.party_image

            elif type in [
                Common.PushNotificationType.LIKE,
                Common.PushNotificationType.STORAGE,
            ]:
                navigation = Common.PushNavigationType.FEED
                navigation_id = feed.id

                if type == Common.PushNotificationType.LIKE:
                    title = f"💘 피드 사진이 맛있어 보여요!"
                    body = f"{account.nickname}님이 회원님의 피드에 포크를 찍었어요."
                    image = feed.image.get(order="0").image

                elif type == Common.PushNotificationType.STORAGE:
                    title = f"🗂 피드가 도움이 됐어요."
                    body = f"다른 유저가 회원님의 피드를 보관했어요."
                    image = feed.image.get(order="0").image

            elif type == Common.PushNotificationType.COMMENT:
                navigation = Common.PushNavigationType.COMMENT
                navigation_id = feed.id

                if state == Common.CommentState.PARENT_COMMENT:
                    title = f"💬 피드에 댓글이 달렸어요"
                    body = f"{account.nickname}님이 댓글을 남겼어요.\n'{content}'"
                    image = feed.image.get(order="0").image

                elif state == Common.CommentState.CHILD_COMMENT:
                    title = f"💬 댓글에 댓글이 달렸어요"
                    body = f"{account.nickname}님이 댓글을 남겼어요.\n'{content}'"
                    image = feed.image.get(order="0").image

            elif type == Common.PushNotificationType.PIONEER_SUCCESS:
                title = f"🎉 피드가 등록되었어요!"
                body = (
                    f"{pioneer.shop_name} {pioneer.menu_name} 피드가 등록되었어요! 피드에서 확인해보세요."
                )
                image = pioneer.image_1
                navigation = Common.PushNavigationType.FEED
                navigation_id = feed.id

            elif type == Common.PushNotificationType.PIONEER_REJECT:
                title = f"📌 피드 등록이 반려되었어요."
                body = f"{dict(PIONEER_REJECT_REASON)[pioneer.reject_reason]}"
                image = pioneer.image_1

            PushNotification.objects.create(
                receiver=receiver,
                party=party,
                sender=sender,
                pioneer=pioneer,
                feed=feed,
                title=title,
                content=body,
                type=type,
                image=image,
            )
            if not receiver.fcm_token == "0":
                message = messaging.Message(
                    notification=messaging.Notification(
                        title=title,
                        body=body,
                    ),
                    token=receiver.fcm_token,
                    data={
                        "navigation": navigation,
                        "navigation_id": str(navigation_id),
                    },
                )
                messaging.send(message)

    except Exception as e:
        Common.fooiy_standard_response(
            False, 5996, fcm_token=receiver.fcm_token, account=receiver, error=e
        ),


def push_navigation(type):
    try:
        if type in [
            Common.PushNotificationType.STORAGE,
            Common.PushNotificationType.LIKE,
            Common.PushNotificationType.PIONEER_SUCCESS,
        ]:
            return Common.PushNavigationType.FEED

        elif type == Common.PushNotificationType.COMMENT:
            return Common.PushNavigationType.COMMENT

        elif type == Common.PushNotificationType.RANK:
            return Common.PushNavigationType.MY_PAGE

        elif type == Common.PushNotificationType.PARTY:
            return Common.PushNavigationType.PARTY

        elif type == Common.PushNotificationType.OVERALL_NOTICE:
            return Common.PushNavigationType.OVERALL_NOTICE

        return ""
    except:
        return ""


def push_navigation_id(obj):
    try:
        if (
            obj.type == Common.PushNotificationType.STORAGE
            or obj.type == Common.PushNotificationType.COMMENT
            or obj.type == Common.PushNotificationType.LIKE
            or obj.type == Common.PushNotificationType.PIONEER_SUCCESS
        ):
            return obj.feed.id

        elif obj.type == Common.PushNotificationType.PARTY:
            return obj.party.id

        elif obj.type == Common.PushNotificationType.RANK:
            return obj.receiver.public_id

        return ""
    except:
        return ""
