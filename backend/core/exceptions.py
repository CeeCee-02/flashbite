"""
Custom DRF exception handler.
Converts all API errors into a consistent JSON envelope:
  {
    "success": false,
    "error": "Short error type",
    "message": "Human-readable message",
    "details": { ... }   # optional field-level errors
  }
"""

import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger("flashbite")


def custom_exception_handler(exc, context):
    """
    Wrap DRF's default exception handler output in the FLASHBITE error envelope.
    Non-DRF exceptions are converted to a generic 500 response and logged.
    """
    # Call REST framework's default handler first to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        # DRF handled it — reformat the body
        data = response.data
        error_detail = _extract_message(data)
        details = data if isinstance(data, dict) and "detail" not in data else None

        response.data = {
            "success": False,
            "error": _status_to_error_type(response.status_code),
            "message": error_detail,
        }
        if details:
            response.data["details"] = details
    else:
        # Unhandled exception — log it and return 500
        logger.exception("Unhandled exception in view %s", context.get("view"))
        response = Response(
            {
                "success": False,
                "error": "InternalServerError",
                "message": "An unexpected error occurred. Our team has been notified.",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response


def _extract_message(data):
    if isinstance(data, dict):
        detail = data.get("detail", "")
        if detail:
            return str(detail)
        # Field-level errors: return first field's first error
        for _field, errors in data.items():
            if isinstance(errors, list) and errors:
                return str(errors[0])
        return "Validation error."
    if isinstance(data, list) and data:
        return str(data[0])
    return str(data)


def _status_to_error_type(status_code: int) -> str:
    mapping = {
        400: "BadRequest",
        401: "Unauthorized",
        403: "Forbidden",
        404: "NotFound",
        405: "MethodNotAllowed",
        409: "Conflict",
        429: "TooManyRequests",
        500: "InternalServerError",
    }
    return mapping.get(status_code, f"HttpError{status_code}")


def success_response(data=None, message="", status_code=status.HTTP_200_OK):
    """
    Helper to build a standard success envelope.
    Usage in views:
        return success_response(serializer.data, status_code=201)
    """
    body = {"success": True}
    if message:
        body["message"] = message
    if data is not None:
        body["data"] = data
    return Response(body, status=status_code)
