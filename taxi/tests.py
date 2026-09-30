from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from .models import Driver, Car, Manufacturer


class DriverModelTest(TestCase):
    def test_str_method(self):
        driver = Driver(username="test_driver")
        self.assertEqual(str(driver), "test_driver")


class ManufacturerModelTest(TestCase):
    def test_str_method(self):
        manufacturer = Manufacturer(name="Toyota")
        self.assertEqual(str(manufacturer), "Toyota")


class CarModelTest(TestCase):
    def test_str_method(self):
        manufacturer = Manufacturer(name="Toyota")
        manufacturer.save()
        car = Car(model="Camry", manufacturer=manufacturer)
        self.assertEqual(str(car), "Toyota Camry")


class DriverListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

        Driver.objects.create(username="driver1", license_number="ABC12345")
        Driver.objects.create(username="driver2", license_number="ABC12346")

    def test_list_view(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver1")

    def test_search_by_username(self):
        response = self.client.get(reverse("taxi:driver-list") + "?q=driver1")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver1")
        self.assertNotContains(response, "driver2")


class CarListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

        self.manufacturer = Manufacturer.objects.create(name="Toyota")
        Car.objects.create(model="Camry", manufacturer=self.manufacturer)
        Car.objects.create(model="Corolla", manufacturer=self.manufacturer)

    def test_search_by_model(self):
        response = self.client.get(reverse("taxi:car-list") + "?q=Camry")
        self.assertContains(response, "Camry")
        self.assertNotContains(response, "Corolla")


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

        Manufacturer.objects.create(name="Toyota")
        Manufacturer.objects.create(name="Honda")

    def test_search_by_name(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-list") + "?q=Toyota"
        )
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Honda")
