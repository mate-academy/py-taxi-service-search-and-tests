from django.test import Client, TestCase
from django.urls import reverse


URL = reverse("taxi:car-list")


class PublickCarFormatTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self) -> None:
        res = self.client.get(URL)
        self.assertNotEqual(res.status_code, 200)
