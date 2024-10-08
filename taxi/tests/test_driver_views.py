from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Manufacturer

DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicDriverTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.driver = Driver.objects.create(
            username="testdriver",
            password="testpass123",
            first_name="Test",
            last_name="Driver",
            license_number="XYZ12345"
        )

    def test_login_required(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_detail_view_requires_login(self):
        response = self.client.get(reverse(
            "taxi:driver-detail",
            args=[self.driver.id]
        ))
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.driver1 = Driver.objects.create(
            username="driver1",
            password="testpass123",
            first_name="First",
            last_name="Driver",
            license_number="ABC12345"
        )
        self.driver2 = Driver.objects.create(
            username="driver2",
            password="testpass123",
            first_name="Second",
            last_name="Driver",
            license_number="XYZ67890"
        )

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_LIST_URL)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_get_context_data(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "driver1"})
        search_form = response.context["search_form"]
        self.assertEqual(search_form.initial["username"], "driver1")

    def test_get_queryset_with_search(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "driver1"})
        drivers = Driver.objects.filter(username__icontains="driver1")
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
