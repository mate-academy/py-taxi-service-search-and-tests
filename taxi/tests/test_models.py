from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):

    def setUp(self):
        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford", country="USA")
        self.manufacturer3 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        self.driver1 = get_user_model().objects.create_user(
            username="driver1", password="test123",
            first_name="John",
            last_name="Doe",
            license_number="L123456"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver2",
            password="test123",
            first_name="Jane",
            last_name="Smith",
            license_number="L654321"
        )
        self.driver3 = get_user_model().objects.create_user(
            username="driver3",
            password="test123",
            first_name="Emily",
            last_name="Johnson",
            license_number="L789012"
        )

        self.car1 = Car.objects.create(
            model="Corolla", manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Mustang", manufacturer=self.manufacturer2
        )
        self.car3 = Car.objects.create(
            model="X5", manufacturer=self.manufacturer3
        )

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer1), "Toyota Japan")
        self.assertEqual(str(self.manufacturer2), "Ford USA")
        self.assertEqual(str(self.manufacturer3), "BMW Germany")

    def test_driver_str(self):
        self.assertEqual(str(self.driver1), "driver1 (John Doe)")
        self.assertEqual(str(self.driver2), "driver2 (Jane Smith)")
        self.assertEqual(str(self.driver3), "driver3 (Emily Johnson)")

    def test_car_str(self):
        self.assertEqual(str(self.car1), "Corolla")
        self.assertEqual(str(self.car2), "Mustang")
        self.assertEqual(str(self.car3), "X5")

    def test_create_driver_with_license(self):
        driver = get_user_model().objects.create_user(
            username="test_driver",
            password="test123",
            license_number="QWE12345"
        )
        self.assertEqual(driver.username, "test_driver")
        self.assertEqual(driver.license_number, "QWE12345")
        self.assertTrue(driver.check_password("test123"))

    def test_search_manufacturers(self):
        search_result = Manufacturer.objects.filter(name__icontains="To")
        self.assertIn(self.manufacturer1, search_result)
        self.assertNotIn(self.manufacturer2, search_result)
        self.assertNotIn(self.manufacturer3, search_result)

    def test_search_cars(self):
        search_result = Car.objects.filter(model__icontains="X")
        self.assertIn(self.car3, search_result)
        self.assertNotIn(self.car1, search_result)
        self.assertNotIn(self.car2, search_result)
