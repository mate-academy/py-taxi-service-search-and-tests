from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm, validate_license_number
from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class TestManufacturerSearchForm(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            license_number="TES12345"
        )
        get_user_model().objects.create_user(
            username="test2",
            license_number="TES98765"
        )
        manufacturer_1 = Manufacturer.objects.create(
            name="Test_1",
        )
        manufacturer_2 = Manufacturer.objects.create(
            name="Test_2",
        )
        Car.objects.create(
            model="Test_1",
            manufacturer=manufacturer_1
        )
        Car.objects.create(
            model="Test_2",
            manufacturer=manufacturer_2
        )
        self.client.force_login(self.user)

    def test_manufacturer_search_form(self):
        form_data = {"name": "Test_1"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_manufacturer_search_form_username_search(self):
        form_data = {"name": "Test_2"}
        res = self.client.get(MANUFACTURER_URL, data=form_data)
        self.assertContains(res, form_data["name"])
        self.assertNotContains(res, "Test_1")

    def test_license_number_validation(self):
        self.assertRaises(
            ValidationError,
            validate_license_number,
            license_number="TES123456789"
        )
        self.assertRaises(
            ValidationError,
            validate_license_number,
            license_number="tes12345"
        )
        self.assertRaises(
            ValidationError,
            validate_license_number,
            license_number="TES_qwerty"
        )
