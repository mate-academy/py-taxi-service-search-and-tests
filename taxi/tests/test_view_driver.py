from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver

Driver_url = reverse("taxi:driver-list")


class PublicDriverListView(TestCase):
    def test_login_required(self) -> None:
        res = self.client.get(Driver_url)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverListView(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12234",
            license_number="TST00001"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self) -> None:
        response = self.client.get(Driver_url)
        self.assertEqual(response.status_code, 200)
        driver_all = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(driver_all)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_by_name(self) -> None:
        Driver.objects.create_user(
            username="test_1",
            password="test111",
            first_name="test_first_name_1",
            last_name="test_last_name_1",
            license_number="TST11111"
        )
        Driver.objects.create_user(
            username="test_2",
            password="test2",
            first_name="test_first_name_2",
            last_name="test_last_name_2",
            license_number="TST22222"
        )
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"driver": "test_1"}
        )
        self.assertContains(response, "test_1")
        self.assertNotContains(response, "test_2")
