from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerModelTest(TestCase):
    def setUp(self):
        Manufacturer.objects.create(
            name="Test name",
            country="Test country"
        )

    def test_name_unique_and_length(self):
        manufacturer = Manufacturer.objects.get(id=1)
        max_length = manufacturer._meta.get_field("name").max_length
        is_unique = manufacturer._meta.get_field("name").unique

        self.assertEqual(max_length, 255)
        self.assertTrue(is_unique)

    def test_country_length(self):
        manufacturer = Manufacturer.objects.get(id=1)
        max_length = manufacturer._meta.get_field("country").max_length

        self.assertEqual(max_length, 255)

    def test_format_str(self):
        manufacturer = Manufacturer.objects.get(id=1)

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )


class DriverModelTest(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(
            username="test",
            password="testpassword",
            license_number="DNA23794"
        )

    def test_license_number_unique_and_length(self):
        driver = get_user_model().objects.get(id=1)
        max_length = driver._meta.get_field("license_number").max_length
        is_unique = driver._meta.get_field("license_number").unique

        self.assertEqual(max_length, 255)
        self.assertTrue(is_unique)

    def test_meta_verbose_name(self):
        driver = get_user_model().objects.get(id=1)
        verbose_name = driver._meta.verbose_name
        verbose_name_plural = driver._meta.verbose_name_plural

        self.assertEqual(verbose_name, "driver")
        self.assertEqual(verbose_name_plural, "drivers")

    def test_format_str(self):
        driver = get_user_model().objects.get(id=1)

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_get_absolute_path(self):
        _id = 1
        driver = get_user_model().objects.get(id=_id)

        self.assertEqual(driver.get_absolute_url(), f"/drivers/{_id}/")


class CarModelTest(TestCase):
    def setUp(self):
        manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country"
        )

        Car.objects.create(
            model="BMW",
            manufacturer=manufacturer
        )

    def test_model_length(self):
        car = Car.objects.get(id=1)
        max_length = car._meta.get_field("model").max_length

        self.assertEqual(max_length, 255)

    def test_format_str(self):
        car = Car.objects.get(id=1)

        self.assertEqual(
            str(car),
            car.model
        )
