from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()


class PublicAccessTest(BaseTestCase):
    def test_manufacturer_access(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_car_access(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_access(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateAccessTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="Porsche SE")
        Manufacturer.objects.create(name="Stellantis")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturer = Manufacturer.objects.all()
        self.assertEqual(
            list(
                response.context["manufacturer_list"]), list(manufacturer)
        )

        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html"
        )

    def test_retrieve_car(self):
        manufacturer = Manufacturer.objects.create(name="Porsche SE")
        Car.objects.create(model="Porsche", manufacturer=manufacturer)
        Car.objects.create(model="Citroen", manufacturer=manufacturer)
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        car = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]), list(car))

        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_driver(self):
        Driver.objects.create(username="driver1", license_number="MIG43985")
        Driver.objects.create(username="driver2", license_number="KLE07329")
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        driver = Driver.objects.all()
        self.assertEqual(list(response.context["driver_list"]), list(driver))

        self.assertTemplateUsed(response, "taxi/driver_list.html")
