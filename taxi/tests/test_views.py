from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")
MANUFACTURER_AFTER_SEARCH_URL = reverse("taxi:manufacturer-list") + "?name=d"
CAR_AFTER_SEARCHING_URL = reverse("taxi:car-list") + "?model=i"
DRIVER_AFTER_SEARCHING_URL = reverse("taxi:driver-list") + "?username=d"


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test_user",
            "passwordtest6567",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="Teslemod",
            country="Higurashi"
        )
        Manufacturer.objects.create(
            name="WayneInc",
            country="USA"
        )

        res = self.client.get(MANUFACTURER_URL)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def retrieve_manufacturers_after_search(self):
        manufacturers = Manufacturer.objects.filter(
            name__icontains="d"
        )
        res = self.client.get(MANUFACTURER_AFTER_SEARCH_URL)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")


class PublicCarTests(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateCarTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test_user",
            "passwordtest6567",
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="TestoManu",
            country="BangLand"
        )

        self.car = Car.objects.create(
            model="TestMod",
            manufacturer=self.manufacturer
        )

    def test_retrieve_car(self):
        cars = Car.objects.all()
        response = self.client.get(CAR_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_after_search_car(self):
        cars = Car.objects.filter(model__icontains="i")
        res = self.client.get(CAR_AFTER_SEARCHING_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")


class PublicDriverTests(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "passsyh7y6",
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "test_username",
            "password1": "pass688uJH",
            "password2": "pass688uJH",
            "license_number": "FRG54345",
            "first_name": "Test First",
            "last_name": "Test Last",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_retrieve_driver_after_search(self):
        drivers = get_user_model().objects.filter(
            username__icontains="d"
        )
        res = self.client.get(DRIVER_AFTER_SEARCHING_URL)

        self.assertEqual(
            list(res.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")
