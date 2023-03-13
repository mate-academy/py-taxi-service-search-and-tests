from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Manufacturer, Car


class TestModels(TestCase):
    def test_manufacturer_str(self):
        form_ = Manufacturer.objects.create(name="Test", country="Country")

        self.assertEqual(str(form_), "Test Country")

    def test_driver_str_and_license_number(self):
        user = get_user_model().objects.create_user(
            username="name",
            password="12345",
            first_name="Test1",
            last_name="Test2",
            license_number="AAA12345"
        )

        self.assertEqual(str(user), "name (Test1 Test2)")
        self.assertEqual(user.license_number, "AAA12345")

    def test_car_str(self):
        man = Manufacturer.objects.create(name="name")
        car = Car.objects.create(model="Model", manufacturer=man)

        self.assertEqual(str(car), "Model")
