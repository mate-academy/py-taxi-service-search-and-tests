from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver

CARS_URL = reverse("taxi:car-list")
DRIVERS_URL = reverse("taxi:driver-list")
MANUFACTURERS_URL = reverse("taxi:manufacturer-list")


class PublicAccessTests(TestCase):
    def test_login_required(self):
        response = self.client.get(CARS_URL)
        self.assertNotEqual(response.status_code, 200)

        response = self.client.get(DRIVERS_URL)
        self.assertNotEqual(response.status_code, 200)

        response = self.client.get(MANUFACTURERS_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test1234",
        )
        self.client.force_login(self.user)

        manufacturer = Manufacturer.objects.create(
            name="HAVAL",
            country="Chine"
        )
        Car.objects.create(
            model="H6",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="M4",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="H6 turbo",
            manufacturer=manufacturer
        )

    def test_retrieve_cars(self):
        response = self.client.get(CARS_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_car_detail(self):
        response = self.client.get(reverse("taxi:car-detail", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")

    def test_car_search(self):
        response = self.client.get(CARS_URL + "?model=H6")
        self.assertContains(response, "H6 turbo")


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test1234",
        )
        self.client.force_login(self.user)

        Driver.objects.create(
            username="test_driver",
            first_name="Test",
            last_name="Driver",
            license_number="HHH12345"
        )

    def test_retrieve_drivers(self):
        res = self.client.get(DRIVERS_URL)
        driver_list = Driver.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["driver_list"]), list(driver_list))
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_retrieve_driver_detail(self):
        response = self.client.get(reverse("taxi:driver-detail", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_driver_search(self):
        response = self.client.get(DRIVERS_URL + "?user_name=test")
        self.assertContains(response, "test_driver")


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test1234",
        )
        self.client.force_login(self.user)

        Manufacturer.objects.create(
            name="HAVAL",
            country="Chine"
        )
        Manufacturer.objects.create(
            name="Nissan",
            country="Japan"
        )

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_search(self):
        response = self.client.get(MANUFACTURERS_URL + "?name=HAVAL")
        self.assertContains(response, "HAVAL")
