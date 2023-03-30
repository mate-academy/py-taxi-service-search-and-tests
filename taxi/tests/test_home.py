from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


INDEX_URL = reverse("taxi:index")
LOGIN_URL = reverse("login")


class PublicHomeTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_index_login_required(self):
        response = self.client.get(INDEX_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get(LOGIN_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")


class PrivateHomeTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test.user",
            "user12345",
        )
        self.client.force_login(self.user)

    def test_index(self):
        response = self.client.get(INDEX_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")

    def test_visit_counter(self):
        visits = 3

        for visit in range(visits):
            response = self.client.get(INDEX_URL)
            self.assertEqual(response.context["num_visits"], visit + 1)
