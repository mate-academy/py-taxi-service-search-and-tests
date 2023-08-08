from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)

        self.assertNotEquals(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="test_name1", country="test_country1")
        Manufacturer.objects.create(name="test_name2", country="test_country2")

        res = self.client.get(MANUFACTURER_URL)
        manufacturer = Manufacturer.objects.all()

        self.assertEquals(res.status_code, 200)
        self.assertEquals(
            list(res.context["manufacturer_list"]),
            list(manufacturer)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_manufacturer_search(self):
        Manufacturer.objects.create(name="test_name3", country="test_country3")
        res = self.client.get(MANUFACTURER_URL)
        search = Manufacturer.objects.filter(name="test_name3")
        self.assertEquals(res.status_code, 200)
        self.assertEquals(list(res.context["manufacturer_list"]), list(search))


class PublicCarTests(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="car_user",
            password="car_password"
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Volkswagen",
            country="Germany"
        )
        Car.objects.create(model="Golf", manufacturer=manufacturer)

        res = self.client.get(CAR_URL)
        car = Car.objects.all()
        self.assertEquals(res.status_code, 200)
        self.assertEquals(list(res.context["car_list"]), list(car))

    def test_search_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Audi", country="Germany"
        )
        Car.objects.create(model="Q6", manufacturer=manufacturer)
        res = self.client.get(CAR_URL)
        search = Car.objects.filter(model="Q6")
        self.assertEquals(res.status_code, 200)
        self.assertEquals(list(res.context["car_list"]), list(search))


class PublicDriverTests(TestCase):
    def test_login_required(self) -> None:
        res = self.client.get(DRIVER_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        get_user_model().objects.create(
            username="username",
            first_name="first_name",
            last_name="last_name",
            license_number="ASW86418"
        )
        get_user_model().objects.create(
            username="black13",
            first_name="john",
            last_name="white",
            license_number="QWE89354"
        )
        res = self.client.get(DRIVER_URL)
        driver = get_user_model().objects.all()
        self.assertEquals(res.status_code, 200)
        self.assertEquals(list(res.context["driver_list"]), list(driver))

    def test_search_driver(self):
        res = self.client.get(DRIVER_URL, {"username": "limon13"})
        search = get_user_model().objects.filter(username="limon13")
        self.assertEquals(res.status_code, 200)
        self.assertEquals(list(res.context["driver_list"]), list(search))
