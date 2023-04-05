from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.driver = get_user_model().objects.create_user(
            username="rickky",
            first_name="Rick",
            last_name="Sanchez",
            password="12345",
            license_number="RIS12345",
        )
        self.car = Car.objects.create(
            model="Corolla", manufacturer=self.manufacturer
        )

        self.models = [
            {"entity": self.manufacturer, "expected_data": "Toyota Japan"},
            {"entity": self.driver, "expected_data": "rickky (Rick Sanchez)"},
            {"entity": self.car, "expected_data": "Corolla"},
        ]

    def test_str_representation(self):
        for model in self.models:
            with self.subTest(model=model["entity"].__class__.__name__):
                self.assertEqual(str(model["entity"]), model["expected_data"])

    def test_get_driver_absolute_url(self):
        self.assertEqual(
            self.driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": self.driver.pk}),
        )

    def test_driver_has_license_number_field(self):
        fields_name = [field.name for field in get_user_model()._meta.fields]
        self.assertIn("license_number", fields_name)
