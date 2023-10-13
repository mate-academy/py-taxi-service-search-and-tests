from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ManufacturerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name="Big", country="UA"
        )
        cls.manufacturer = Manufacturer.objects.get(pk=1)
        cls.field_name = cls.manufacturer._meta.get_field("name")
        cls.field_country = cls.manufacturer._meta.get_field("country")

    def test_labels(self):
        self.assertEqual(self.field_name.verbose_name, "name")
        self.assertEqual(self.field_country.verbose_name, "country")

    def test_fields_max_lenght(self) -> None:
        self.assertEqual(self.field_name.max_length, 255)
        self.assertEqual(self.field_country.max_length, 255)

    def test_str_representation(self) -> None:
        correct_str_repr = (
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )
        self.assertEqual(str(self.manufacturer), correct_str_repr)


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.driver_to_test = Driver.objects.create_user(
            username="test.username",
            license_number="ABC12345",
            password="test_password",
        )
        cls.license_num_field = cls.driver_to_test._meta.get_field(
            "license_number"
        )

    def test_lables(self) -> None:
        self.assertEqual(self.license_num_field.verbose_name, "license number")

    def test_absolute_url(self) -> None:
        self.assertEqual(self.driver_to_test.get_absolute_url(), "/drivers/1/")


class CarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.car_to_test = Car.objects.create(
            model="Test_model",
            manufacturer=Manufacturer.objects.create(name="Big", country="UA"),
        )
        cls.field_model = cls.car_to_test._meta.get_field("model")
        cls.field_manufacturer = cls.car_to_test._meta.get_field(
            "manufacturer"
        )

    def test_related_name(self) -> None:
        related_name = Car._meta.get_field("drivers").remote_field.related_name
        self.assertEqual(related_name, "cars")

    def test_labels(self) -> None:
        self.assertEqual(self.field_model.verbose_name, "model")
        self.assertEqual(self.field_manufacturer.verbose_name, "manufacturer")

    def test_str_representation(self) -> None:
        correct_str_repr = f"{self.car_to_test.model}"
        self.assertEqual(str(self.car_to_test), correct_str_repr)

    def test_model_max_length(self) -> None:
        self.assertEqual(self.field_model.max_length, 255)
