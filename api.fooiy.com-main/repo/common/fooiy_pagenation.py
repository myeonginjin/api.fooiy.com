from rest_framework.pagination import LimitOffsetPagination


class FooiyPagenation(LimitOffsetPagination):
    def get_paginated_response(self, data):
        return {
            "total_count": self.count,
            "links": {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
            },
            "results": data,
        }

    def paginate_queryset(self, queryset, request, view=None):
        confirm_pioneer_count = getattr(request, "confirm_pioneer_count", 0)
        self.count = self.get_count(queryset)
        self.limit = self.get_limit(request)
        self.offset = self.get_offset(request)
        self.request = request

        if confirm_pioneer_count:
            if self.offset - confirm_pioneer_count <= 0:
                self.offset = 0
                self.limit = (
                    self.limit - confirm_pioneer_count
                    if self.limit - confirm_pioneer_count > 0
                    else 0
                )
            else:
                self.offset = (
                    self.offset - confirm_pioneer_count
                    if self.offset - confirm_pioneer_count > 0
                    else 0
                )

        if self.limit is None:
            return None

        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        if self.count == 0 or self.offset > self.count:
            return []
        return list(queryset[self.offset : self.offset + self.limit])
