from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

URL_MANUFACTURER_LIST = reverse("taxi:manufacturer-list")
URL_DRIVER_LIST = reverse("taxi:driver-list")
URL_CAR_LIST = reverse("taxi:car-list")


class PublicDriverTests(TestCase):
    def test_login_required(self):
        response = self.client.get(URL_DRIVER_LIST)

        self.assertNotEqual(
            response.status_code,
            200,
        )


class PrivateDriverTests(TestCase):
    def setUp(self):
        Driver.objects.create(
            username="ace_ventura",
            first_name="Jim",
            last_name="Carrey",
            license_number="JJJ55555"
        )
        Driver.objects.create(
            username="neo",
            first_name="Keanu",
            last_name="Reeves",
            license_number="KKK11111",
        )
        self.user = get_user_model().objects.create_user(
            "test",
            "test1234"
        )
        self.client.force_login(self.user)

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
        res = self.client.get(URL_DRIVER_LIST + "?username=neo")

        self.assertContains(
            res,
            "neo"
        )
        self.assertNotContains(
            res,
            "ace_ventura"
        )


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        response = self.client.get(URL_MANUFACTURER_LIST)

        self.assertNotEqual(
            response.status_code,
            200,
        )


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        Manufacturer.objects.create(name="Mazda")
        Manufacturer.objects.create(name="Opel")

        self.user = get_user_model().objects.create_user(
            "test",
            "test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
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
        res = self.client.get(URL_MANUFACTURER_LIST + "?name=opel")

        self.assertContains(
            res,
            "opel"
        )
        self.assertNotContains(
            res,
            "mazda"
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
        mazda = Manufacturer.objects.create(name="Mazda")
        opel = Manufacturer.objects.create(name="Opel")
        Car.objects.create(
            model="Miata",
            manufacturer=mazda
        )
        Car.objects.create(
            model="Vectra",
            manufacturer=opel
        )

        self.user = get_user_model().objects.create_user(
            "test",
            "test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
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
        res = self.client.get(URL_CAR_LIST + "?model=Vectra")

        self.assertContains(
            res,
            "Vectra"
        )
        self.assertNotContains(
            res,
            "Miata"
        )
