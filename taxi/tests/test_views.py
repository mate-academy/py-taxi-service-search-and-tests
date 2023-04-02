from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver

DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicTests(TestCase):
    def test_login_required_driver(self) -> None:
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response, 200)

    def test_login_required_car(self) -> None:
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response, 200)

    def test_login_required_manufacturer(self) -> None:
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test-driver",
            password="testdriver"
        )
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(
            name="German Auto co.",
            country="Germany"
        )
        Car.objects.create(model="Mercedes", manufacturer=manufacturer)
        Car.objects.create(model="BMW", manufacturer=manufacturer)
        Car.objects.create(model="Peugeot", manufacturer=manufacturer)

    def test_get_car_list(self) -> None:
        res = self.client.get(CAR_URL)

        cars = Car.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_search_car(self) -> None:
        key = "e"
        response = self.client.get(reverse("taxi:car-list") + f"?model={key}")

        car_list = Car.objects.filter(model__icontains=key)
        self.assertEqual(
            list(response.context["car_list"]),
            list(car_list)
        )


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test-driver",
            password="testdriver"
        )
        self.client.force_login(self.user)
        Driver.objects.create(username="testdriver1",
                              password="pastest1",
                              license_number="TYU98793")
        Driver.objects.create(username="testdriver2",
                              password="pastest2",
                              license_number="THJ09093")

    def test_get_car_list(self) -> None:
        res = self.client.get(DRIVER_URL)

        drivers = Driver.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_search_driver_with_username(self) -> None:
        key = "driver"
        response = self.client.get(reverse("taxi:driver-list")
                                   + f"?username={key}")

        driver_list = Driver.objects.filter(username__icontains=key)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(driver_list)
        )


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test-driver",
            password="testdriver"
        )
        self.client.force_login(self.user)

        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Mercedes", country="Germany")
        Manufacturer.objects.create(name="Citroen", country="France")

    def test_get_manufac_list(self):
        res = self.client.get(MANUFACTURER_URL)

        manus = Manufacturer.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manus)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_search_driver_with_username(self) -> None:
        key = "i"
        response = self.client.get(reverse("taxi:manufacturer-list")
                                   + f"?name={key}")

        manu_list = Manufacturer.objects.filter(name__icontains=key)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manu_list)
        )
