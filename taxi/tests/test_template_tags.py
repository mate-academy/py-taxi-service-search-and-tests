from django.test import TestCase, RequestFactory

from taxi.templatetags.query_transform import query_transform


class QueryTransformTagTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_add_new_param_to_empty_query(self):
        request = self.factory.get("/")

        result = query_transform(request, page=2)

        self.assertEqual(result, "page=2")

    def test_update_existing_param_and_keep_others(self):
        request = self.factory.get("/?page=1&username=john")

        result = query_transform(request, page=3)

        self.assertIn("page=3", result)
        self.assertIn("username=john", result)
        self.assertEqual(len(result.split("&")), 2)

    def test_remove_param_when_value_is_none(self):
        request = self.factory.get("/?page=2&username=john")

        result = query_transform(request, page=None)

        self.assertEqual(result, "username=john")

    def test_multiple_params_update_and_remove(self):
        request = self.factory.get("/?page=1&username=john&ordering=asc")

        result = query_transform(
            request,
            page=5,
            username=None,
            ordering="desc",
        )

        parts = result.split("&")
        self.assertIn("page=5", parts)
        self.assertIn("ordering=desc", parts)
        self.assertEqual(len(parts), 2)
