from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        """creation of test objects from manufacturers for use in tests"""
        self.user = get_user_model().objects.create_user(
            username="testdriver",
            password="testpassword",
            license_number="AB12345678"
        )
        self.client.login(username="testdriver", password="testpassword")
        self.manufacturer1 = Manufacturer.objects.create(
            name="Ford", country="test"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Toyota", country="test"
        )
        self.manufacturer3 = Manufacturer.objects.create(
            name="Honda", country="test"
        )

    def test_view_url_exists_at_desired_location(self):
        """The test verifies that the ManufacturerListView URL exists
            and has the correct path and uses correct template"""
        response = self.client.get("/manufacturers/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_view_displays_manufacturer_list(self):
        """The test checks the display of manufacturers on the page"""
        response = self.client.get("/manufacturers/")
        self.assertContains(response, "Ford")
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Honda")

    def test_search_form_displayed(self):
        """The test checks for the presence of a search form on the page"""
        response = self.client.get("/manufacturers/")
        self.assertContains(response, "Search by name")

    def test_search_works(self):
        """The test checks the operation of the search form
            by manufacturer name"""
        response = self.client.get("/manufacturers/", {"name": "Ford"})
        self.assertContains(response, "Ford")
        self.assertNotContains(response, "Toyota")
        self.assertNotContains(response, "Honda")


class CarListViewTest(TestCase):
    def setUp(self):
        """creation of test objects from cars for use in tests"""
        self.user = get_user_model().objects.create_user(
            username="testdriver",
            password="testpassword",
            license_number="AB12345678"
        )
        self.client.login(username="testdriver", password="testpassword")
        self.manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="test"
        )
        self.car1 = Car.objects.create(
            model="Model1",
            manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="Model2",
            manufacturer=self.manufacturer
        )
        self.car3 = Car.objects.create(
            model="Model3",
            manufacturer=self.manufacturer
        )

    def test_view_url_exists(self):
        """The test verifies that the CarListView URL exists
            and has the correct path and uses correct template"""
        response = self.client.get("/cars/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_view_displays_car_list(self):
        """The test checks the display of cars on the page"""
        response = self.client.get("/cars/")
        self.assertContains(response, "Model1")
        self.assertContains(response, "Model2")
        self.assertContains(response, "Model3")

    def test_search_form_displayed(self):
        """The test checks for the presence of a search form on the page"""
        response = self.client.get("/cars/")
        self.assertContains(response, "Search by model")

    def test_search_works(self):
        """The test checks the operation of the search form by car model"""
        response = self.client.get("/cars/", {"model": "Model1"})
        self.assertContains(response, "Model1")
        self.assertNotContains(response, "Model2")
        self.assertNotContains(response, "Model3")


class DriverListViewTest(TestCase):
    def setUp(self):
        """creation of test objects from cars for use in tests"""
        self.user = get_user_model().objects.create_user(
            username="testdriver",
            password="testpassword",
            license_number="AB12345678"
        )
        self.client.login(username="testdriver", password="testpassword")
        self.driver1 = Driver.objects.create(
            username="driver1",
            password="testpassword",
            license_number="AB12982678"
        )
        self.driver2 = Driver.objects.create(
            username="driver2",
            password="testpassword",
            license_number="AB18452678"
        )
        self.driver3 = Driver.objects.create(
            username="driver3",
            password="testpassword",
            license_number="AB12988628"
        )

    def test_view_url_exists(self):
        """The test verifies that the DriverListView URL exists
            and has the correct path and uses correct template"""
        response = self.client.get("/drivers/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_view_displays_car_list(self):
        """The test checks the display of drivers on the page"""
        response = self.client.get("/drivers/")
        self.assertContains(response, "driver1")
        self.assertContains(response, "driver2")
        self.assertContains(response, "driver3")

    def test_search_form_displayed(self):
        """The test checks for the presence of a search form on the page"""
        response = self.client.get("/drivers/")
        self.assertContains(response, "Search by username")

    def test_search_works(self):
        """The test checks the operation of the search form by car model"""
        response = self.client.get("/drivers/", {"username": "driver1"})
        self.assertContains(response, "driver1")
        self.assertNotContains(response, "driver2")
        self.assertNotContains(response, "driver3")
