from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car, Driver


class TaxiViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="admin",
            password="StrongPass123!",
            license_number="LIC12345",
        )
        self.client.login(username="admin", password="StrongPass123!")
        self.manufacturer = Manufacturer.objects.create(name="Toyota",
                                                        country="Japan")
        self.car = Car.objects.create(model="Corolla",
                                      manufacturer=self.manufacturer)

    def test_index_view(self):
        url = reverse("taxi:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("num_drivers", response.context)
        self.assertIn("num_cars", response.context)
        self.assertIn("num_manufacturers", response.context)

    def test_manufacturer_list_view(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.manufacturer.name)

    def test_manufacturer_create_view(self):
        url = reverse("taxi:manufacturer-create")
        response = self.client.post(url, {"name": "Honda", "country": "Japan"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Manufacturer.objects.filter(name="Honda").exists())

    def test_manufacturer_update_view(self):
        url = reverse("taxi:manufacturer-update",
                      args=[self.manufacturer.id])
        response = self.client.post(url, {"name": "ToyotaUpdated",
                                          "country": "Japan"})
        self.assertEqual(response.status_code, 302)
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, "ToyotaUpdated")

    def test_manufacturer_delete_view(self):
        url = reverse("taxi:manufacturer-delete", args=[self.manufacturer.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Manufacturer.objects.filter(
            id=self.manufacturer.id).exists())

    def test_car_list_view(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car.model)

    def test_car_detail_view(self):
        url = reverse("taxi:car-detail", args=[self.car.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car.model)

    def test_driver_list_view(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("driver_list", response.context)

    def test_driver_license_update_view(self):
        url = reverse("taxi:driver-update", args=[self.user.id])
        response = self.client.post(url, {"license_number": "XYZ12345"})
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.license_number, "XYZ12345")

    def test_toggle_assign_to_car_add_and_remove(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.car, self.user.cars.all())
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.car, self.user.cars.all())
