from django.test import TestCase
from django.urls import reverse
from taxi.models import Driver, Car, Manufacturer


class SearchTestCase(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="testdriver",
            password="123test"
        )

        self.manufacturer = Manufacturer.objects.create(
            name="testmanufacturer",
            country="testcountry"
        )

        self.car = Car.objects.create(
            model="Tesla Model S",
            manufacturer=self.manufacturer
        )

        # login
        self.client.login(username="testdriver", password="123test")

    def test_search_drivers(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=test"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver.username)

    def test_search_cars(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=Tesla")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tesla Model S")

    def test_search_manufacturers(self):
        response = self.client.get(reverse("taxi:manufacturer-list")
                                   + "?name=facturer")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testmanufacturer")

    def test_search_no_results(self):
        response = self.client.get(
            reverse("taxi:driver-list")
            + "?username=nonexistent")
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["object_list"], [])
