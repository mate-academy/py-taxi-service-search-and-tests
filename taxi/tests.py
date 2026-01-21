from django.test import TestCase
from django.urls import reverse
from .models import Driver, Car, Manufacturer


class CustomSearchFeatureTests(TestCase):
    def setUp(self):
        self.manufacturer_audi = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        self.manufacturer_bmw = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        self.car_a4 = Car.objects.create(
            model="A4",
            manufacturer=self.manufacturer_audi
        )
        self.car_x5 = Car.objects.create(
            model="X5",
            manufacturer=self.manufacturer_bmw
        )

        self.driver_alex = Driver.objects.create_user(
            username="alex_smith",
            password="securepass1",
            license_number="AS123456"
        )
        self.driver_emma = Driver.objects.create_user(
            username="emma_jones",
            password="securepass2",
            license_number="EJ654321"
        )
        self.client.login(
            username="alex_smith",
            password="securepass1"
        )

    def test_search_manufacturer_by_name(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-list"), {"name": "Audi"}
        )
        self.assertContains(response, "Audi")
        self.assertNotContains(response, "BMW")

    def test_search_car_by_model(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": "A4"})
        self.assertContains(response, "A4")
        self.assertNotContains(response, "X5")

    def test_search_driver_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "alex_smith"}
        )
        self.assertContains(response, "alex_smith")
        self.assertNotContains(response, "emma_jones")

    def test_search_no_results(self):
        response = self.client.get(reverse(
            "taxi:driver-list"), {"username": "non_existent_user"}
        )
        self.assertEqual(response.context["driver_list"].count(), 0)
