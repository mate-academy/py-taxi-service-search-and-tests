from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer


class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.driver = Driver.objects.create_user(
            username="test_driver_1",
            password="pass1234",
            license_number="TES12345"
        )
        self.client.login(username="test_driver_1", password="pass1234")
        self.manufacturer = Manufacturer.objects.create(name="Test Manufacturer", country="Test Country")
        self.car = Car.objects.create(model="Test Model 1", manufacturer=self.manufacturer)
        self.car.drivers.add(self.driver)

    def test_index_view(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_drivers"], 1)
        self.assertEqual(response.context["num_cars"], 1)
        self.assertEqual(response.context["num_manufacturers"], 1)
        self.assertEqual(response.context["num_visits"], 1)


class ToggleAssignToCarViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.driver = Driver.objects.create_user(
            username="test_driver_1",
            password="pass1234",
            license_number="TES12345"
        )
        self.client.login(username="test_driver_1", password="pass1234")
        self.manufacturer = Manufacturer.objects.create(name="Test Manufacturer", country="Test Country")
        self.car = Car.objects.create(model="Test Model 1", manufacturer=self.manufacturer)

    def test_toggle_assign_to_car_view(self):
        response = self.client.get(reverse("taxi:toggle-car-assign", args=[self.car.id]))
        self.assertEqual(response.status_code, 302)
        self.car.refresh_from_db()
        self.assertIn(self.driver, self.car.drivers.all())
