from django.test import TestCase, RequestFactory

from taxi.templatetags.query_transform import query_transform


class QueryTransformTests(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_adds_parameter_and_keeps_existing(self):
        request = self.factory.get("/drivers/", {"username": "john"})
        self.assertEqual(
            query_transform(request, page=2), "username=john&page=2"
        )

    def test_replaces_existing_parameter(self):
        request = self.factory.get("/drivers/", {"page": 1})
        self.assertEqual(query_transform(request, page=2), "page=2")

    def test_removes_parameter_with_none_value(self):
        request = self.factory.get(
            "/drivers/", {"username": "john", "page": 1}
        )
        self.assertEqual(
            query_transform(request, page=None), "username=john"
        )
