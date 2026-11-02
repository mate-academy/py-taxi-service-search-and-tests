from urllib.parse import parse_qs

from django.test import RequestFactory, SimpleTestCase

from taxi.templatetags.query_transform import query_transform


class QueryTransformTests(SimpleTestCase):
    def test_replace_page_preserves_query_and_request(self):
        request = RequestFactory().get(
            "/cars/", {"model": "A & B", "page": "1"}
        )
        original = request.GET.copy()
        result = query_transform(request, page=2)
        self.assertEqual(
            parse_qs(result), {"model": ["A & B"], "page": ["2"]}
        )
        self.assertEqual(request.GET, original)

    def test_remove_parameter(self):
        request = RequestFactory().get(
            "/cars/", {"model": "Audi", "page": "2"}
        )
        result = query_transform(request, page=None, missing=None)
        self.assertEqual(parse_qs(result), {"model": ["Audi"]})
