# flake8: noqa: E731

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")
CAR_DETAIL_URL = lambda pk: reverse("taxi:car-detail", args=[pk])
CAR_CREATE_URL = reverse("taxi:car-create")
CAR_UPDATE_URL = lambda pk: reverse("taxi:car-update", args=[pk])
CAR_DELETE_URL = lambda pk: reverse("taxi:car-delete", args=[pk])


class PublicCarTests(TestCase):
    def test_login_required(self):
        """Test that login is required for accessing the car list view"""
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self):
        """Set up a logged-in user and sample data"""
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.driver = get_user_model().objects.create_user(
            username="driver1",
            password="password123",
            license_number="ABC12345",
        )
        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)

    def test_retrieve_car_list(self):
        """Test retrieving the car list"""
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.car, response.context["car_list"])
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_car_by_model(self):
        """Test searching cars by model"""
        Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer,
        )
        response = self.client.get(CAR_LIST_URL, {"model": "Corolla"})
        self.assertEqual(len(response.context["car_list"]), 1)
        self.assertEqual(response.context["car_list"][0], self.car)

    def test_retrieve_car_detail(self):
        """Test retrieving the car detail"""
        url = CAR_DETAIL_URL(self.car.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["car"], self.car)
        self.assertTemplateUsed(response, "taxi/car_detail.html")

    def test_create_car(self):
        """Test creating a new car"""
        from_data = {
            "model": "Prius",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id]
        }
        response = self.client.post(CAR_CREATE_URL, data=from_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Car.objects.filter(model="Prius").exists())
        car = Car.objects.get(model="Prius")
        self.assertEqual(car.manufacturer, self.manufacturer)
        self.assertIn(self.driver, car.drivers.all())

    def test_update_car(self):
        """Test updating an existing car"""
        new_driver = get_user_model().objects.create_user(
            username="driver2",
            password="password123",
            license_number="DEF67890",
        )
        from_data = {
            "model": "Corolla Updated",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id, new_driver.id]
        }
        url = CAR_UPDATE_URL(self.car.id)
        response = self.client.post(url, data=from_data)
        self.car.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.car.model, "Corolla Updated")
        self.assertIn(new_driver, self.car.drivers.all())

    def test_delete_car(self):
        """Test deleting a car"""
        url = CAR_DELETE_URL(self.car.id)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Car.objects.filter(id=self.car.id).exists())
