from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicCarTests(TestCase):

    def test_login_required_for_car_list(self):
        res = self.client.get(CAR_LIST_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="User123",
            password="qwer1234"
        )
        self.manufacturer = Manufacturer.objects.create(name="Test")
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        Car.objects.create(model="Car1", manufacturer=self.manufacturer)
        Car.objects.create(model="Car2", manufacturer=self.manufacturer)

        response = self.client.get(CAR_LIST_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_car_form(self):
        manufacturer = Manufacturer.objects.create(name="Test123")
        Car.objects.create(model="test1", manufacturer=manufacturer)
        Car.objects.create(model="test2", manufacturer=manufacturer)
        url = CAR_LIST_URL + "?model=test1"
        res = self.client.get(url)

        self.assertContains(res, "test1")
        self.assertNotContains(res, "test2")


class PublicManufacturerTests(TestCase):

    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="User123",
            password="qwer1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="Test1")
        Manufacturer.objects.create(name="Test2")

        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturer_form(self):
        Manufacturer.objects.create(name="test1", country="test1")
        Manufacturer.objects.create(name="test2", country="test2")
        url = MANUFACTURER_URL + "?name=test1"
        res = self.client.get(url)

        self.assertContains(res, "test1")
        self.assertNotContains(res, "test2")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
             username="User123",
             password="qwer1234"
         )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "TestUser",
            "password1": "qwer1234!",
            "password2": "qwer1234!",
            "license_number": "ASD12341",
            "first_name": "test_name",
            "last_name": "test_last_name"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_search_driver_form(self):
        get_user_model().objects.create_user(
            username="test1",
            password="test1234",
            license_number="ASD12345")
        get_user_model().objects.create_user(
            username="test2",
            password="test1234",
            license_number="ASD12346")
        url = DRIVER_URL + "?username=test1"
        res = self.client.get(url)

        self.assertContains(res, "test1")
        self.assertNotContains(res, "test2")
