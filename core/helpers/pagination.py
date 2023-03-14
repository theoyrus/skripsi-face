from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class AppRestNumPagination(PageNumberPagination):
    # https://stackoverflow.com/a/64949239
    # override page numbering DRF
    page_size = 10  # default limit per page
    page_query_param = "page"  # this is the "page"
    page_size_query_param = "limit"  # this is the "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        req = self.request
        limit = int(req.GET.get("limit", self.page_size))
        page = int(req.GET.get("page", 1))

        # hitung index awal & akhir dari queryset
        start = (page - 1) * limit
        end = page * limit

        # tambahkan prop num di setiap item di data
        for i, item in enumerate(data[0:limit], start=start):
            item["num"] = i + 1

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
