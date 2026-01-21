from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Driver, Car, Manufacturer


class TaxiViewsTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser",
                                                         password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )
        self.driver = Driver.objects.create(
            username="driver",
            password="testpass",
            license_number="D12345"
        )

    def test_index_view(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("num_visits", response.context)

    def test_manufacturer_list_view(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.manufacturer, response.context["manufacturer_list"])

    def test_manufacturer_create_view(self):
        response = self.client.post(reverse("taxi:manufacturer-create"),
                                    {"name": "Ford", "country": "USA"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Manufacturer.objects.filter(name="Ford").exists())

    def test_car_list_view(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.car, response.context["object_list"])

    def test_car_detail_view(self):
        response = self.client.get(reverse(
            "taxi:car-detail",
            args=[self.car.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], self.car)

    def test_driver_list_view(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.driver, response.context["object_list"])

    def test_toggle_assign_to_car(self):
        # Спочатку додаємо користувача до списку водіїв авто
        self.car.drivers.add(self.user)
        self.car.save()
        self.assertIn(self.user, self.car.drivers.all())
        response = self.client.post(reverse(
            "taxi:toggle-assign-to-car",
            args=[self.car.id])
        )
        self.assertEqual(response.status_code, 302)
        self.car.refresh_from_db()
        self.assertNotIn(self.user, self.car.drivers.all())
