from multiprocessing.connection import Client

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import ManufacturerNameSearchForm, DriverCreationForm
from taxi.models import Manufacturer, Car, Driver


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        url = reverse("taxi:manufacturer-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self) -> None:
        url = reverse("taxi:manufacturer-list")
        Manufacturer.objects.create(name="Test", country="TRR")
        Manufacturer.objects.create(name="Test2", country="CRR")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)


class PublicCarTests(TestCase):
    def test_login_required(self):
        url = reverse("taxi:car-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self) -> None:
        url = reverse("taxi:car-list")
        man1 = Manufacturer.objects.create(name="Test", country="TRR")
        man2 = Manufacturer.objects.create(name="Test2", country="CRR")
        Car.objects.create(model="test", manufacturer=man1)
        Car.objects.create(model="test2", manufacturer=man2)
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)


class FormTests(TestCase):
    def test_driver_creation(self):
        form_data = {
            "username": "testuser",
            "password1": "CompL3xP@ssw0rd2024",
            "password2": "CompL3xP@ssw0rd2024",
            "first_name": "Test",
            "last_name": "Test2",
            "license_number": "AZX12354"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=form.errors)
        self.assertEqual(form.cleaned_data, form_data)


class DriverSearchTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

        self.driver1 = Driver.objects.create_user(
            username="driver_one", password="testpass123", license_number="AAA123456"
        )
        self.driver2 = Driver.objects.create_user(
            username="driver_two", password="testpass123", license_number="BBB123456"
        )

    def test_search_driver_by_partial_username(self):
        response = self.client.get(reverse("taxi:driver-list") + "?username=one")
        self.assertContains(response, "driver_one")
        self.assertNotContains(response, "driver_two")

    def test_search_driver_no_results(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=unknown"
        )
        self.assertNotContains(response, "driver_one")
        self.assertNotContains(response, "driver_two")

    def test_search_driver_empty_query_returns_all(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertContains(response, "driver_one")
        self.assertContains(response, "driver_two")


class ManufacturerSearchTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="<PASSWORD>",)
        self.client.force_login(self.user)

        self.man1 = Manufacturer.objects.create(name="Test1", country="TRR")
        self.man2 = Manufacturer.objects.create(name="Test2", country="CRR")

    def test_search_manufacturer_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=Test1"
        )
        self.assertContains(response, "Test1")
        self.assertNotContains(response, "Test2")


class CarSearchTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="<PASSWORD>",)
        self.client.force_login(self.user)
        man1 = Manufacturer.objects.create(name="Test3", country="TRR")
        man2 = Manufacturer.objects.create(name="Test4", country="CRR")
        self.car1 = Car.objects.create(model="Test1", manufacturer=man1)
        self.car2 = Car.objects.create(model="Test2", manufacturer=man2)

    def test_search_car_by_name(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=Test1")
        self.assertContains(response, "Test1")
        self.assertNotContains(response, "Test2")
