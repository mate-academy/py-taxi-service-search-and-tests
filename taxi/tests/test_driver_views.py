from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Driver

DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicDriverTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver_list(self):
        Driver.objects.create(username="testuser5", license_number="HGM15157")
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers),
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class DriverSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser5",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_search_by_username(self):
        Driver.objects.create_user(
            username="Ichigo_Kurosaki",
            password="test1234",
            license_number="HGM15157",
            first_name="Ichigo",
            last_name="Kurosaki",
        )
        Driver.objects.create_user(
            username="Isida_Uryu",
            password="test1234",
            license_number="HGM15167",
            first_name="Isida",
            last_name="Uryu",
        )
        response = self.client.get(
            reverse("taxi:driver-list")
            + "?username=Ichigo"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ichigo")
        self.assertNotContains(response, "Isida")
