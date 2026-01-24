from django.test import RequestFactory, TestCase
from taxi.templatetags.query_transform import query_transform


class QueryTransformTest(TestCase):

    def test_query_transform(self):
        self.factory = RequestFactory()
        request = self.factory.get("/drivers/?username=Name")

        result = query_transform(request, page=2)

        self.assertEqual(result, "username=Name&page=2")
