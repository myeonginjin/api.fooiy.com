from common import index as Common
from archives.models import SUGGESTION_TYPE
from fooiy.settings import DEBUG


class SlackAttachments:
    def tip_off_slack_attachments(account, shop, content):
        return [
            {
                "title": "[💬 *문의 접수* 🔔]",
                "fields": [
                    {
                        "title": "문의유형",
                        "value": dict(SUGGESTION_TYPE)[Common.SuggestionType.TIP_OFF],
                        "short": True,
                    },
                    {
                        "title": "문의자",
                        "value": f"<{'http://dev-api.fooiy.com' if DEBUG else 'https://admin.fooiy.com'}/admin-fooiy/accounts/account/{account.id}/change/|{account}>",
                        "short": True,
                    },
                    {
                        "title": "매장",
                        "value": f"<{'http://dev-api.fooiy.com' if DEBUG else 'https://admin.fooiy.com'}/admin-fooiy/shops/shop/{shop.id}/change/|{shop}>",
                        "short": True,
                    },
                    {
                        "title": "내용",
                        "value": content,
                        "short": True,
                    },
                ],
            },
        ]

    def suggestion_slack_attachments(account, _type, content):
        return [
            {
                "title": "[💬 *문의 접수* 🔔]",
                "fields": [
                    {
                        "title": "문의유형",
                        "value": dict(SUGGESTION_TYPE)[_type],
                        "short": True,
                    },
                    {
                        "title": "문의자",
                        "value": f"<{'http://dev-api.fooiy.com' if DEBUG else 'https://admin.fooiy.com'}/admin-fooiy/accounts/account/{account.id}/change/|{account}>",
                        "short": True,
                    },
                    {
                        "title": "내용",
                        "value": content,
                        "short": True,
                    },
                ],
            },
        ]
