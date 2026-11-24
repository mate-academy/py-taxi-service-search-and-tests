from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class LoginRequiredTest(TestCase):
    def setUp(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="test name",
            country="test country"
        )
        get_user_model().objects.create_user(
            username="test_user",
            password="test123user"
        )
        Car.objects.create(
            model="test model",
            manufacturer=manufacturer
        )

    def test_main_pages(self) -> None:
        urls = (
            "taxi:index",
            "taxi:manufacturer-list",
            "taxi:manufacturer-create",
            "taxi:car-list",
            "taxi:car-create",
            "taxi:driver-list",
            "taxi:driver-create",
        )
        for url in urls:
            response = self.client.get(reverse(url))
            self.assertNotEqual(response.status_code, 200)

    def test_pages_with_pk(self) -> None:
        urls = (
            "taxi:manufacturer-update",
            "taxi:manufacturer-delete",
            "taxi:car-detail",
            "taxi:car-update",
            "taxi:car-delete",
            "taxi:driver-detail",
            "taxi:driver-update",
            "taxi:driver-delete",
            "taxi:toggle-car-assign",
        )
        for url in urls:
            response = self.client.get(reverse(url, args=[1]))
            self.assertNotEqual(response.status_code, 200)


class SuccessResponseTest(TestCase):
    def setUp(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="test name",
            country="test country"
        )
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test123user"
        )
        Car.objects.create(
            model="test model",
            manufacturer=manufacturer
        )
        self.client.force_login(self.user)

    def test_main_pages(self) -> None:
        urls = (
            "taxi:index",
            "taxi:manufacturer-list",
            "taxi:manufacturer-create",
            "taxi:car-list",
            "taxi:car-create",
            "taxi:driver-list",
            "taxi:driver-create",
        )
        for url in urls:
            response = self.client.get(reverse(url))
            self.assertEqual(response.status_code, 200)

    def test_pages_with_pk(self) -> None:
        urls = (
            "taxi:manufacturer-update",
            "taxi:manufacturer-delete",
            "taxi:car-detail",
            "taxi:car-update",
            "taxi:car-delete",
            "taxi:driver-detail",
            "taxi:driver-update",
            "taxi:driver-delete",
        )
        for url in urls:
            response = self.client.get(reverse(url, args=[1]))
            self.assertEqual(response.status_code, 200)


class ManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.url_manufacturer_list = reverse("taxi:manufacturer-list")
        self.user = get_user_model().objects.create_user(
            username="user",
            password="test123user"
        )
        self.client.force_login(self.user)
        self.manufacturer1 = Manufacturer.objects.create(
            name="first_name",
            country="first_country"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="second_name",
            country="second_country"
        )

    def test_manufacturer_list_view(self) -> None:
        response = self.client.get(self.url_manufacturer_list)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_get_context_data(self) -> None:
        response = self.client.get(self.url_manufacturer_list)
        self.assertIn("search_form", response.context)

    def test_get_queryset_with_params(self) -> None:
        response = self.client.get(
            self.url_manufacturer_list + f"?name={self.manufacturer1.name}"
        )
        self.assertContains(response, self.manufacturer1.name)
        self.assertNotContains(response, self.manufacturer2.name)

    def test_get_queryset_without_params(self) -> None:
        response = self.client.get(self.url_manufacturer_list)
        self.assertContains(response, self.manufacturer1.name)
        self.assertContains(response, self.manufacturer2.name)


class DriverTests(TestCase):
    def setUp(self) -> None:
        self.url_driver_list = reverse("taxi:driver-list")
        self.user1 = get_user_model().objects.create_user(
            username="first_user",
            password="test123user",
            license_number="DDD44444"
        )
        self.client.force_login(self.user1)
        self.user2 = get_user_model().objects.create_user(
            username="second_user",
            password="test123user",
            license_number="DDD55555"
        )

    def test_create_driver_with_correct_attributes(self) -> None:
        form_data = {
            "username": "new_user",
            "password1": "test123user",
            "password2": "test123user",
            "first_name": "test_first",
            "last_name": "test_last",
            "license_number": "DDD88888"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.username, form_data["username"])
        self.assertTrue(new_user.check_password(form_data["password1"]))
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_driver_list(self) -> None:
        response = self.client.get(self.url_driver_list)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )

    def test_context_data(self) -> None:
        response = self.client.get(self.url_driver_list)
        self.assertIn("search_form", response.context)

    def test_get_queryset_with_params(self) -> None:
        response = self.client.get(
            self.url_driver_list + f"?username={self.user1.username}"
        )
        self.assertContains(response, self.user1.username)
        self.assertNotContains(response, self.user2.username)

    def test_get_queryset_without_params(self) -> None:
        response = self.client.get(self.url_driver_list)
        self.assertContains(response, self.user1.username)
        self.assertContains(response, self.user2.username)


class CarTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.url_car_list = reverse("taxi:car-list")
        self.user = get_user_model().objects.create_user(
            username="user",
            password="test123user"
        )
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        self.car1 = Car.objects.create(
            model="first_model",
            manufacturer=manufacturer
        )
        self.car2 = Car.objects.create(
            model="second_model",
            manufacturer=manufacturer
        )

    def test_get_context_data(self) -> None:
        response = self.client.get(self.url_car_list)
        self.assertIn("search_form", response.context)

    def test_get_queryset_with_params(self) -> None:
        response = self.client.get(
            self.url_car_list + f"?model={self.car1.model}"
        )
        self.assertContains(response, self.car1.model)
        self.assertNotContains(response, self.car2.model)

    def test_get_queryset_without_params(self) -> None:
        response = self.client.get(self.url_car_list)
        self.assertContains(response, self.car1.model)
        self.assertContains(response, self.car2.model)
