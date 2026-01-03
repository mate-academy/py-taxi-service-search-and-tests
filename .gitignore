from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

INDEX_URL = reverse("taxi:index")


class PublicIndexTest(TestCase):
    def test_login_required(self):
        res = self.client.get(INDEX_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateIndexTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="test",
            password="test1234"
        )
        self.client.force_login(self.user)

    def test_template_response(self):
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")
