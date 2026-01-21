from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicTest(TestCase):
    def test_login_required_for_manufacturer_list(self) -> None:
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_for_driver_list(self) -> None:
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_for_car_list(self) -> None:
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="password",
        )
        self.client.force_login(self.user)

    def test_receive_manufacturer_list(self) -> None:
        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="Dodge", country="USA")
        res = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertQuerysetEqual(
            res.context["manufacturer_list"],
            manufacturers,
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_receive_driver_list(self) -> None:
        Driver.objects.create(username="user1", license_number="QWE12345")
        Driver.objects.create(username="user2", license_number="QWE12346")
        res = self.client.get(DRIVER_URL)
        drivers = Driver.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertQuerysetEqual(
            res.context["driver_list"], drivers, ordered=False
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_receive_car_list(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="GM", country="USA"
        )
        Car.objects.create(model="Mustang", manufacturer=manufacturer)
        Car.objects.create(model="Focus", manufacturer=manufacturer)
        res = self.client.get(CAR_URL)
        cars = Car.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertQuerysetEqual(res.context["car_list"], cars, ordered=False)
        self.assertTemplateUsed(res, "taxi/car_list.html")
