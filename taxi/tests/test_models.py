from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car, Driver


class ManufacturerModelTests(TestCase):
    def setUp(self):
        manufacturer_list = {
            ("Suzuki", "Japan"),
            ("Kia", "South Korea"),
            ("Audi", "Germany")
        }
        for manufacturer in manufacturer_list:
            name, country = manufacturer
            Manufacturer.objects.create(
                name=name,
                country=country
            )

        self.manufacturer = Manufacturer.objects.get(name="Suzuki")

    def test_name_and_country_labels_in_manufacturer_model(self):
        name_label = self.manufacturer._meta.get_field("name").verbose_name
        country_label = self.manufacturer._meta.get_field(
            "country"
        ).verbose_name
        self.assertEqual(name_label, "name")
        self.assertEqual(country_label, "country")

    def test_name_and_country_fields_max_length_in_manufacturer_model(self):
        name_max_length = self.manufacturer._meta.get_field(
            "name"
        ).max_length
        country_max_length = self.manufacturer._meta.get_field(
            "country"
        ).max_length
        self.assertEqual(name_max_length, 255)
        self.assertEqual(country_max_length, 255)

    def test_str_in_manufacturer_model(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_ordering_in_manufacturer_model(self):
        self.assertEqual(
            [man.name for man in Manufacturer.objects.all()],
            ["Audi", "Kia", "Suzuki"]
        )


class DriverModelTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test-name",
            password="test12345",
            first_name="Firstname",
            last_name="Lastname",
            license_number="XXX12345"
        )

    def test_license_number_label_in_driver_model(self):
        license_number_label = self.driver._meta.get_field(
            "license_number"
        ).verbose_name
        self.assertEqual(license_number_label, "license number")

    def test_license_number_field_max_length_in_driver_model(self):
        license_number_max_length = self.driver._meta.get_field(
            "license_number"
        ).max_length
        self.assertEqual(license_number_max_length, 255)

    def test_verbose_names_labels_in_driver_model(self):
        self.assertEqual(self.driver._meta.verbose_name, "driver")
        self.assertEqual(self.driver._meta.verbose_name_plural, "drivers")

    def test_str_in_driver_model(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username}"
            f" ({self.driver.first_name} {self.driver.last_name})"
        )

    def test_license_number_field_in_driver_model(self):
        self.assertEqual(self.driver.license_number, "XXX12345")

    def test_get_absolute_url_in_driver_model(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")


class CarModelTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )

        self.driver = get_user_model().objects.create_user(
            username="test-name",
            password="test12345",
            first_name="Firstname",
            last_name="Lastname",
            license_number="XXX12345"
        )

        self.car = Car.objects.create(
            model="test-model",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)

    def test_model_manufacturer_and_drivers_labels_in_car_model(self):
        model_label = self.car._meta.get_field("model").verbose_name
        manufacturer_label = self.car._meta.get_field(
            "manufacturer"
        ).verbose_name
        drivers_label = self.car._meta.get_field(
            "drivers"
        ).verbose_name
        self.assertEqual(model_label, "model")
        self.assertEqual(manufacturer_label, "manufacturer")
        self.assertEqual(drivers_label, "drivers")

    def test_model_field_max_length_in_car_model(self):
        model_max_length = self.car._meta.get_field(
            "model"
        ).max_length
        self.assertEqual(model_max_length, 255)

    def test_car_str(self):
        self.assertEqual(str(self.car), self.car.model)
