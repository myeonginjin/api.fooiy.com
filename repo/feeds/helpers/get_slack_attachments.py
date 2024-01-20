from fooiy.settings import DEBUG


def get_request_pioneer_slack_attachments(pioneer):
    return [
        {
            "title": "[🥳 개척 검수 요청 🚩]",
            "fields": [
                {
                    "title": "매장명",
                    "value": pioneer.shop_name,
                    "short": True,
                },
                {
                    "title": "주소",
                    "value": pioneer.address,
                    "short": True,
                },
                {
                    "title": "메뉴 이름",
                    "value": pioneer.menu_name,
                    "short": True,
                },
                {
                    "title": "맛 평가",
                    "value": pioneer.taste_evaluation + "점",
                    "short": True,
                },
                {
                    "title": "개척자",
                    "value": pioneer.account.nickname,
                },
                {
                    "title": "개척자 코멘트",
                    "value": pioneer.comment,
                },
            ],
            "fallback": "개척 검수 요청이 들어왔습니다!",
            "color": "#FF5C5C",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "pioneer",
                    "text": "매장 찾기",
                    "type": "button",
                    "url": f"https://map.naver.com/v5/search/",
                },
                {
                    "name": "pioneer",
                    "text": "검수하기",
                    "type": "button",
                    "url": f"http://dev-api.fooiy.com/admin-fooiy/feeds/pioneer/{pioneer.id}/change/"
                    if DEBUG
                    else f"https://fooiy.com/pioneer-check/{pioneer.id}",
                },
            ],
        }
    ]


def get_request_menu_slack_attachments(feed):
    return [
        {
            "title": f"🥳 [{feed.shop.name}] 메뉴 등록 요청 🚩",
            "fallback": "개척이 완료되었어요! 나머지 메뉴를 등록해 볼까요 ?",
            "color": "#FF5C5C",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "pioneer",
                    "text": "매장 찾기",
                    "type": "button",
                    "url": f"https://map.naver.com/v5/search/{feed.shop.name}",
                },
                {
                    "name": "pioneer",
                    "text": "메뉴 등록하기",
                    "type": "button",
                    "url": f"http://dev-api.fooiy.com/admin-fooiy/shops/shop/{feed.shop_id}/change/"
                    if DEBUG
                    else f"https://admin.fooiy.com/admin-fooiy/shops/shop/{feed.shop_id}/change/",
                },
            ],
        }
    ]


def get_notification_shop_slack_attachments(shop):
    return [
        {
            "title": f"[매장이 이상해요 😭]",
            "fallback": "🚨 매장 이상 알림 🚨",
            "color": "#FF5C5C",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "shop",
                    "text": "매장 보기",
                    "type": "button",
                    "url": f"http://dev-api.fooiy.com/admin-fooiy/shops/shop/{shop.id}/change/"
                    if DEBUG
                    else f"https://admin.fooiy.com/admin-fooiy/shops/shop/{shop.id}/change/",
                },
            ],
        }
    ]


def get_notification_report_comment_attachments(account, comment):
    return [
        {
            "title": f"[댓글 신고 😭]",
            "fields": [
                {
                    "title": "댓글 작성자",
                    "value": comment.writer.nickname,
                    "short": True,
                },
                {
                    "title": "댓글 신고자",
                    "value": account.nickname,
                    "short": True,
                },
                {
                    "title": "댓글 내용",
                    "value": comment.content,
                },
            ],
            "fallback": "이상한 댓글이 들어왔어요 !",
            "color": "#FF5C5C",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "comment",
                    "text": "댓글 보기",
                    "type": "button",
                    "url": f"http://dev-api.fooiy.com/admin-fooiy/feeds/feedcomment/{comment.id}/change/"
                    if DEBUG
                    else f"https://admin.fooiy.com/admin-fooiy/feeds/feedcomment/{comment.id}/change/",
                },
            ],
        }
    ]


def get_notification_report_feed_attachments(account, feed):
    return [
        {
            "title": f"[피드 신고 😭]",
            "fields": [
                {
                    "title": "피드 작성자",
                    "value": feed.account.nickname,
                    "short": True,
                },
                {
                    "title": "피드 신고자",
                    "value": account.nickname,
                    "short": True,
                },
                {
                    "title": "피드 내용",
                    "value": feed.description,
                },
            ],
            "fallback": "이상한 피드가 들어왔어요 !",
            "color": "#FF5C5C",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "feed",
                    "text": "피드 보기",
                    "type": "button",
                    "url": f"http://dev-api.fooiy.com/admin-fooiy/feeds/feed/{feed.id}/change/"
                    if DEBUG
                    else f"https://admin.fooiy.com/admin-fooiy/feeds/feed/{feed.id}/change/",
                },
            ],
        }
    ]
