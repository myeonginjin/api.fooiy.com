from rest_framework.views import exception_handler
from django.http import JsonResponse

from .enums import LogLevel
from .slack import slack_post_message
from .error_code import warning, error
import logging


logger = logging.getLogger("api")


def get_request_ip(request):
    """
    # request ip 추출
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def unexpected_exception_handler(exc, context):
    """
    # DRF 커스텀 예외 핸들러
    """
    response = exception_handler(exc, context)

    if response is not None:
        del response.data["detail"]
        response.data["success"] = False
        response.data["error"] = {"code": 5000, "message": "unexpected error occurred"}

    return response


def fooiy_standard_response(success: bool, data="success", **kwargs):
    """
    # 푸이 표준 응답
    """
    if success:
        return {"success": True, "payload": data}
    elif data != 4404:
        if data >= 5000:
            message = f"{error[data]}"
            logger.error(message)
            channel = "#log_error"
            slack_message = f"[code:{data}] {error[data]}"
        else:
            message = f"{warning[data]}"
            logger.warning(message)
            channel = "#log_user_warning"

            slack_message = f"[code:{data}] {warning[data]}"

        for key, value in kwargs.items():
            slack_message += f", {key}: {value}"

        slack_post_message(channel, slack_message)
        return {"success": False, "error": {"code": data, "message": message}}


def fooiy_standard_response_v1(success: bool, data: object = {}, log_data: object = {}):
    """
    # 푸이 표준 응답
    """
    if success:
        if log_data:
            logger.info(log_data["message"])

        return {"success": True, "payload": data}
    else:
        if data.get("code", None) != 4404:
            if log_data["level"] == LogLevel.ERROR:
                logger.error(log_data["message"])
                slack_post_message("#log_error", log_data["message"])
            elif log_data["level"] == LogLevel.WARNING:
                logger.warning(log_data["message"])
                slack_post_message("#log_user_warning", log_data["message"])

        return {"success": False, "error": data}


def custom404(request, exception=None):
    """
    # 경로 404 에러 처리
    """
    return JsonResponse(
        fooiy_standard_response(
            False,
            4404,
            uri=f"{request.build_absolute_uri()}",
            ip=f"{get_request_ip(request)}",
        ),
        status=404,
    )


def custom500(request, exception=None):
    """
    # 예측 못한 서버 에러 처리
    """
    origin_uri = "http://api.fooiy.com/"
    origin_secure_uri = "https://api.fooiy.com/"
    admin_secure_uri = "http://admin.fooiy.com/admin-fooiy/"
    request_uri = request.build_absolute_uri()
    if not (
        request_uri.startswith(origin_uri)
        or request_uri.startswith(origin_secure_uri)
        or request_uri.startswith(admin_secure_uri)
    ):
        return {"success": False, "error": "wrong approach api"}
    return JsonResponse(
        fooiy_standard_response(
            False,
            5000,
            uri=f"{request.build_absolute_uri()}",
            ip=f"{get_request_ip(request)}",
        ),
        status=500,
    )
