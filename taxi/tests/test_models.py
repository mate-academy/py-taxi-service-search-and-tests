from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Tavria",
            country="Ukraine"
        )
        self.assertEquals(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        manufacturer_ = Manufacturer.objects.create(
            name="Tavria",
            country="Ukraine"
        )
        car = Car.objects.create(
            model="Nova",
            manufacturer=manufacturer_
        )
        self.assertEquals(
            str(car),
            f"{car.model}"
        )

    def test_create_driver_with_licence(self):
        username_ = "usna",
        password_ = "test@123"
        first_name_ = "fn",
        last_name_ = "ln",
        license_number_ = "AAA12345"
        driver = get_user_model().objects.create_user(
            username=username_,
            password=password_,
            first_name=first_name_,
            last_name=last_name_,
            license_number=license_number_
        )
        self.assertEquals(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )
        self.assertTrue(driver.check_password(password_))
        self.assertEquals(driver.license_number, license_number_)
