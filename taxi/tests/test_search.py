from django.test import TestCase
from django.urls import reverse
from taxi.models import Driver, Car, Manufacturer


class SearchTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.manufacturer1 = Manufacturer.objects.create(name="Toyota",
                                                        country="Japan")
        cls.manufacturer2 = Manufacturer.objects.create(name="Ford",
                                                        country="USA")

        cls.car1 = Car.objects.create(model="Corolla",
                                      manufacturer=cls.manufacturer1)
        cls.car2 = Car.objects.create(model="Focus",
                                      manufacturer=cls.manufacturer2)

        cls.driver1 = Driver.objects.create_user(username="john",
                                                 password="pass1234",
                                                 license_number="ABC12345")
        cls.driver2 = Driver.objects.create_user(username="alice",
                                                 password="pass1234",
                                                 license_number="XYZ54321")

    def setUp(self):
        self.client.login(username="john", password="pass1234")

    # --- DRIVER SEARCH ---
    def test_driver_search_found(self):
        response = self.client.get(reverse("taxi:driver-list"),
                                   {"search": "john"})
        self.assertContains(response, "john")
        self.assertNotContains(response, "alice")

    def test_driver_search_not_found(self):
        response = self.client.get(reverse("taxi:driver-list"),
                                   {"search": "mike"})
        self.assertContains(response, "There are no drivers in the service.")

    # --- CAR SEARCH ---
    def test_car_search_found(self):
        response = self.client.get(reverse("taxi:car-list"),
                                   {"search": "Corolla"})
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Focus")

    def test_car_search_not_found(self):
        response = self.client.get(reverse("taxi:car-list"),
                                   {"search": "Civic"})
        self.assertContains(response, "There are no cars in the service.")

    # --- MANUFACTURER SEARCH ---
    def test_manufacturer_search_found(self):
        response = self.client.get(reverse("taxi:manufacturer-list"),
                                   {"search": "Toyota"})
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")

    def test_manufacturer_search_not_found(self):
        response = self.client.get(reverse("taxi:manufacturer-list"),
                                   {"search": "Honda"})
        self.assertContains(response,
                            "There are no manufacturers in the service.")

    # --- SEARCH FIELD VALUE PRESERVED ---
    def test_search_field_preserved_in_driver_list(self):
        response = self.client.get(reverse("taxi:driver-list"),
                                   {"search": "john"})
        self.assertContains(response, 'value="john"')

    def test_search_field_preserved_in_car_list(self):
        response = self.client.get(reverse("taxi:car-list"),
                                   {"search": "Corolla"})
        self.assertContains(response, 'value="Corolla"')

    def test_search_field_preserved_in_manufacturer_list(self):
        response = self.client.get(reverse("taxi:manufacturer-list"),
                                   {"search": "Toyota"})
        self.assertContains(response, 'value="Toyota"')
