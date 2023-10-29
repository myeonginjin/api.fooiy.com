from fooiy.settings import SLACK_TOKEN, DEBUG
import requests, json

import logging

logger = logging.getLogger("api")


def slack_post_message(channel, text, attachments=None):
    data = {"channel": "#dev" if DEBUG else channel, "text": text}

    if attachments:
        data["attachments"] = json.dumps(attachments)

    try:
        requests.post(
            "https://slack.com/api/chat.postMessage",
            headers={"Authorization": "Bearer " + SLACK_TOKEN},
            data=data,
        )
    except Exception as e:
        logger.error(
            f"slack post message error occur, (channel : {channel}, text : {text}, error : {e})"
        )
