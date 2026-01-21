from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from taxi.models import Driver, Manufacturer, Car

DRIVER_URL = reverse("taxi:driver-list")
MANUFACTURER_ULR = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")


class PrivateModelsViewTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="Schumacher", password="formula1"
        )
        self.client.force_login(self.driver)
        self.manufacturer_instance = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.manufacturer_instance_two = Manufacturer.objects.create(
            name="Tesla", country="USA"
        )
        self.car_instance = Car.objects.create(
            model="Supra", manufacturer=self.manufacturer_instance
        )

    def test_retrieve_driver_list(self) -> None:
        test_response = self.client.get(DRIVER_URL)
        self.assertEqual(test_response.status_code, 200)
        all_drivers = Driver.objects.all()
        self.assertEqual(all_drivers.count(), 1)
        self.assertTemplateUsed(test_response, "taxi/driver_list.html")

    def test_retrieve_manufacturer_list(self):
        test_response = self.client.get(MANUFACTURER_ULR)
        self.assertEqual(test_response.status_code, 200)
        all_manufacturers = Manufacturer.objects.all()
        self.assertEqual(all_manufacturers.count(), 2)
        self.assertTemplateUsed(test_response, "taxi/manufacturer_list.html")

    def test_retrieve_car_list(self):
        test_response = self.client.get(CAR_URL)
        self.assertEqual(test_response.status_code, 200)
        all_cars = Car.objects.all()
        self.assertEqual(all_cars.count(), 1)
        self.assertTemplateUsed(test_response, "taxi/car_list.html")
