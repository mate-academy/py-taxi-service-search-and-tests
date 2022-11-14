from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer, Car


class FormsTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Test", country="Testostan"
        )
        self.driver = get_user_model().objects.create_superuser(
            username="drivertest",
            first_name="Test",
            last_name="Testovich",
            license_number="GFT12456",
            password="stronkPass124_",
        )
        self.client.force_login(self.driver)

    def test_driver_creation(self):
        form_data = {
            "username": "test_user",
            "password1": "test_pass123",
            "password2": "test_pass123",
            "first_name": "Test first_name",
            "last_name": "Test last_name",
            "license_number": "TST12243",
        }
        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_update(self):
        data = {"license_number": "QWE12345"}
        form = DriverLicenseUpdateForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, data)

    def test_car_creation(self):
        response = self.client.post(
            reverse("taxi:car-create"),
            data={
                "model": "Test model",
                "manufacturer": self.manufacturer.id,
                "drivers": self.driver.id,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Car.objects.first().model, "Test model")

    def test_delete_car(self):
        car = Car.objects.create(
            model="Test model",
            manufacturer=self.manufacturer,
        )
        response = self.client.post(
            reverse("taxi:car-delete", kwargs={"pk": car.id})
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Car.objects.filter(id=car.id).exists())
