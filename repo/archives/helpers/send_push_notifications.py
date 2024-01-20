from firebase_admin import messaging

from common import index as Common
from ..models import PushNotification


# 지울예정!!!!!!!!!!!!!


def send_push_notifications(
    title, body, receiver, type=None, sender=None, pioneer=None, feed=None
):
    try:
        if receiver.is_active:
            PushNotification.objects.create(
                receiver=receiver,
                sender=sender,
                pioneer=pioneer,
                feed=feed,
                title=title,
                content=body,
                type=type,
            )
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                token=receiver.fcm_token,
            )
            messaging.send(message)

    except Exception as e:
        Common.fooiy_standard_response(
            False, 5996, fcm_token=receiver.fcm_token, account=receiver, error=e
        ),
