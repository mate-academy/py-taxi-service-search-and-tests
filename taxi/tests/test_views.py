from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Car, Manufacturer


class PublicTaxiViewsTest(TestCase):
    def test_login_required(self):
        res = self.client.get("taxi:index")
        self.assertNotEquals(res.status_code, 200)


class PrivateTaxiViewsTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="Test Country"
        )
        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345",
            password="1qazcde3",
        )
        self.car = Car.objects.create(
            model="Test Model", manufacturer=self.manufacturer
        )
        self.driver.cars.add(self.car)
        self.client.force_login(self.driver)

    def test_index_view(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Taxi Service Home")
        self.assertContains(response, "Drivers:")
        self.assertContains(response, "Cars:")
        self.assertContains(response, "Manufacturers:")

    def test_manufacturer_list_view(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Manufacturer")

    def test_car_list_view(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Model")

    def test_driver_list_view(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_driver")

    def test_car_detail_view(self):
        response = self.client.get(
            reverse(
                "taxi:car-detail",
                args=[self.car.pk]
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Model")

    def test_driver_detail_view(self):
        response = self.client.get(
            reverse(
                "taxi:driver-detail",
                args=[self.driver.pk]
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_driver")
