from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm, DriverSearchForm, CarSearchForm
from taxi.models import Manufacturer, Driver, Car


class ViewAccessTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="test123"
        )
        self.client.login(username="testuser", password="test123")

        self.manufacturer = Manufacturer.objects.create(
            name="TestMan",
            country="Country"
        )
        self.driver = Driver.objects.create_user(
            username="driver1", password="pass123", license_number="ABC12345"
        )
        self.car = Car.objects.create(
            model="TestCar",
            manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.driver)
        self.protected_url = [
            reverse("taxi:car-list"),
            reverse("taxi:car-create"),
            reverse("taxi:car-update", kwargs={"pk": 1}),
            reverse("taxi:car-delete", kwargs={"pk": 1}),
            reverse("taxi:car-detail", kwargs={"pk": 1}),
            reverse("taxi:driver-list"),
            reverse("taxi:driver-create"),
            reverse("taxi:driver-update", kwargs={"pk": 1}),
            reverse("taxi:driver-delete", kwargs={"pk": 1}),
            reverse("taxi:driver-detail", kwargs={"pk": 1}),
            reverse("taxi:manufacturer-list"),
            reverse("taxi:manufacturer-create"),
            reverse("taxi:manufacturer-update", kwargs={"pk": 1}),
            reverse("taxi:manufacturer-delete", kwargs={"pk": 1}),
        ]

    def test_protected_views_redirect_for_anonymous(self):
        self.client.logout()
        for url in self.protected_url:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn("/accounts/login/", response.url)

    def test_protected_views_accessible_for_logged_user(self):
        self.client.login(username="testuser", password="test123")
        for url in self.protected_url:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)


class ViewsQuerySetTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="TestMan",
            country="Country"
        )
        self.user = get_user_model().objects.create_user(
            username="testuser", password="test123"
        )
        self.client.force_login(self.user)

    def test_car_list_view_queryset_filtered_by_query(self):
        Car.objects.create(model="BMW", manufacturer=self.manufacturer)
        Car.objects.create(model="Audi", manufacturer=self.manufacturer)

        response = self.client.get(reverse("taxi:car-list") + "?model=bmw")
        self.assertEqual(response.status_code, 200)
        cars = response.context["car_list"]
        self.assertEqual(len(cars), 1)
        self.assertEqual(cars[0].model, "BMW")

    def test_driver_list_view_queryset_filtered_by_query(self):
        Driver.objects.create_user(
            username="driver1",
            password="test123",
            license_number="ABC12345"
        )
        Driver.objects.create_user(
            username="driver2",
            password="test1234",
            license_number="ABD12345"
        )

        response = self.client.get(
            reverse("taxi:driver-list") + "?username=driver1"
        )
        self.assertEqual(response.status_code, 200)
        drivers = response.context["driver_list"]
        self.assertEqual(len(drivers), 1)
        self.assertEqual(drivers[0].username, "driver1")

    def test_manufacturer_list_view_queryset_filtered_by_query(self):
        Manufacturer.objects.create(
            name="TestMan1",
            country="TestCountry1"
        )
        Manufacturer.objects.create(
            name="TestMan2",
            country="TestCountry2"
        )

        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=TestMan1"
        )
        self.assertEqual(response.status_code, 200)
        manufacturers = response.context["manufacturer_list"]
        self.assertEqual(len(manufacturers), 1)
        self.assertEqual(manufacturers[0].name, "TestMan1")


class GetContextDataTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="TestMan",
            country="TestCountry"
        )
        self.car = Car.objects.create(
            model="TestCar",
            manufacturer=self.manufacturer
        )
        self.driver = Driver.objects.create_user(
            username="testuser2",
            password="test123",
            license_number="ABC12345"
        )
        self.user = get_user_model().objects.create_user(
            username="testuser", password="test123"
        )
        self.client.force_login(self.user)

    def test_manufacturer_get_context_data(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"], ManufacturerSearchForm
        )
        self.assertEqual(response.context["search_form"].initial["name"], "")

    def test_driver_get_context_data(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)

        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"], DriverSearchForm
        )
        self.assertEqual(
            response.context["search_form"].initial["username"], ""
        )

    def test_car_get_context_data(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)

        self.assertIn("search_form", response.context)
        self.assertIsInstance(response.context["search_form"], CarSearchForm)
        self.assertEqual(response.context["search_form"].initial["model"], "")
