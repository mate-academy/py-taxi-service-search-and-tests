from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class SearchFormTests(TestCase):
    def setUp(self):
        self.user1 = Driver.objects.create_user(
            username="test1",
            password="test123",
            license_number="TES55555",
        )
        self.user2 = Driver.objects.create_user(
            username="another",
            password="test123",
            license_number="TES55556",
        )
        self.client.force_login(self.user1)

    def test_search_form_in_manufacturer_list(self):
        ferrari = Manufacturer.objects.create(name="Ferrari", country="Italy")
        bmw = Manufacturer.objects.create(name="BMW", country="Germany")

        url = reverse("taxi:manufacturer-list") + "?name=Ferrari"
        response = self.client.get(url)

        self.assertIn(ferrari, response.context["manufacturer_list"])
        self.assertNotIn(bmw, response.context["manufacturer_list"])

    def test_search_form_in_driver_list(self):
        url = reverse("taxi:driver-list") + "?username=test1"
        response = self.client.get(url)

        self.assertIn(self.user1, response.context["driver_list"])
        self.assertNotIn(self.user2, response.context["driver_list"])

    def test_search_form_in_car_list(self):
        ferrari = Manufacturer.objects.create(name="Ferrari", country="Italy")
        bmw = Manufacturer.objects.create(name="BMW", country="Germany")

        car1 = Car.objects.create(model="250 GTO", manufacturer=ferrari)
        car2 = Car.objects.create(model="M3", manufacturer=bmw)

        url = reverse("taxi:car-list") + "?model=250"
        response = self.client.get(url)

        self.assertIn(car1, response.context["car_list"])
        self.assertNotIn(car2, response.context["car_list"])
