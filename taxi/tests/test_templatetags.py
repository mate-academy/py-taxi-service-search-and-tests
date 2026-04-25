from django.test import TestCase, RequestFactory
from urllib.parse import parse_qs

from taxi.templatetags.query_transform import query_transform


class QueryTransformTagTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def _qs_to_dict(self, qs):
        # parse_qs returns values as lists;
        # normalize to single values for assertions
        parsed = parse_qs(qs, keep_blank_values=True)
        return {k: v if len(v) > 1 else v[0] for k, v in parsed.items()}

    def test_updates_existing_param(self):
        req = self.factory.get("/?a=1&b=2")
        result = query_transform(req, a="42")
        assert self._qs_to_dict(result) == {"a": "42", "b": "2"}

    def test_removes_param_when_value_is_none(self):
        req = self.factory.get("/?a=1&b=2")
        result = query_transform(req, b=None)
        assert self._qs_to_dict(result) == {"a": "1"}

    def test_adds_new_param(self):
        req = self.factory.get("/?a=1")
        result = query_transform(req, page="3")
        assert self._qs_to_dict(result) == {"a": "1", "page": "3"}
