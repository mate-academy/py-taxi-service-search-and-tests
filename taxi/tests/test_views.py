from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class PublicHomePageTest(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse("taxi:index"))

        self.assertNotEqual(res.status_code, 200)


class PrivateHomePageTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="userPwd12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_home_page(self):
        resp = self.client.get(reverse("taxi:index"))

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "taxi/index.html")


class ManufacturerListViewTests(TestCase):
    def setUp(self):

        driver = get_user_model().objects.create_user(
            username="test",
            password="userPwd12345"
        )
        self.client.force_login(driver)

    def test_manufacturer_list_view(self):
        resp = self.client.get(reverse("taxi:manufacturer-list"))
        manufacturer_list = Manufacturer.objects.all()
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "taxi/manufacturer_list.html")
        self.assertEqual(
            list(resp.context["manufacturer_list"]),
            list(manufacturer_list))


class CarListViewTests(TestCase):
    def setUp(self):
        manufacturer = Manufacturer.objects.create(
            name=f"test_manufacturer",
            country=f"test_manufacturer_country",
        )
        Car.objects.create(
            model=f"test_model",
            manufacturer=manufacturer
        )
        driver = get_user_model().objects.create_user(
            username="test",
            password="userPwd12345"
        )

        self.client.force_login(driver)

    def test_car_list_view(self):
        resp = self.client.get(reverse("taxi:car-list"))
        cars = Car.objects.all()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            list(resp.context["car_list"]),
            list(cars))


class DriverListViewTests(TestCase):
    def setUp(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="userPwd12345"
        )
        self.client.force_login(driver)

    def test_driver_list_view(self):
        resp = self.client.get(reverse("taxi:driver-list"))
        driver_list = Driver.objects.all()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            list(resp.context["driver_list"]),
            list(driver_list))


class PrivateDriverTests(TestCase):
    def setUp(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="userPwd12345"
        )
        self.client.force_login(driver)

    def test_create_driver(self):
        form_data = {
            "username": "test_user",
            "password1": "pwdUser12345",
            "password2": "pwdUser12345",
            "first_name": "first_name_test",
            "last_name": "last_name_test",
            "license_number": "ABC12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
