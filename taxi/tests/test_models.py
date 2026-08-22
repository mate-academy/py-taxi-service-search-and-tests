from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ManufacturerModelTest(TestCase):
    def test_str_return(self):
        manufacturer = Manufacturer.objects.create(name="Audi",
                                                   country="Germany")
        self.assertEqual(str(manufacturer),
                         "Audi Germany")

    def test_manufacturers_ordered_by_name(self):
        Manufacturer.objects.create(name="Skoda",
                                    country="Germany")
        Manufacturer.objects.create(name="BMW",
                                    country="Germany")
        Manufacturer.objects.create(name="Audi",
                                    country="Germany")

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(list(manufacturers.values_list("name", flat=True)),
                         ["Audi", "BMW", "Skoda"]
                         )


class DriverModelTest(TestCase):
    def test_str_return(self):
        self.user = self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            first_name="Pawel",
            last_name="jumper",
            license_number="ABC23456",
        )

        self.assertEqual(str(self.user), "test (Pawel jumper)")

    def test_get_absolute_url(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            first_name="Pawel",
            last_name="jumper",
            license_number="ABC23456")

        self.assertEqual(self.user.get_absolute_url(),
                         reverse("taxi:driver-detail",
                                 kwargs={"pk": self.user.pk}))

    def test_nonunique_license_number(self):
        get_user_model().objects.create_user(
            username="test",
            password="test123",
            first_name="Pawel",
            last_name="jumper",
            license_number="ABC23456",
        )

        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(
                username="test321",
                password="test123",
                first_name="adrian",
                last_name="razmus",
                license_number="ABC23456",
            )


class CarModelTest(TestCase):
    def test_str_return(self):
        manufacturer = Manufacturer.objects.create(name="BMW",
                                                   country="Germany")
        car = Car.objects.create(model="M5",
                                 manufacturer=manufacturer)

        self.assertEqual(str(car), "M5")
