from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from taxi.models import Car, Manufacturer


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test")
        self.assertEqual(
            str(manufacturer),
            manufacturer.name + " " + manufacturer.country)

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            password="test123",
            first_name="test_first_name",
            last_name="test_last_name",
            license_number="AAA12345",
        )
        self.assertEqual(
            str(driver), f"{driver.username}"
            f" ({driver.first_name} "
            f"{driver.last_name})")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test")
        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer)
        self.assertEqual(str(car), "test")

    def test_car_with_drivers_str(self):
        manufacturer = Manufacturer.objects.create(
            name="TestBrand",
            country="Germany")
        car = Car.objects.create(model="ModelX", manufacturer=manufacturer)
        driver = get_user_model().objects.create(
            username="testdriver",
            password="test123",
            first_name="John",
            last_name="Doe",
            license_number="DEF456",
        )
        car.drivers.add(driver)
        self.assertIn(driver, car.drivers.all())

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create(
            username="testuser",
            password="test123",
            first_name="Test",
            last_name="User",
            license_number="ABC12345",
        )
        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": driver.pk}))

    def test_driver_license_number_unique(self):
        get_user_model().objects.create(
            username="testuser1",
            password="test123",
            first_name="Test",
            last_name="User",
            license_number="ABC12345",
        )
        with self.assertRaises(IntegrityError):
            get_user_model().objects.create(
                username="testuser2",
                password="test123",
                first_name="Test2",
                last_name="User2",
                license_number="ABC12345",
            )

    def test_manufacturer_ordering(self):
        m1 = Manufacturer.objects.create(name="B Company", country="USA")
        m2 = Manufacturer.objects.create(name="A Company", country="Germany")
        self.assertEqual(list(Manufacturer.objects.all()), [m2, m1])

    def test_car_drivers_relationship(self):
        manufacturer = Manufacturer.objects.create(
            name="TestBrand",
            country="Japan")
        car = Car.objects.create(
            model="TestModel",
            manufacturer=manufacturer)

        driver1 = get_user_model().objects.create(
            username="driver1",
            password="test123",
            first_name="Driver",
            last_name="One",
            license_number="XYZ123",
        )
        driver2 = get_user_model().objects.create(
            username="driver2",
            password="test123",
            first_name="Driver",
            last_name="Two",
            license_number="XYZ456",
        )

        car.drivers.add(driver1, driver2)

        self.assertEqual(list(car.drivers.all()), [driver1, driver2])
