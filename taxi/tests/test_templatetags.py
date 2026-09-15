from django.test import RequestFactory, TestCase

from taxi.templatetags.query_transform import query_transform


class TemplateTagsTests(TestCase):
    def test_query_transform(self):
        factory = RequestFactory()
        request = factory.get("/cars/?model=Camry&page=1")
        context = {"request": request}

        result = query_transform(context, page=2)
        self.assertIn("page=2", result)
        self.assertIn("model=Camry", result)

        result_new_param = query_transform(context, sort="name")
        self.assertIn("sort=name", result_new_param)
        self.assertIn("model=Camry", result_new_param)
        self.assertIn("page=1", result_new_param)
