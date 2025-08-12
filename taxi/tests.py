

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Manufacturer, Car, Driver

class ManufacturerListViewTest(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(username="testuser", password="testpass")
		Manufacturer.objects.create(name="Toyota", country="Japan")
		Manufacturer.objects.create(name="Ford", country="USA")

	def test_search_by_name(self):
		self.client.login(username="testuser", password="testpass")
		response = self.client.get(reverse("taxi:manufacturer-list"), {"name": "toy"})
		self.assertContains(response, "Toyota")
		self.assertNotContains(response, "Ford")


class CarListViewTest(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(username="testuser", password="testpass")
		self.manufacturer = Manufacturer.objects.create(name="Toyota", country="Japan")
		Car.objects.create(model="Corolla", manufacturer=self.manufacturer)
		Car.objects.create(model="Camry", manufacturer=self.manufacturer)

	def test_search_by_model(self):
		self.client.login(username="testuser", password="testpass")
		response = self.client.get(reverse("taxi:car-list"), {"model": "Corolla"})
		self.assertContains(response, "Corolla")
		self.assertNotContains(response, "Camry")


class DriverListViewTest(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(username="testuser", password="testpass")
		Driver.objects.create_user(username="driver1", password="pass1", license_number="12345")
		Driver.objects.create_user(username="driver2", password="pass2", license_number="67890")

	def test_search_by_username(self):
		self.client.login(username="testuser", password="testpass")
		response = self.client.get(reverse("taxi:driver-list"), {"username": "driver1"})
		self.assertContains(response, "driver1")
		self.assertNotContains(response, "driver2")


class IndexViewTest(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(username="testuser", password="testpass")

	def test_index_view_counts(self):
		Manufacturer.objects.create(name="Toyota", country="Japan")
		Car.objects.create(model="Corolla", manufacturer=Manufacturer.objects.first())
		Driver.objects.create_user(username="driver1", password="pass1", license_number="12345")
		self.client.login(username="testuser", password="testpass")
		response = self.client.get(reverse("taxi:index"))
		self.assertContains(response, "<li><strong>Cars:</strong> 1</li>", html=True)
		self.assertContains(response, "<li><strong>Drivers:</strong> 2</li>", html=True)
		self.assertContains(response, "<li><strong>Manufacturers:</strong> 1</li>", html=True)
