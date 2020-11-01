from rest_framework import pagination

# 기존의 PageNumberPagination을 오버라이딩해서 직접 만든 pagination
class CustomPagination(pagination.PageNumberPagination):

    def get_html_context(self):
        base_url = self.request.build_absolute_uri()

        def page_number_to_url(page_number):
            if page_number == 1:
                return pagination.remove_query_param(base_url, self.page_query_param)
            else:
                return pagination.replace_query_param(base_url, self.page_query_param, page_number)

        current = self.page.number
        final = self.page.paginator.num_pages
        page_numbers = pagination._get_displayed_page_numbers(current, final)
        page_links = pagination._get_page_links(page_numbers, current, page_number_to_url)

        return {
            'current' : current,
            'final' : final,
            'page_numbers' : page_numbers,
            'page_links' : page_links,
            'previous_url': self.get_previous_link(),
            'next_url': self.get_next_link(),
            'page_links': page_links
        }