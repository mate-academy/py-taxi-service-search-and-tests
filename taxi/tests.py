from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

# Create your tests here.
from taxi.models import Car, Manufacturer


class PublicViewTest(TestCase):
    def setUp(self):
        model = get_user_model()
        self.driver = model.objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345",
        )

    def test_car_list_view_redirects_for_anonymous_user(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertRedirects(response, "/accounts/login/?next=/cars/")

    def test_driver_login_view(self):
        login = self.client.login(username="testuser", password="testpass123")
        self.assertTrue(login)

    def test_if_user_can_access_car_list_view(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)


class ManufacturerModelTest(TestCase):
    def setUp(self):
        model = get_user_model()
        self.driver = model.objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345",
        )
        self.client.force_login(self.driver)

    def test_string_representation(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.assertEqual(str(manufacturer), "Toyota")

    def test_search_by_name(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Honda", country="Japan")
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, data={"name": "toy"})
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Honda")


class CarViewTest(TestCase):
    def setUp(self):
        model = get_user_model()
        self.driver = model.objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345",
        )
        self.client.force_login(self.driver)
        self.manufacturer = Manufacturer.objects.create(
            name="Ferrari", country="Italy"
        )

    def test_search_by_model(self):
        Car.objects.create(
            model="Ferrari F8",
            manufacturer=self.manufacturer,
        )
        Car.objects.create(
            model="Fiat Uno",
            manufacturer=self.manufacturer,
        )
        url = reverse("taxi:car-list")
        response = self.client.get(url, data={"model": "ferrari"})
        self.assertContains(response, "Ferrari F8")
        self.assertNotContains(response, "Fiat Uno")


class DriverListViewTest(TestCase):
    def setUp(self):
        model = get_user_model()
        self.driver1 = model.objects.create_user(
            username="testuser1",
            password="testpass123",
            license_number="ABC12345",
        )
        self.driver2 = model.objects.create_user(
            username="testuser2",
            password="testpass123",
            license_number="DEF67890",
        )
        self.client.force_login(self.driver1)

    def test_search_by_username(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, data={"username": "testuser1"})
        self.assertContains(response, "testuser1")
        self.assertNotContains(response, "testuser2")
