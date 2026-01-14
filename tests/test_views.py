from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car


class IndexViewTest(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 302)


class ManufacturerViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.manufacturer = Manufacturer.objects.create(name="Toyota", country="Japan")

    def test_manufacturer_list_view(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")

    def test_manufacturer_create_view(self):
        response = self.client.post(reverse("taxi:manufacturer-create"), {"name": "Honda", "country": "Japan"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Manufacturer.objects.filter(name="Honda").exists())


class CarViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.manufacturer = Manufacturer.objects.create(name="Ford", country="USA")
        self.car = Car.objects.create(model="Focus", manufacturer=self.manufacturer)

    def test_car_list_view(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Focus")

    def test_car_detail_view(self):
        response = self.client.get(reverse("taxi:car-detail", args=[self.car.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Focus")


class ToggleAssignToCarViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.manufacturer = Manufacturer.objects.create(name="BMW", country="Germany")
        self.car = Car.objects.create(model="X5", manufacturer=self.manufacturer)

    def test_toggle_assign_to_car(self):
        response = self.client.post(reverse("taxi:toggle-car-assign", args=[self.car.pk]))
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertIn(self.car, self.user.cars.all())
