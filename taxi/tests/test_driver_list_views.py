from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver

DRIVERS_URL = reverse("taxi:driver-list")
TEMPLATE_NAME = "taxi/driver_list.html"
CONTEXT_OBJECT_NAME = "driver_list"
TEST_DATA_1 = {
    "username": "test_1",
    "password": "test111",
    "first_name": "test_first_name_1",
    "last_name": "test_last_name_1",
    "license_number": "TST11111"
}
TEST_DATA_2 = {
    "username": "test_2",
    "password": "test222",
    "first_name": "test_first_name_2",
    "last_name": "test_last_name_2",
    "license_number": "TST22222"
}


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVERS_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="123"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        Driver.objects.create(**TEST_DATA_1)
        Driver.objects.create(**TEST_DATA_2)
        res = self.client.get(DRIVERS_URL)
        self.assertEqual(res.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(res.context[CONTEXT_OBJECT_NAME]),
            list(drivers)
        )
        self.assertTemplateUsed(
            res, TEMPLATE_NAME
        )

    def test_search_drivers(self):
        d1 = Driver.objects.create(**TEST_DATA_1)
        d2 = Driver.objects.create(**TEST_DATA_2)
        query = TEST_DATA_1["username"][-3:]

        res = self.client.get(
            DRIVERS_URL, {"username": query}
        )
        self.assertEqual(
            res.context["search_form"].initial["username"], query
        )
        self.assertIn(d1, res.context[CONTEXT_OBJECT_NAME])
        self.assertNotIn(d2, res.context[CONTEXT_OBJECT_NAME])
