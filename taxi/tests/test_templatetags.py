from django.test import RequestFactory, SimpleTestCase

from taxi.templatetags.query_transform import query_transform


class QueryTransformTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_replaces_page_and_keeps_search_query(self):
        request = self.factory.get("/cars/", {"model": "focus", "page": 1})
        self.assertEqual(
            query_transform(request, page=2), "model=focus&page=2"
        )

    def test_adds_page_when_there_is_no_query(self):
        request = self.factory.get("/cars/")
        self.assertEqual(query_transform(request, page=2), "page=2")

    def test_removes_parameter_passed_as_none(self):
        request = self.factory.get("/cars/", {"model": "focus", "page": 3})
        self.assertEqual(query_transform(request, page=None), "model=focus")

    def test_does_not_change_the_request(self):
        request = self.factory.get("/cars/", {"model": "focus", "page": 1})
        query_transform(request, page=2)
        self.assertEqual(request.GET["page"], "1")
