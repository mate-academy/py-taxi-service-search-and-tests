from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

INDEX_URL = reverse("taxi:index")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
CAR_LIST_URL = reverse("taxi:car-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        response_index = self.client.get(INDEX_URL)
        response_manufacturer = self.client.get(MANUFACTURER_LIST_URL)
        response_driver = self.client.get(DRIVER_LIST_URL)
        response_car = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response_index.status_code, 200)
        self.assertNotEqual(response_manufacturer.status_code, 200)
        self.assertNotEqual(response_driver.status_code, 200)
        self.assertNotEqual(response_car.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country",
        )
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)

        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )

        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_driver(self) -> None:
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)

        drivers = get_user_model().objects.all()
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_retrieve_car(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country"
        )
        Car.objects.create(model="test_model", manufacturer=manufacturer)
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)

        cars = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")
