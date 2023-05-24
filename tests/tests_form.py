from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from taxi.forms import DriverCreationForm
from taxi.models import Car, Manufacturer


class TestDriverCreationForm(TestCase):
    def test_driver_form_intro(self):
        form_data = {
            "username": "test1",
            "license_number": "AAA12345",
            "first_name": "test",
            "last_name": "test",
            "password1": "admin-123",
            "password2": "admin-123",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEquals(form_data, form.cleaned_data)


class TestDriverSearchForm(TestCase):
    def setUp(self) -> None:
        self.user_1 = get_user_model().objects.create_user(
            username="test1", password="admin-123", license_number="AAA12345"
        )
        self.user_2 = get_user_model().objects.create_user(
            username="test2", password="admin-123", license_number="AAA12346"
        )
        self.client.force_login(self.user_1)

    def test_driver_search_form(self):
        url = "http://localhost/drivers/?username=1"
        response = self.client.get(url)
        self.assertContains(response, self.user_1.username)
        self.assertNotContains(response, self.user_2.username)


class TestCarSearchForm(TestCase):
    def setUp(self) -> None:

        manufacturer = Manufacturer.objects.create(name="test", country="test")
        self.car_1 = Car.objects.create(
            model="test1",
            manufacturer=manufacturer)
        self.car_2 = Car.objects.create(
            model="test2",
            manufacturer=manufacturer)
        self.client.force_login(
            get_user_model().objects.create_user(
                username="test",
                password="admin-123",
                license_number="AAA12345"
            )
        )

    def test_car_search_form(self):
        url = "http://localhost/cars/?model=1"
        response = self.client.get(url)
        self.assertContains(response, self.car_1.model)
        self.assertNotContains(response, self.car_2.model)


class TestManufacturerSearchForm(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.manufacturer_1 = Manufacturer.objects.create(
            name="test1", country="test"
        )
        self.manufacturer_2 = Manufacturer.objects.create(
            name="test2", country="test"
        )
        self.client.force_login(
            get_user_model().objects.create_user(
                username="test",
                password="admin-123",
                license_number="AAA12345"
            )
        )

    def test_manufacturer_search_form(self):

        url = "http://localhost/manufacturers/?name=1"
        response = self.client.get(url)
        self.assertContains(response, self.manufacturer_1.name)
        self.assertNotContains(response, self.manufacturer_2.name)
