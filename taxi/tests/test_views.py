from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

DRIVER_LIST_URL = reverse("taxi:driver-list")


class DriverListViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass1",
            license_number="ABC12341"
        )
        self.driver1 = get_user_model().objects.create_user(
            username="alica_black",
            password="testpass2",
            license_number="ABC12346"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="jennifer_lopez",
            password="testpass3",
            license_number="ABC12347"
        )

    def test_login_required(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

        self.client.force_login(self.user)
        res = self.client.get(DRIVER_LIST_URL)
        self.assertEquals(res.status_code, 200)

    def test_search_by_username(self):
        self.client.force_login(self.user)
        res = self.client.get(DRIVER_LIST_URL + "?username=pez")
        self.assertContains(res, "jennifer_lopez")
        self.assertNotContains(res, "alica_black")
        res = self.client.get(DRIVER_LIST_URL + "?username=lic")
        self.assertContains(res, "alica_black")
        self.assertNotContains(res, "jennifer_lopez")
