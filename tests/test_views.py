from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

URL_MANUFACTURER_LIST = reverse("taxi:manufacturer-list")
URL_DRIVER_LIST = reverse("taxi:driver-list")
URL_CAR_LIST = reverse("taxi:car-list")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        response = self.client.get(URL_MANUFACTURER_LIST)
        self.assertNotEqual(
            response.status_code,
            200,
        )


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "user",
            "user1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="BMW")
        Manufacturer.objects.create(name="AUDI")
        res = self.client.get(URL_MANUFACTURER_LIST)
        manufacturer_list = Manufacturer.objects.all()

        self.assertEqual(
            res.status_code,
            200
        )
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturer_list)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_search_manufacturer_form(self):
        Manufacturer.objects.create(name="BMW")
        Manufacturer.objects.create(name="AUDI")
        res = self.client.get(URL_MANUFACTURER_LIST + "?name=BMW")

        self.assertContains(
            res,
            "BMW"
        )
        self.assertNotContains(
            res,
            "AUDI"
        )


class PublicCarTests(TestCase):
    def test_login_required(self):
        response = self.client.get(URL_CAR_LIST)
        self.assertNotEqual(
            response.status_code,
            200,
        )


class PrivateCarTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "user",
            "user1234"
        )
        self.client.force_login(self.user)
        self.test_man_1 = Manufacturer.objects.create(name="BMW")
        self.test_man_2 = Manufacturer.objects.create(name="AUDI")

    def test_retrieve_car(self):
        Car.objects.create(model="X4", manufacturer=self.test_man_1)
        res = self.client.get(URL_CAR_LIST)
        car_list = Car.objects.all()

        self.assertEqual(
            res.status_code,
            200
        )
        self.assertEqual(
            list(res.context["car_list"]),
            list(car_list)
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_retrieve_car_detail(self):
        Car.objects.create(model="X4", manufacturer=self.test_man_1)
        res = self.client.get(URL_CAR_LIST + "1/")

        self.assertEqual(
            res.status_code,
            200
        )

        self.assertTemplateUsed(
            res,
            "taxi/car_detail.html"
        )

    def test_search_car_form(self):
        Car.objects.create(model="X4", manufacturer=self.test_man_1)
        Car.objects.create(model="X5", manufacturer=self.test_man_2)
        res = self.client.get(URL_CAR_LIST + "?car_model=X4")

        self.assertContains(
            res,
            "X4"
        )
        self.assertNotContains(
            res,
            "X5"
        )


class PublicDriverTests(TestCase):
    def test_login_required(self):
        response = self.client.get(URL_DRIVER_LIST)
        self.assertNotEqual(
            response.status_code,
            200,
        )


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "user",
            "user1234"
        )
        self.client.force_login(self.user)
        self.test_driver_1 = Driver.objects.create(
            license_number="ABC12345",
            username="heisenberg",
            first_name="Walter",
            last_name="White"
        )
        self.test_driver_1 = Driver.objects.create(
            license_number="BCD12345",
            username="jimmy.beam",
            first_name="Jimmy",
            last_name="Beam"
        )

    def test_retrieve_driver(self):
        res = self.client.get(URL_DRIVER_LIST)
        driver_list = Driver.objects.all()

        self.assertEqual(
            res.status_code,
            200
        )
        self.assertEqual(
            list(res.context["driver_list"]),
            list(driver_list)
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_retrieve_driver_detail(self):
        res = self.client.get(URL_DRIVER_LIST + "1/")

        self.assertEqual(
            res.status_code,
            200
        )

        self.assertTemplateUsed(
            res,
            "taxi/driver_detail.html"
        )

    def test_search_driver_form(self):
        res = self.client.get(URL_CAR_LIST + "?car_model=heisenberg")

        self.assertContains(
            res,
            "heisenberg"
        )
        self.assertNotContains(
            res,
            "jimmy.beam"
        )
