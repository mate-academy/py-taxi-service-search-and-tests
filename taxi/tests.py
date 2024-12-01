from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Driver, Car


class ManufacturerModelTests(TestCase):
    # Тест на створення виробника
    def test_manufacturer_creation(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.assertEqual(str(manufacturer), "Toyota Japan")
        self.assertEqual(manufacturer.name, "Toyota")
        self.assertEqual(manufacturer.country, "Japan")

    # Тест на унікальність назви виробника
    def test_manufacturer_unique_name(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        with self.assertRaises(Exception):
            Manufacturer.objects.create(
                name="Toyota", country="USA"
            )

    # Тест на створення водія з іменем та прізвищем
    def test_driver_creation_with_names(self):
        driver = Driver.objects.create_user(
            username="johndoe", password="testpass", license_number="AB12345",
            first_name="John", last_name="Doe"
        )
        self.assertEqual(str(driver), "johndoe (John Doe)")

    # Тест на правильність URL для водія
    def test_driver_get_absolute_url(self):
        driver = Driver.objects.create_user(
            username="johndoe", password="testpass", license_number="AB12345"
        )
        self.assertEqual(driver.get_absolute_url(), f"/drivers/{driver.pk}/")


class CarModelTests(TestCase):
    def setUp(self):
        # Підготовка тестових даних: виробник, водій і машина
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.driver = Driver.objects.create_user(
            username="johndoe", password="testpass", license_number="AB12345"
        )
        self.car = Car.objects.create(model="Camry",
                                      manufacturer=self.manufacturer)

    # Тест на створення машини
    def test_car_creation(self):
        car = Car.objects.create(
            model="Corolla", manufacturer=self.manufacturer
        )
        self.assertEqual(str(car), "Corolla")

    # Тест на зв'язок між машиною та її виробником
    def test_car_manufacturer_relation(self):
        car = Car.objects.create(
            model="Corolla", manufacturer=self.manufacturer
        )
        self.assertEqual(car.manufacturer.name, "Toyota")

    # Тест на асоціацію водія з машиною
    def test_car_driver_association(self):
        self.car.drivers.add(self.driver)
        self.assertIn(self.driver, self.car.drivers.all())

    # Тест на кілька водіїв для однієї машини
    def test_car_multiple_drivers(self):
        driver2 = Driver.objects.create_user(
            username="janedoe", password="testpass", license_number="XY67890"
        )
        self.car.drivers.add(self.driver, driver2)
        self.assertEqual(self.car.drivers.count(), 2)

        # Тест на правильність URL для водія

        def test_driver_get_absolute_url(self):
            driver = Driver.objects.create_user(
                username="johndoe", password="testpass",
                license_number="AB12345"
            )
            expected_url = reverse("taxi:driver-detail",
                                   kwargs={"pk": driver.pk})
            self.assertEqual(driver.get_absolute_url(), expected_url)
