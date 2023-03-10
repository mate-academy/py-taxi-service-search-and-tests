from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class PublicIndexTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required_car_list(self):
        res = self.client.get(
            reverse("taxi:index")
        )

        self.assertNotEqual(res.status_code, 200)


class PrivateIndexTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model(
        ).objects.create_user(
            "test",
            "password123",
        )
        self.client.force_login(self.user)

    def test_retrieve_index(self):
        response = self.client.get(
            reverse("taxi:index")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "taxi/index.html"
        )
