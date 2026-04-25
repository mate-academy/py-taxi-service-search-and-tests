from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Car, Manufacturer


User = get_user_model()


class CatModelTest(TestCase):

    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Deutschland",
        )

        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@mail.com",
            password="abc1234",
            first_name="Test",
            last_name="User",
            license_number="ABC12345"
        )

        self.car = Car.objects.create(
            model="X3",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.user)
        self.car.save()

    def test_str_representation(self):
        car = Car.objects.get(pk=1)

        self.assertEqual(
            str(car),
            car.model
        )


class ManufacturerModelTest(TestCase):

    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Deutschland",
        )

    def test_str_representation(self):
        manufacturer = Manufacturer.objects.get(pk=1)

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}")


class UserModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@mail.com",
            password="abc1234",
            first_name="Test",
            last_name="User",
            license_number="ABC12345"
        )

    def test_str_representation(self):
        user = User.objects.get(pk=1)

        self.assertEqual(
            str(user),
            f"{user.username} ({user.first_name} {user.last_name})")

    def test_license_number(self):
        user = User.objects.get(pk=1)

        self.assertEqual(user.license_number, "ABC12345")

    def test_password_hashing_functionality(self):
        user = User.objects.get(pk=1)

        self.assertNotEqual(user.password, "abc1234")
        self.assertTrue(user.check_password("abc1234"))

    def test_get_absolute_url(self):
        user = User.objects.get(pk=1)
        self.assertEqual(user.get_absolute_url(), "/drivers/1/")
