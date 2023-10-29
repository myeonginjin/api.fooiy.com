def get_keyword_slack_attachments(keyword):
    return [
        {
            "title": "? 위치 검색에 실패했어요!",
            "fields": [
                {
                    "title": "검색어",
                    "value": keyword,
                },
            ],
            "fallback": "? 위치 검색에 실패했어요!",
            "color": "#FF5C5C",
            "attachment_type": "default",
        }
    ]
