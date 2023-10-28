from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ManufacturerModelTest(TestCase):

    def test_string_representation(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        expected_str = f"{manufacturer.name} {manufacturer.country}"
        self.assertEqual(str(manufacturer), expected_str)

    def test_model_has_correct_ordering_parameter(self) -> None:
        expected_ordering_parameter = ["name"]
        self.assertEqual(
            Manufacturer._meta.ordering,
            expected_ordering_parameter
        )

    def test_model_has_necessary_fields(self) -> None:
        necessary_fields = ["name", "country"]

        model_field_manes = [
            model_field.name
            for model_field in Manufacturer._meta.get_fields()
        ]

        for field in necessary_fields:
            self.assertIn(field, model_field_manes)


class DriverModelTest(TestCase):

    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test.driver",
            first_name="test_first_name",
            last_name="test_last_name",
            password="password"
        )

    def test_string_representation(self) -> None:
        expected_str = (f"{self.driver.username} "
                        f"({self.driver.first_name} "
                        f"{self.driver.last_name})")
        self.assertEqual(str(self.driver), expected_str)

    def test_get_absolute_url_method(self) -> None:
        expected_url = reverse("taxi:driver-detail",
                               kwargs={"pk": self.driver.pk})
        self.assertEqual(self.driver.get_absolute_url(), expected_url)

    def test_model_has_correct_verbose_names(self) -> None:
        driver_model = get_user_model()
        self.assertEqual(driver_model._meta.verbose_name, "driver")
        self.assertEqual(driver_model._meta.verbose_name_plural, "drivers")

    def test_model_has_necessary_fields(self) -> None:
        necessary_fields = ["username",
                            "first_name",
                            "last_name",
                            "password",
                            "license_number"]

        model_field_manes = [
            model_field.name
            for model_field in get_user_model()._meta.get_fields()
        ]

        for field in necessary_fields:
            self.assertIn(field, model_field_manes)


class CarModelTest(TestCase):

    def test_string_representation(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)

    def test_model_has_necessary_fields(self) -> None:
        necessary_fields = ["model", "manufacturer", "drivers"]

        model_field_manes = [model_field.name
                             for model_field in Car._meta.get_fields()]

        for field in necessary_fields:
            self.assertIn(field, model_field_manes)
