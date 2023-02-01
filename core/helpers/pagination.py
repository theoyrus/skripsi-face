from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class AppRestNumPagination(PageNumberPagination):
    # https://stackoverflow.com/a/64949239
    # override page numbering DRF
    page_size = 10  # default limit per page
    page_query_param = "offset"  # this is the "page"
    page_size_query_param = "limit"  # this is the "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            {
                "meta": {
                    "total": self.page.paginator.count,
                    "per_page": self.page.paginator.per_page,
                    "current": self.page.number,
                    "next": self.get_next_link(),
                    "prev": self.get_previous_link(),
                },
                "data": data,
            }
        )
