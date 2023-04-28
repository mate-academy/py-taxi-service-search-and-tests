from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverCreationForm
from .test_views import DRIVERS_URL, CARS_URL, MANUFACTURERS_URL
from taxi.models import Manufacturer, Car


class FormsTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin12345"
        )
        self.client.force_login(self.user)

    def test_driver_creation_form_with_license_and_name_is_valid(self):
        form_data = {
            "username": "Test.1",
            "password1": "Test12345",
            "password2": "Test12345",
            "first_name": "Name",
            "last_name": "Surname",
            "license_number": "TES12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_search_form(self):
        get_user_model().objects.create_user(
            username="test",
            password="test12345",
            license_number="TES12345"
        )
        get_user_model().objects.create_user(
            username="test2",
            password="test12345",
            license_number="TES12456"
        )
        search = {"username": "test"}
        response = self.client.get(DRIVERS_URL, search)
        result = get_user_model().objects.filter(username__icontains="test")
        self.assertEqual(
            list(response.context["driver_list"]),
            list(result)
        )

    def test_car_search_form(self):
        manufacturer = Manufacturer.objects.create(
            name="Manufacturer", country="Country"
        )
        Car.objects.create(model="Test1", manufacturer=manufacturer)
        Car.objects.create(model="Test2", manufacturer=manufacturer)
        search = {"model": "test"}
        response = self.client.get(CARS_URL, search)
        result = Car.objects.filter(model__icontains="test")
        self.assertEqual(
            list(response.context["car_list"]),
            list(result)
        )

    def test_manufacturer_search_form(self):
        Manufacturer.objects.create(name="Test1", country="Country")
        Manufacturer.objects.create(name="Test2", country="Country")
        search = {"name": "test"}
        response = self.client.get(MANUFACTURERS_URL, search)
        result = Manufacturer.objects.filter(name__icontains="test")
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(result)
        )
