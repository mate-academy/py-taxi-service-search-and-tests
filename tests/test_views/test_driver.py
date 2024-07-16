from django.contrib.auth import get_user_model
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car
from taxi.views import DriverListView

DRIVER_URL = reverse("taxi:driver-list")


class TestLoginRequired(TestCase):

    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class TestDriverListView(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test", password="testpass"
        )
        self.client.force_login(self.user)

    def test_paginates_driver_list_with_5_per_page(self):
        request = RequestFactory().get(reverse("taxi:driver-list"))
        request.user = Driver.objects.create_user(
            username="testuser12", password="12345", license_number="KJH23456"
        )
        response = DriverListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data["paginator"].per_page, 5)

    def test_display_correct_driver_list_information(self):
        Driver.objects.create(
            username="testuser12",
            password="<PASSWORD>",
            first_name="test_first",
            last_name="test_last",
            license_number="KJH23456",
        )
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser12")
        self.assertContains(response, "test_first")
        self.assertContains(response, "test_last")
        self.assertContains(response, "KJH23456")


class TestDriverDetailView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass",
        )
        self.client.login(username="testuser", password="testpass")

    def test_drivers_detail_view(self):
        driver = Driver.objects.create(
            username="test_driver",
            first_name="Test",
            last_name="Driver",
            license_number="12345",
        )
        response = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test")
        self.assertContains(response, "Driver")
        self.assertContains(response, "12345")

    def test_display_associated_cars_and_manufacturers(self):
        driver = Driver.objects.create(
            username="test_driver",
            first_name="John",
            last_name="Doe",
            license_number="12345",
        )
        manufacturer = Manufacturer.objects.create(name="Test Manufacturer")
        car = Car.objects.create(model="Test Car", manufacturer=manufacturer)
        driver.cars.add(car)
        response = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Car")
        self.assertContains(response, "Test Manufacturer")

    def test_correct_html(self):
        driver = Driver.objects.create(
            username="test_driver",
            first_name="Test",
            last_name="Driver",
            license_number="12345",
        )
        response = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        )
        self.assertTemplateUsed(response, "taxi/driver_detail.html")
