from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car, Driver

CARS_URL = reverse("taxi:car-list")
MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
DRIVERS_URL = reverse("taxi:driver-list")


class PublicModelTests(TestCase):
    def test_login_required(self):
        result = self.client.get(CARS_URL)
        result1 = self.client.get(MANUFACTURERS_URL)
        result2 = self.client.get(DRIVERS_URL)
        self.assertNotEquals(result.status_code, 200)
        self.assertNotEquals(result1.status_code, 200)
        self.assertNotEquals(result2.status_code, 200)


class PrivateModelTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="AUDI", country="Germany")
        Manufacturer.objects.create(name="Volkswagen", country="Germany")
        response = self.client.get(MANUFACTURERS_URL)
        self.assertEquals(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEquals(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="AUDI", country="Germany"
        )
        Car.objects.create(model="AUDI100", manufacturer=manufacturer)
        Car.objects.create(model="AUDI200", manufacturer=manufacturer)

        response = self.client.get(CARS_URL)
        self.assertEquals(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEquals(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_driver(self):
        Driver.objects.create(
            username="driver1_test", license_number="MMM99999"
        )
        Driver.objects.create(
            username="driver2_test", license_number="KKK98765"
        )
        response = self.client.get(DRIVERS_URL)
        self.assertEqual(response.status_code, 200)
        driver = Driver.objects.all()
        self.assertEqual(list(response.context["driver_list"]), list(driver))

        self.assertTemplateUsed(response, "taxi/driver_list.html")
