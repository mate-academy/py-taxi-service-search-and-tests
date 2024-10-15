from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicTest(TestCase):
    def test_login_required_for_manufacturer_list_page(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_driver_list_page(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_car_list_page(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Volvo", country="Sweden")
        cls.car1 = Car.objects.create(
            model="M4",
            manufacturer=Manufacturer.objects.get(id=1)
        )
        cls.car2 = Car.objects.create(
            model="XC60",
            manufacturer=Manufacturer.objects.get(id=2)
        )
        Driver.objects.create(
            username="test_user_1",
            password="Test1234!",
            license_number="AAA00001"
        )
        Driver.objects.create(
            username="test_user_2",
            password="Test1234!",
            license_number="AAA00002"
        )

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="Test1234!",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_URL)
        drivers = Driver.objects.exclude(username=self.user.username)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )

    def test_retrieve_cars(self):
        response = self.client.get(CAR_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

    def test_assign_car_to_driver(self):
        driver = Driver.objects.get(id=self.user.id)
        self.assertFalse(driver.cars.exists())

        response = self.client.post(reverse(
            "taxi:toggle-car-assign",
            args=[self.car1.id]
        ))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(driver.cars.filter(id=self.car1.id).exists())

    def test_remove_car_from_driver(self):
        driver = Driver.objects.get(id=self.user.id)
        driver.cars.add(self.car2)

        self.assertTrue(driver.cars.filter(id=self.car2.id).exists())
        response = self.client.post(reverse(
            "taxi:toggle-car-assign",
            args=[self.car2.id]
        ))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(driver.cars.filter(id=self.car2.id).exists())
