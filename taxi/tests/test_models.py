from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car


class ManufacturerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(
            name="test",
            country="test_country",
        )

    def test_manufacturer_name_field_label(self):
        manufacturer = Manufacturer.objects.get(id=1)
        field_label = manufacturer._meta.get_field("name").verbose_name
        self.assertEquals(field_label, "name")

    def test_manufacturer_name_field_max_length(self):
        manufacturer = Manufacturer.objects.get(id=1)
        name_max_length = manufacturer._meta.get_field("name").max_length
        self.assertEqual(
            name_max_length,
            255,
            msg=f"max length for 'name' field must be 255"
                f" not {name_max_length}"
        )

    def test_manufacturer_name_field_unique(self):
        manufacturer = Manufacturer.objects.get(id=1)
        is_unique = manufacturer._meta.get_field("name").unique
        self.assertTrue(
            is_unique,
            msg="manufacturer name must be unique"
        )

    def test_manufacturer_country_field_label(self):
        manufacturer = Manufacturer.objects.get(id=1)
        field_label = manufacturer._meta.get_field("country").verbose_name
        self.assertEquals(field_label, "country")

    def test_manufacturer_country_field_max_length(self):
        manufacturer = Manufacturer.objects.get(id=1)
        country_max_length = manufacturer._meta.get_field("country").max_length
        self.assertEqual(
            country_max_length,
            255,
            msg=f"max length for 'country' field must be 255"
                f" not {country_max_length}"
        )

    def test_ordering(self):
        ordering_by = Manufacturer._meta.ordering[0]
        self.assertEqual(
            ordering_by,
            "name",
            msg="manufacturer object must be ordered by 'name' field"
        )

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEqual(str(manufacturer), "test test_country")


class DriverTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            username="test",
            first_name="first_name",
            last_name="last_name",
            password="test",
            license_number="ABC12345"
        )

    def test_driver_license_number_field_label(self):
        driver = get_user_model().objects.get(id=1)
        label = driver._meta.get_field("license_number").verbose_name
        self.assertEquals(label, "license number")

    def test_driver_license_number_field_max_length(self):
        driver = get_user_model().objects.get(id=1)
        max_length = driver._meta.get_field("license_number").max_length
        self.assertEqual(
            max_length,
            255,
            msg=f"license_number max_length must be 255, not {max_length}."
        )

    def test_driver_license_number_field_unique(self):
        driver = get_user_model().objects.get(id=1)
        is_unique = driver._meta.get_field("license_number").unique
        self.assertTrue(
            is_unique,
            msg="license_number must be unique"
        )

    def test_driver_model_verbose_name(self):
        verbose_name = get_user_model()._meta.verbose_name
        self.assertEquals(
            verbose_name,
            "driver",
        )

    def test_driver_model_verbose_name_plural(self):
        verbose_name_plural = get_user_model()._meta.verbose_name_plural
        self.assertEquals(
            verbose_name_plural,
            "drivers",
        )

    def test_driver_model_str(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(
            str(driver),
            "test (first_name last_name)"
        )

    def test_get_absolute_url(self):
        user = get_user_model().objects.get(id=1)
        url = user.get_absolute_url()
        self.assertEqual(
            url,
            "/drivers/1/",
        )


class CarTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="test",
        )
        Car.objects.create(
            manufacturer=manufacturer,
            model="test_model",
        )

    def test_car_model_field_label(self):
        car = Car.objects.get(id=1)
        model_field_label = car._meta.get_field("model").verbose_name
        self.assertEquals(model_field_label, "model")

    def test_car_model_field_max_length(self):
        car = Car.objects.get(id=1)
        model_field_max_length = car._meta.get_field("model").max_length
        self.assertEqual(
            model_field_max_length,
            255,
            msg=f"max length for 'model' field must be 255"
                f" not {model_field_max_length}"
        )

    def test_car_manufacturer_field_label(self):
        car = Car.objects.get(id=1)
        manufacturer_field_label = car._meta.get_field(
            "manufacturer"
        ).verbose_name
        self.assertEquals(manufacturer_field_label, "manufacturer")

    def test_car_manufacturer_field_on_delete(self):
        Manufacturer.objects.get(name="test").delete()
        response = Car.objects.filter(model="test_model").exists()
        self.assertFalse(
            response,
            msg="when manufacturer deleted"
                " all the cars of this manufacturer must be deleted"
        )

    def test_car_drivers_field_label(self):
        car = Car.objects.get(id=1)
        driver_field_label = car._meta.get_field("drivers").verbose_name
        self.assertEquals(driver_field_label, "drivers")

    def test_car_drivers_field_related_name(self):
        car = Car.objects.get(id=1)
        driver_field_related_name = (
            car._meta.get_field("drivers").remote_field.related_name
        )
        self.assertEquals(driver_field_related_name, "cars")

    def test_car_model_str(self):
        car = Car.objects.get(id=1)
        self.assertEqual(
            str(car),
            "test_model",
            msg="__str__ method must return the 'model' of the car"
        )
