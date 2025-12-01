from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class TestModels(TestCase):
    def test_manufacturer_str(self) -> None:
        name = "BMW"
        country = "Germany"
        obj = Manufacturer.objects.create(name=name, country=country)
        self.assertEqual(str(obj), f"{name} {country}")

    def test_driver_str(self) -> None:
        license_number = "some_text"
        username = "some"
        first_name = "Bob"
        last_name = "Bobinsky"
        obj = Driver.objects.create(
            license_number=license_number,
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        self.assertEqual(str(obj), f"{username} ({first_name} {last_name})")

    def test_driver_get_absolute_url(self) -> None:
        license_number = "some_text"
        obj = Driver.objects.create(license_number=license_number)
        self.assertEqual(obj.get_absolute_url(), "/drivers/1/")

    def test_car_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="name", country="country"
        )
        model = "some_model"
        obj = Car.objects.create(model=model, manufacturer=manufacturer)
        self.assertEqual(str(obj), f"{model}")
