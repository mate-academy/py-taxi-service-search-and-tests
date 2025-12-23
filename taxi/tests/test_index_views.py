from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class PublicIndexTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        self.manufacturer.save()

        self.driver = get_user_model().objects.create_user(
            username="Test Driver",
            password="TestPassword123",
        )
        self.driver.save()

        self.car = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer,
        )
        self.car.save()
        self.car.drivers.add(self.driver)

        self.url = reverse("taxi:index")

    def test_login_required(self):
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)


class PrivateIndexTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        self.manufacturer.save()

        self.driver = get_user_model().objects.create_user(
            username="Test Driver",
            first_name="Test First",
            last_name="Test Last",
            password="TestPassword123",
            license_number="ABC12345",
        )
        self.driver.save()

        self.car = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer,
        )
        self.car.save()
        self.car.drivers.add(self.driver)

        self.client.force_login(self.driver)

        self.url = reverse("taxi:index")

    def test_retrieve_user_index(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        cars_count = Car.objects.count()
        drivers_count = get_user_model().objects.count()
        manufacturer_count = Manufacturer.objects.count()
        self.assertEqual(response.context["num_cars"], cars_count)
        self.assertEqual(response.context["num_drivers"], drivers_count)
        self.assertEqual(
            response.context["num_manufacturers"],
            manufacturer_count
        )
