from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Opel",
            country="Germany"
        )
        self.assertEquals(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="michael",
            first_name="Michael",
            last_name="Schumacher",
            password="test1234",
        )

        self.assertEquals(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_with_license_number(self):
        username = "michael"
        first_name = "Michael"
        last_name = "Schumacher"
        password = "test1234"
        license_number = "LICENSE"
        driver = get_user_model().objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            license_number=license_number,
        )

        self.assertEquals(driver.username, username)
        self.assertEquals(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Opel",
            country="Germany"
        )
        car = Car.objects.create(model="audi", manufacturer=manufacturer)

        self.assertEquals(str(car), car.model)

    def test_manufacturer_ordering(self):
        manufacturer1 = Manufacturer.objects.create(
            name="opel",
            country="country1"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="alfa romeo", country="country2"
        )
        manufacturer3 = Manufacturer.objects.create(
            name="nissan",
            country="country3"
        )
        manufacturer4 = Manufacturer.objects.create(
            name="citroen",
            country="country4"
        )

        all_manufacturers = list(Manufacturer.objects.all())

        self.assertEquals(
            all_manufacturers,
            [manufacturer2, manufacturer4, manufacturer3, manufacturer1],
        )

    def test_driver_absolute_url(self):
        driver = get_user_model().objects.create(
            username="michael",
            first_name="Michael",
            last_name="Schumacher",
            password="test1234",
        )
        self.assertEquals(driver.get_absolute_url(), f"/drivers/{driver.id}/")

    def test_driver_license_number_max_length(self):
        driver = get_user_model().objects.create(
            username="michael",
            first_name="Michael",
            last_name="Schumacher",
            password="test1234",
        )
        self.assertEquals(
            driver._meta.get_field("license_number").max_length, 255
        )

    def test_car_blank_false(self):
        car = Car.objects.create(
            model="Opel",
            manufacturer=Manufacturer.objects.create(
                name="test",
                country="country1"
            ),
        )
        self.assertFalse(car._meta.get_field("model").blank)
