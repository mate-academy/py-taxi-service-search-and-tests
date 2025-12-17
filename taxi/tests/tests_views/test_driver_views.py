from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver

DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")


class PublicDriverTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.driver = get_user_model().objects.create(
            username="test",
            first_name="test",
            last_name="test"
        )

    def test_login_required_list(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_create(self):
        res = self.client.get(DRIVER_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_update(self):
        url = reverse("taxi:driver-update", args=[self.driver.id])
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_delete(self):
        url = reverse("taxi:driver-delete", args=[self.driver.id])
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test",
            first_name="test",
            last_name="test",
        )

        self.client.force_login(self.driver)

    def test_retrieve_driver_list(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(list(response.context["driver_list"]),
                         list(drivers))
        self.assertTemplateUsed(response,
                                "taxi/driver_list.html")
