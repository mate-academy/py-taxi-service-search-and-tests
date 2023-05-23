from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverTest(TestCase):
    def test_login_required(self) -> None:
        res = self.client.get(DRIVER_URL)

        self.assertNotEquals(res.status_code, 200)


class PublicCarTest(TestCase):
    def test_login_required(self) -> None:
        res = self.client.get(CAR_URL)

        self.assertNotEquals(res.status_code, 200)


class PublicManufacturerTest(TestCase):
    def test_login_required(self) -> None:
        res = self.client.get(MANUFACTURER_URL)

        self.assertNotEquals(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="Test_driver",
            password="Driver_12345",
        )

        self.client.force_login(self.driver)

    def test_create_driver(self) -> None:
        driver_data = {
            "username": "Driver-123",
            "first_name": "Driver_name",
            "last_name": "Driver_surname",
            "password1": "Test-098765",
            "password2": "Test-098765",
            "license_number": "BTC27656",
        }

        self.client.post(reverse("taxi:driver-create"), data=driver_data)
        new_driver = get_user_model().objects.get(
            username=driver_data["username"]
        )

        self.assertEqual(new_driver.first_name, driver_data["first_name"])
        self.assertEqual(new_driver.last_name, driver_data["last_name"])
        self.assertEqual(
            new_driver.license_number,
            driver_data["license_number"]
        )


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "testUser1",
            "User_654321"
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self) -> None:
        manufacturer_one = Manufacturer.objects.create(name="Manufacturer1")
        manufacturer_two = Manufacturer.objects.create(name="Manufacturer2")

        Car.objects.create(
            model="Model_1",
            manufacturer=manufacturer_one,
        )
        Car.objects.create(
            model="Model_1",
            manufacturer=manufacturer_two,
        )

        response_ = self.client.get(CAR_URL)
        car = Car.objects.all()

        self.assertEquals(response_.status_code, 200)
        self.assertEquals(
            list(response_.context["car_list"]),
            list(car)
        )
        self.assertTemplateUsed(response_, "taxi/car_list.html")


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "testUser2",
            "User_123456"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self) -> None:
        Manufacturer.objects.create(name="Test_manufacturer1")
        Manufacturer.objects.create(name="Test_manufacturer2")

        response_ = self.client.get(MANUFACTURER_URL)
        manufacturer = Manufacturer.objects.all()

        self.assertEquals(response_.status_code, 200)
        self.assertEquals(
            list(response_.context["manufacturer_list"]),
            list(manufacturer)
        )
        self.assertTemplateUsed(response_, "taxi/manufacturer_list.html")
