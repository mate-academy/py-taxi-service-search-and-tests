from django.test import TestCase, Client
from django.urls import reverse
from .models import Driver, Car, Manufacturer


class SearchTests(TestCase):

    def setUp(self):
        self.client = Client()

        self.manufacturer1 = Manufacturer.objects.create(name="Toyota")
        self.manufacturer2 = Manufacturer.objects.create(name="honda")
        self.driver1 = Driver.objects.create(username="Alice_123", email="a@a.com")
        self.driver2 = Driver.objects.create(username="Bob_456", email="b@b.com")
        self.car1 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Civic",
            manufacturer=self.manufacturer2
        )

        self.drivers_url = reverse("taxi:driver_list")
        self.cars_url = reverse("taxi:car_list")
        self.manufacturers_url = reverse("taxi:manufacturer_list")

    def test_driver_list_no_search(self):
        response = self.client.get(self.drivers_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["drivers"]), 2)

    def test_driver_list_search_icontains(self):
        response = self.client.get(self.drivers_url, {"q": "Alice"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["drivers"]), 1)

    def test_driver_list_search_case_insensitive(self):
        response = self.client.get(self.drivers_url, {"q": "BOB"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["drivers"]), 1)

    def test_car_list_search_model(self):
        response = self.client.get(self.cars_url, {"q": "olla"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["cars"]), 1)

    def test_manufacturer_list_search_name_case(self):
        response = self.client.get(self.manufacturers_url, {"q": "HONDA"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturers"]), 1)

    def test_search_form_present_on_drivers_page(self):
        response = self.client.get(self.drivers_url)
        self.assertContains(response, '<input type="text" name="q"')

