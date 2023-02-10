from rest_framework.views import exception_handler
from http import HTTPStatus
from rest_framework.views import Response

# Using the description's of the HTTPStatus class as error message.
http_code_to_message = {v.value: v.description for v in HTTPStatus}
http_code_to_phrase = {v.value: v.phrase for v in HTTPStatus}


def api_exception_handler(exc: Exception, context) -> Response:
    """Custom API exception handler."""

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:

        error_payload = {
            "type": "",
            "error": {
                "status_code": 0,
                "status": "",
                "message": "",
                "data": [],
            },
        }
        error = error_payload["error"]
        status_code = response.status_code
        error_payload["type"] = "client_error" if status_code < 500 else "server_error"

        error["status"] = http_code_to_phrase[status_code]
        error["status_code"] = status_code
        error["message"] = http_code_to_message[status_code]
        error["data"] = response.data
        response.data = error_payload
    return response


from drf_standardized_errors.formatter import ExceptionFormatter
from drf_standardized_errors.types import ErrorResponse


class ApiExceptionFormatter(ExceptionFormatter):
    def format_error_response(self, error_response: ErrorResponse):
        error = error_response.errors[0]
        return {
            "type": error_response.type,
            "error": {
                "code": error.code,
                "message": error.detail,
                "field_name": error.attr,
            },
        }


from django.http import JsonResponse


def error404(request, exception):
    message = str(exception)
    response_data = {
        "type": "client_error",
        "error": {
            "status_code": 404,
            "status": http_code_to_phrase[404],
            "message": message if len(message) < 100 else http_code_to_message[404],
            "data": message if len(message) < 100 else http_code_to_message[404],
        },
    }
    return JsonResponse(response_data, status=404)


def error500(request, *args, **kwargs):
    response_data = {
        "type": "server_error",
        "error": {
            "status_code": 500,
            "status": http_code_to_phrase[500],
            "message": http_code_to_message[500],
            "data": http_code_to_message[500],
        },
    }
    return JsonResponse(response_data, status=500)


from rest_framework.exceptions import APIException


class KaryawanUserError(APIException):
    status_code = 400
    default_code = "bad_request"
    pass
