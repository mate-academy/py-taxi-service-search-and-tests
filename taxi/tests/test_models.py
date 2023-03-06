from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def setUp(self):
        manufacturer_ = Manufacturer.objects.create(
            name="name_",
            country="country_"
        )
        get_user_model().objects.create_user(
            username="test",
            password="test12345",
            license_number="TES12345",
            first_name="Test first",
            last_name="Test last"
        )
        Car.objects.create(
            model="test",
            manufacturer=manufacturer_
        )

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEqual(str(manufacturer), "name_ country_")

    def test_car_str(self):
        model_ = Car.objects.get(id=1)
        self.assertEqual(str(model_), model_.model)

    def test_car_model_max_length(self):
        car_ = Car.objects.get(id=1)
        max_length = car_._meta.get_field("model").max_length
        self.assertEqual(max_length, 67)

    def test_driver_str(self):
        user_ = get_user_model().objects.get(
            username="test"
        )

        self.assertEqual(
            str(user_),
            f"{user_.username} ({user_.first_name} {user_.last_name})"
        )

    def test_driver_get_absolute_url(self):
        driver_ = get_user_model().objects.get(id=1)
        self.assertEqual(
            driver_.get_absolute_url(),
            "/drivers/1/"
        )

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "test12345"
        license_number = "TES12345"
        user_ = get_user_model().objects.get(
            username=username
        )

        self.assertEqual(user_.username, username)
        self.assertTrue(user_.check_password(password))
        self.assertEqual(user_.license_number, license_number)
