from django.utils import timezone
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.viewsets import (
    mixins,
    GenericViewSet,
)

from rest_framework.response import Response

from common import index as Common
from accounts.helpers import index as AccountsHelpers
from accounts.serializers.v2 import index as AccountsSerializerV2
from ...models import Version, Notice

import logging

logger = logging.getLogger("api")


class InitViewSet(mixins.ListModelMixin, GenericViewSet):
    @method_decorator(AccountsHelpers.fooiy_account_guard())
    def list(self, request):
        """
        # init API
        """
        version = request.query_params.get("version", None)
        os = request.query_params.get("os", None)
        payload = {}

        if version and os:
            try:
                try:
                    current_version = Version.objects.get(version=version, os=os)
                except:
                    current_version = (
                        Version.objects.filter(os=os).order_by("version").last()
                    )

                latest_version = Version.objects.filter(
                    version__gt=current_version.version, os=os
                ).last()

                emergency_notice = Notice.objects.filter(
                    is_exposure=True,
                    is_emergency=True,
                ).last()

                if emergency_notice:
                    payload = {
                        "emergency_notice": {
                            "id": emergency_notice.id,
                            "title": emergency_notice.title,
                            "content": emergency_notice.content,
                        }
                    }
                elif latest_version:
                    payload = {
                        "update_info": {
                            "is_force_update": current_version.is_update_required,
                            "update_title": f"{Common.global_variables.version_force_update_message if current_version.is_update_required else Common.global_variables.version_normal_update_message}",
                            "change_history": latest_version.change_history,
                        }
                    }
                try:
                    if request.account:
                        account = request.account

                        account.is_active = True
                        account.last_login = timezone.now()
                        account.app_version = version

                        account.save(
                            update_fields=[
                                "is_active",
                                "last_login",
                                "app_version",
                            ]
                        )

                        payload.update(
                            {
                                "account_info": AccountsSerializerV2.AccountDetailSerializer(
                                    account
                                ).data
                            }
                        )
                except:
                    pass
                payload.update(
                    {
                        "default_region": {
                            "default_longitude": Common.global_variables.default_longitude,
                            "default_latitude": Common.global_variables.default_latitude,
                            "default_address_depth1": Common.global_variables.default_address_depth1,
                            "default_address_depth2": Common.global_variables.default_address_depth2,
                        }
                    }
                )

                return Response(Common.fooiy_standard_response(True, payload))

            except Exception as e:
                return Response(
                    Common.fooiy_standard_response(False, 5033, error=e),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        else:
            Response(
                Common.fooiy_standard_response(
                    False, 4038, version=version, os=os, error=e
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
