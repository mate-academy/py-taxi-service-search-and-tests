from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Driver, Car, Manufacturer

User = get_user_model()


class TaxiTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="12345",
            license_number="ABC12345",
        )
        self.client = Client()
        self.client.login(username="testuser", password="12345")

        self.driver1 = Driver.objects.create(
            username="driver1",
            license_number="DEF12345",
            first_name="John",
            last_name="Doe"
        )
        self.driver2 = Driver.objects.create(
            username="driver2",
            license_number="GHI12345",
            first_name="Jane",
            last_name="Smith"
        )
        self.manufacturer = (Manufacturer.objects
                             .create(name="Toyota"))
        self.car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.driver1)

    def test_driver_search(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"search_term": "driver1"})
        self.assertContains(response, "driver1")
        self.assertNotContains(response, "driver2")

    def test_car_search(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"search_term": "Camry"})
        self.assertContains(response, "Camry")
        response = self.client.get(url, {"search_term": "NonExistingCar"})
        self.assertNotContains(response, "Camry")

    def test_manufacturer_search(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"search_term": "Toyota"})
        self.assertContains(response, "Toyota")
        response = self.client.get(url, {"search_term": "Honda"})
        self.assertNotContains(response, "Toyota")

    def test_driver_create_view(self):
        url = reverse("taxi:driver-create")
        self.client.post(url, {
            "username": "driver3",
            "password1": "testpass123",
            "password2": "testpass123",
            "license_number": "JKL12345",
        })
        self.assertEqual(Driver.objects.filter(username="driver3").count(), 1)

    def test_driver_detail_view(self):
        url = reverse("taxi:driver-detail", args=[self.driver1.id])
        response = self.client.get(url)
        self.assertContains(response, "driver1")

    def test_toggle_assign_to_car_add_and_remove(self):
        self.client.force_login(self.driver1)

        url = reverse("taxi:toggle-car-assign", args=[self.car.id])

        self.driver1.cars.clear()

        self.client.get(url)
        self.driver1.refresh_from_db()
        self.assertIn(self.car, self.driver1.cars.all())

        self.client.get(url)
        self.driver1.refresh_from_db()
        self.assertNotIn(self.car, self.driver1.cars.all())

    def test_search_in_manufacturer_list(self):
        url = reverse("taxi:manufacturer-list")
        res = self.client.get(url + "?search_term=Toyota")

        manufacturers = Manufacturer.objects.filter(name__icontains="Toyota")
        self.assertEqual(list(res.context["manufacturer_list"]),
                         list(manufacturers))

    def test_search_in_car_list(self):
        url = reverse("taxi:car-list")
        res = self.client.get(url + "?search_term=Camry")

        cars = Car.objects.filter(model__icontains="Camry")
        self.assertEqual(list(res.context["car_list"]), list(cars))

    def test_search_in_driver_list(self):
        url = reverse("taxi:driver-list")
        res = self.client.get(url + "?search_term=test")

        drivers = get_user_model().objects.filter(username__icontains="test")
        self.assertEqual(list(res.context["driver_list"]), list(drivers))
