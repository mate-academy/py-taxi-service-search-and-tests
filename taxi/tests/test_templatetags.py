from django.test import TestCase, RequestFactory
from urllib.parse import parse_qs
from taxi.templatetags.query_transform import query_transform


class TemplateTagsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_query_transform_add_parameter(self):
        request = self.factory.get("/test-path?name=test")
        result = query_transform(request, page=2)
        self.assertEqual(
            parse_qs(result),
            {"name": ["test"], "page": ["2"]}
        )

    def test_query_transform_update_parameter(self):
        request = self.factory.get(
            "/test-path?page=1&search=car"
        )
        result = query_transform(request, page=3)
        self.assertEqual(
            parse_qs(result),
            {"search": ["car"], "page": ["3"]}
        )

    def test_query_transform_remove_parameter(self):
        request = self.factory.get(
            "/test-path?page=2&search=car"
        )
        result = query_transform(request, page=None)
        self.assertEqual(
            parse_qs(result), {"search": ["car"]}
        )

    def test_query_transform_multiple_changes(self):
        request = self.factory.get(
            "/test-path?page=1&order=asc"
        )
        result = query_transform(
            request, page=2, order=None, new="val"
        )
        self.assertEqual(
            parse_qs(result), {"page": ["2"], "new": ["val"]}
        )

    def test_query_transform_no_initial_params(self):
        request = self.factory.get("/test-path")
        result = query_transform(request, page=1)
        self.assertEqual(
            parse_qs(result), {"page": ["1"]}
        )
