from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car


class DriverSearchTests(TestCase):
    """Test driver search functionality"""

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="TEST123"
        )
        self.client.force_login(self.user)

        self.driver1 = get_user_model().objects.create_user(
            username="john_driver",
            password="pass123",
            license_number="JD001"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="jane_driver",
            password="pass123",
            license_number="JD002"
        )
        self.driver3 = get_user_model().objects.create_user(
            username="bob_taxi",
            password="pass123",
            license_number="BT001"
        )

    def test_search_driver_by_username(self):
        """Test searching drivers by username"""
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=john"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john_driver")
        self.assertNotContains(response, "bob_taxi")

    def test_search_driver_partial_match(self):
        """Test searching drivers with partial username match"""
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=driver"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john_driver")
        self.assertContains(response, "jane_driver")
        self.assertNotContains(response, "bob_taxi")

    def test_search_driver_case_insensitive(self):
        """Test that search is case insensitive"""
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=JOHN"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john_driver")

    def test_search_driver_no_results(self):
        """Test searching drivers with no matching results"""
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=nonexistent"
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "john_driver")
        self.assertNotContains(response, "jane_driver")

    def test_search_driver_empty_query(self):
        """Test that empty search returns all drivers"""
        response = self.client.get(
            reverse("taxi:driver-list") + "?username="
        )
        self.assertEqual(response.status_code, 200)
        drivers = response.context["driver_list"]
        self.assertEqual(len(drivers), 4)


class CarSearchTests(TestCase):
    """Test car search functionality"""

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="TEST123"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

        self.car1 = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )
        self.car3 = Car.objects.create(
            model="RAV4",
            manufacturer=self.manufacturer
        )

    def test_search_car_by_model(self):
        """Test searching cars by model"""
        response = self.client.get(
            reverse("taxi:car-list") + "?model=Camry"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camry")
        self.assertNotContains(response, "RAV4")

    def test_search_car_partial_match(self):
        """Test searching cars with partial model match"""
        response = self.client.get(
            reverse("taxi:car-list") + "?model=Co"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")

    def test_search_car_case_insensitive(self):
        """Test that car search is case insensitive"""
        response = self.client.get(
            reverse("taxi:car-list") + "?model=camry"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camry")

    def test_search_car_no_results(self):
        """Test searching cars with no matching results"""
        response = self.client.get(
            reverse("taxi:car-list") + "?model=Tesla"
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Camry")

    def test_search_car_empty_query(self):
        """Test that empty search returns all cars"""
        response = self.client.get(
            reverse("taxi:car-list") + "?model="
        )
        self.assertEqual(response.status_code, 200)
        cars = response.context["car_list"]
        self.assertEqual(len(cars), 3)


class ManufacturerSearchTests(TestCase):
    """Test manufacturer search functionality"""

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="TEST123"
        )
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        self.manufacturer3 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

    def test_search_manufacturer_by_name(self):
        """Test searching manufacturers by name"""
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=Toyota"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "BMW")

    def test_search_manufacturer_partial_match(self):
        """Test searching manufacturers with partial name match"""
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=Te"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tesla")

    def test_search_manufacturer_case_insensitive(self):
        """Test that manufacturer search is case insensitive"""
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=toyota"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")

    def test_search_manufacturer_no_results(self):
        """Test searching manufacturers with no matching results"""
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=Ferrari"
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Toyota")

    def test_search_manufacturer_empty_query(self):
        """Test that empty search returns all manufacturers"""
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name="
        )
        self.assertEqual(response.status_code, 200)
        manufacturers = response.context["manufacturer_list"]
        self.assertEqual(len(manufacturers), 3)
