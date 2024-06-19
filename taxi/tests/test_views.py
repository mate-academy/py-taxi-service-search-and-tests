from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicAllModelsTest(TestCase):

    def test_login_required_manufacturer(self) -> None:
        manuf = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(manuf.status_code, 200)

    def test_login_required_driver(self) -> None:
        driver = self.client.get(DRIVER_URL)
        self.assertNotEqual(driver.status_code, 200)

    def test_login_required_car(self) -> None:
        car = self.client.get(CAR_URL)
        self.assertNotEqual(car.status_code, 200)


class PrivateAllModelsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="Test12345",
            first_name="Test",
            last_name="Test",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self) -> None:
        Manufacturer.objects.create(name="bmw", country="Dutch")
        Manufacturer.objects.create(name="Mercedes", country="Dutch")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_drivers(self) -> None:
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(list(response.context["driver_list"]), list(drivers))

    def test_retrieve_cars(self) -> None:
        manufacturer = Manufacturer.objects.create(name="BMW",
                                                   country="Dutch")

        car = Car.objects.create(manufacturer=manufacturer,
                                 model="Mercedes",
                                 )
        car.drivers.add(self.user)
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]), list(cars))
