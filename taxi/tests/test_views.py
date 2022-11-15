from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

INDEX = reverse("taxi:index")
LOGIN = reverse("login")
MANUFACTURER_LIST = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE = reverse("taxi:manufacturer-create")
CAR_LIST = reverse("taxi:car-list")
CAR_CREATE = reverse("taxi:car-create")
DRIVER_LIST = reverse("taxi:driver-list")
DRIVER_CREATE = reverse("taxi:driver-create")


class PublicTests(TestCase):
    def test_login_required_for_index(self):
        res = self.client.get(INDEX)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_for_manufacturer_list(self):
        res = self.client.get(MANUFACTURER_LIST)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_for_manufacturer_create(self):
        res = self.client.get(MANUFACTURER_CREATE)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_for_car_list(self):
        res = self.client.get(CAR_LIST)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_for_car_create(self):
        res = self.client.get(CAR_CREATE)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_for_driver_list(self):
        res = self.client.get(DRIVER_LIST)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_for_driver_create(self):
        res = self.client.get(DRIVER_CREATE)
        self.assertNotEqual(res.status_code, 200)


class PrivateTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password1234",
        )
        self.client.force_login(self.user)

    def test_index_page(self):
        res = self.client.get(INDEX)

        self.assertEqual(res.status_code, 200)

    def test_login_page(self):
        res = self.client.get(LOGIN)

        self.assertEqual(res.status_code, 200)

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(name="test_v1", country="test_v1")
        Manufacturer.objects.create(name="test_v2", country="test_v2")
        res = self.client.get(MANUFACTURER_LIST)
        manufacture_list = Manufacturer.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]), list(manufacture_list)
        )

        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_retrieve_car_list(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name", country="test_country"
        )
        Car.objects.create(model="test_v1", manufacturer=manufacturer)
        Car.objects.create(model="test_v2", manufacturer=manufacturer)
        res = self.client.get(CAR_LIST)
        car_list = Car.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["car_list"]), list(car_list))

        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_retrieve_driver_list(self):
        res = self.client.get(DRIVER_LIST)

        self.assertEqual(res.status_code, 200)


class CreateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user("test", "1qazcde3")
        self.client.force_login(self.user)

    def test_create_driver(self):
        from_data = {
            "username": "username",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
            "first_name": "test_name",
            "last_name": "test_surname",
            "license_number": "AAA00001",
        }

        self.client.post(reverse("taxi:driver-create"), data=from_data)
        new_user = get_user_model().objects.get(username=from_data["username"])

        self.assertEqual(new_user.first_name, from_data["first_name"])
        self.assertEqual(new_user.last_name, from_data["last_name"])
        self.assertEqual(new_user.license_number, from_data["license_number"])


class TestSearch(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password1234",
        )
        self.client.force_login(self.user)

    def test_manufacturer_search(self):
        response = self.client.get("/manufacturers/?name=i")

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            Manufacturer.objects.filter(name__icontains="i")
        )

    def test_car_search(self):
        response = self.client.get("/cars/?name=i")

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["car_list"],
            Manufacturer.objects.filter(name__icontains="i")
        )
