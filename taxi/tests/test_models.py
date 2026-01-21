from django.contrib.auth import get_user_model
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.test import TestCase

from taxi.forms import validate_license_number
from taxi.models import Manufacturer, Driver, Car


# Create your tests here.
class ModelTests(TestCase):
    def setUp(self) -> None:
        self.first_name = "bob"
        self.last_name = "halov"
        self.username = "bob.halov"
        self.password = "test123!"
        self.license_number = "ADM56984"
        self.driver = get_user_model().objects.create_user(
            id=1,
            first_name=self.first_name,
            last_name=self.last_name,
            username=self.username,
            password=self.password,
            license_number=self.license_number,
        )
        "set up for manufacturer"
        self.manufacturer = Manufacturer.objects.create(
            name="Manufacturer", country="United States"
        )

    def test_manufacturer_name_and_country_fields(self):
        manufacturer = Manufacturer.objects.get(name="Manufacturer")
        name_label = manufacturer._meta.get_field("name").verbose_name
        country_label = manufacturer._meta.get_field("country").verbose_name
        self.assertEqual(name_label, "name")
        self.assertEqual(country_label, "country")

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(name="Manufacturer")
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_model(self):
        self.assertEqual(self.driver.username, self.username)
        self.assertEqual(self.driver.license_number, self.license_number)
        self.assertTrue(self.driver.check_password(self.password))

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver), f"{self.username} "
                              f"({self.first_name} {self.last_name})"
        )

    def test_driver_absolute_url(self):
        self.assertEqual(self.driver.get_absolute_url(), "/drivers/1/")

    def test_car_model_fields(self):
        model = "Dodge"
        car_create = Car.objects.create(
            model=model,
            manufacturer=self.manufacturer,
        )
        car_create.drivers.add(self.driver)

        car = Car.objects.get(id=car_create.id)
        self.assertEqual(car.model, model)
        manufacturer_field = Car._meta.get_field("manufacturer")
        self.assertTrue(isinstance(manufacturer_field, ForeignKey))

        drivers_field = Car._meta.get_field("drivers")
        self.assertTrue(isinstance(drivers_field, ManyToManyField))
