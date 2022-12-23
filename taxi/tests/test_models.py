import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car, Comment

temp_name = "Mazda"
temp_country = "Japan"
temp_first_name = "Vlad"
temp_last_name = "Magdenko"
temp_model = "RX8"
temp_username = "blin4ik"
temp_avatar = None


class ModelsTests(TestCase):
    @staticmethod
    def create_manufacturer():
        return Manufacturer.objects.create(
            name=temp_name,
            country=temp_country
        )

    def test_manufacturer_str(self):
        manufacturer_ = self.create_manufacturer()
        self.assertEqual(str(manufacturer_),
                         f"{manufacturer_.name} {manufacturer_.country}"
                         )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username=temp_username,
            first_name=temp_first_name,
            last_name=temp_last_name
        )
        self.assertEqual(str(driver), f"{driver.username} "
                                      f"({driver.first_name} "
                                      f"{driver.last_name})")

    def test_car_str(self):
        car_ = Car.objects.create(model=temp_model,
                                  manufacturer=self.create_manufacturer()
                                  )
        self.assertEqual(str(car_), f"{car_.model}")

    def test_comment_str(self):
        user = get_user_model().objects.create(
            username=temp_username,
            first_name=temp_first_name,
            last_name=temp_last_name
        )
        car = Car.objects.create(model=temp_model,
                                 manufacturer=self.create_manufacturer()
                                 )
        comment_ = Comment.objects.create(
            user=user,
            car=car,
            content="Test comment!",
            date=datetime.date
        )
        self.assertEqual(str(comment_), f"Comment: {comment_.content} "
                                        f"from {comment_.user.username} "
                                        f"at {comment_.date}")

    def test_create_driver_with_license_number(self):
        username = temp_username
        password = "test12345"
        license_number = "TES12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, temp_username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
