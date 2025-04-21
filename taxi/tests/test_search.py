from django.test import TestCase
from django.urls import reverse
from taxi.models import Driver, Manufacturer, Car


class SearchFeatureTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="searchuser",
            password="pass12345",
            license_number="ZZZ12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="SearchMaker", country="US"
        )
        self.car = Car.objects.create(
            model="SearchModel",
            manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.driver)
        self.client.login(
            username="searchuser",
            password="pass12345"
        )

    def test_search_driver_by_username(self):
        response = self.client.get(reverse(
            "taxi:driver-list"),
            {"username": "searchuser"}
        )
        self.assertContains(response, "searchuser")

    def test_search_car_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "SearchModel"}
        )
        self.assertContains(response, "SearchModel")

    def test_search_manufacturer_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "SearchMaker"}
        )
        self.assertContains(response, "SearchMaker")
