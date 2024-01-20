def get_notify_record_slack_attachments(record):
    return [
        {
            "title": "[🥳 기록 작성 📝]",
            "fields": [
                {
                    "title": "매장명",
                    "value": record.shop.name,
                    "short": True,
                },
                {
                    "title": "메뉴 이름",
                    "value": record.menu.name,
                    "short": True,
                },
                {
                    "title": "코멘트",
                    "value": record.description,
                    "short": True,
                },
                {
                    "title": "맛 평가",
                    "value": str(record.taste_evaluation) + "점",
                    "short": True,
                },
            ],
            "fallback": "기록이 작성되었습니다!",
            "color": "#FF5C5C",
            "attachment_type": "default",
        }
    ]
