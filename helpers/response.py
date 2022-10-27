from typing import Dict
from rest_framework.response import Response as DRFResponse
from rest_framework.pagination import PageNumberPagination


class InvalidResponse(Exception):
    pass


class Response:
    def __new__(cls, data=None, errors=None, *args, **kwargs):
        payload = cls.format(data, errors)
        return DRFResponse(payload, *args, **kwargs)

    @classmethod
    def format(cls, data, errors):
        data, errors = cls.validate(data, errors)

        message = "success" if data and not errors else "failure"

        if not data and not errors:
            raise InvalidResponse("Both data and errors cannot be None")

        return dict(
            message=message,
            data=data,
            errors=errors,
        )

    @classmethod
    def validate(cls, data, errors):
        try:
            data = None if data is None else dict(data)
            errors = None if errors is None else dict(errors)
            return (data, errors)
        except Exception:
            raise InvalidResponse(
                "None or dict-like structure expected for both data and errors"
            )


class ResponseManager:
    @staticmethod
    def handle_response(
        data: Dict = {}, errors: Dict = {}, status: int = 200, message: str = ""
    ) -> Response:
        if errors:
            return Response({"errors": errors, "message": message}, status=status)
        return Response({"data": data, "message": message}, status=status)

    @staticmethod
    def handle_paginated_response(
        paginator_instance: PageNumberPagination = PageNumberPagination(),
        data: Dict = {},
    ) -> Response:
        return paginator_instance.get_paginated_response(data)


class CustomPaginatedResponse(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return DRFResponse(
            {
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "data": data,
            }
        )


def paginate_response(
    queryset, serializer_, request, page_size=10, paginator=CustomPaginatedResponse
):
    paginator_instance = paginator()
    paginator_instance.page_size = page_size
    return ResponseManager.handle_paginated_response(
        paginator_instance,
        serializer_(
            paginator_instance.paginate_queryset(queryset, request), many=True
        ).data,
    )
