from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Driver, Car, Manufacturer


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345"
        )
        self.client.login(username="testuser", password="testpass123")

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )

        self.car = Car.objects.create(
            model="Camry", manufacturer=self.manufacturer
        )

    def test_index_view(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")
        self.assertIn("num_drivers", response.context)
        self.assertIn("num_cars", response.context)
        self.assertIn("num_manufacturers", response.context)
        self.assertIn("num_visits", response.context)

    def test_manufacturer_list_view(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertIn(self.manufacturer, response.context["manufacturer_list"])

    def test_car_list_view(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.car, response.context["car_list"])

    def test_car_detail_view(self):
        response = self.client.get(reverse("taxi:car-detail", args=[self.car.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["car"], self.car)

    def test_driver_list_view(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user, response.context["driver_list"])

    def test_driver_detail_view(self):
        response = self.client.get(reverse("taxi:driver-detail", args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["driver"], self.user)

    def test_toggle_assign_to_car_add(self):
        response = self.client.post(reverse("taxi:toggle-car-assign", args=[self.car.id]))
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertIn(self.car, self.user.cars.all())

    def test_toggle_assign_to_car_remove(self):
        self.user.cars.add(self.car)
        response = self.client.post(reverse("taxi:toggle-car-assign", args=[self.car.id]))
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertNotIn(self.car, self.user.cars.all())
