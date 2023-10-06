from django.http import QueryDict
from django.template import RequestContext
from django.template.loader import render_to_string
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from taxi.templatetags.query_transform import query_transform


class QueryTransformTagTest(TestCase):

    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_query_transform_correct_path(self) -> None:
        request = self.factory.get(reverse("taxi:car-list"))
        request.GET = QueryDict("?search=test")

        render = query_transform(request, page=2)

        expected = "%3Fsearch=test&page=2"
        self.assertEquals(render, expected)
