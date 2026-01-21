from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Car, Manufacturer, Driver

DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicTest(TestCase):
    def test_login_car_required(self):
        response_car = self.client.get(CAR_URL)
        self.assertNotEqual(response_car.status_code, 200)

    def test_login_driver_required(self):
        response_driver = self.client.get(DRIVER_URL)
        self.assertNotEqual(response_driver.status_code, 200)

    def test_login_manufacturer_required(self):
        response_manufacturer = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response_manufacturer.status_code, 200)


class PrivateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="<PASSWORD123>",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="BMW", country="Brazil")
        Manufacturer.objects.create(name="AUDI", country="Germany")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html")

    def test_retrieve_cars(self):
        driver = Driver.objects.create(
            username="testuser",
            license_number="ASD12345"
        )
        bmw = Manufacturer.objects.create(name="BMW", country="Brazil")
        audi = Manufacturer.objects.create(name="AUDI", country="Germany")

        car1 = Car.objects.create(model="testbmw", manufacturer=bmw)
        car2 = Car.objects.create(model="testaudi", manufacturer=audi)

        car1.drivers.add(driver)
        car2.drivers.add(driver)

        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_drivers(self):
        Driver.objects.create(
            username="testuser",
            license_number="ASD12345"
        )
        Driver.objects.create(
            username="testuser1",
            license_number="ASD12341"
        )

        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
