from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class PublicTest(TestCase):

    def setUp(self):
        self.urls = [
            reverse("taxi:manufacturer-list"),
            reverse("taxi:driver-list"),
            reverse("taxi:car-list"),
            reverse("taxi:driver-detail", kwargs={"pk": 1}),
            reverse("taxi:car-detail", kwargs={"pk": 1})
        ]

    def test_login_required(self):
        for url in self.urls:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            password="test_pass",
            first_name="test",
            last_name="driver",
            license_number="AAA55555"
        )
        self.client.force_login(self.driver)
        Manufacturer.objects.create(
            name="Test Manufacturer",
            country="United States"
        )

    def test_manufacturer_list(self):

        response = self.client.get(reverse("taxi:manufacturer-list"))
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertEqual(list(response.context["manufacturer_list"]),
                         list(manufacturers))


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            password="test_pass",
            first_name="test",
            last_name="driver",
            license_number="AAA11111"
        )
        self.client.force_login(self.driver)

    def test_driver_list(self):
        response = self.client.get(reverse("taxi:driver-list"))
        drivers = Driver.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertEqual(list(response.context["driver_list"]), list(drivers))


class PrivateCarTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            password="test_pass",
            first_name="test",
            last_name="driver",
            license_number="AAA11111"
        )
        self.client.force_login(self.driver)
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="United States"
        )
        self.car = Car.objects.create(
            manufacturer=self.manufacturer,
            model="Test Model"
        )
        self.car.drivers.add(self.driver)

    def test_car_list(self):
        response = self.client.get(reverse("taxi:car-list"))
        cars = Car.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertEqual(list(response.context["car_list"]), list(cars))
