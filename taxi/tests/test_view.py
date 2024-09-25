from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy

from taxi.models import Manufacturer, Car, Driver


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="test_admin", password="admin_12345"
        )
        self.client.force_login(self.admin_user)
        self.manufacturer = Manufacturer.objects.create(
            name="Nissan", country="Japan"
        )
        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            password="driver_12345",
            license_number="DRV12345"
        )
        self.car = Car.objects.create(
            model="Skyline",
            manufacturer=self.manufacturer,
        )
        # self.car.drivers.set([self.driver])


class IndexViewTests(ViewTests):
    def test_index_view(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cars")
        self.assertContains(response, "Drivers")
        self.assertContains(response, "Manufacturer")


class ManufacturerListViewTests(ViewTests):
    def test_manufacturer_list_view(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.manufacturer.name)


class ManufacturerCreateViewTests(ViewTests):
    def test_manufacturer_create_view(self):
        form_data = {
            "name": "Bogdan",
            "country": "Ukraine",
        }
        response = self.client.post(
            reverse("taxi:manufacturer-create"), data=form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Manufacturer.objects.filter(name="Bogdan").exists())


class ManufacturerUpdateViewTests(ViewTests):
    def test_manufacturer_update_view(self):
        form_data = {
            "name": "Updated Nissan",
            "country": "Updated Japan",
        }
        response = self.client.post(
            reverse("taxi:manufacturer-update", args=[self.manufacturer.id]),
            data=form_data,
        )
        self.assertEqual(response.status_code, 302)
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, "Updated Nissan")


class ManufacturerDeleteViewTests(ViewTests):
    def test_manufacturer_delete_view(self):
        response = self.client.post(
            reverse("taxi:manufacturer-delete", args=[self.manufacturer.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Manufacturer.objects.filter(name="Nissan").exists())


class CarListViewTests(ViewTests):
    def test_car_list_view(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Skyline")


class CarCreateViewTests(ViewTests):
    def test_car_create_view(self):
        form_data = {
            "model": "Datsun_240Z",
            "manufacturer": self.manufacturer.id,
            "drivers": self.driver.id,
        }
        response = self.client.post(reverse("taxi:car-create"), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Car.objects.filter(model="Datsun_240Z").exists())


class CarUpdateViewTests(ViewTests):
    def test_car_update_view(self):
        form_data = {
            "model": "Updated Skyline",
            "manufacturer": self.manufacturer.id,
            "drivers": self.driver.id,
        }
        response = self.client.post(
            reverse(
                "taxi:car-update", args=[self.car.id]
            ),
            data=form_data
        )
        self.assertEqual(response.status_code, 302)
        self.car.refresh_from_db()
        self.assertEqual(self.car.model, "Updated Skyline")


class CarDeleteViewTests(ViewTests):
    def test_car_delete_view(self):
        response = self.client.post(
            reverse("taxi:car-delete", args=[self.car.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Car.objects.filter(model="Skyline").exists())


class DriverListViewTests(ViewTests):
    def test_driver_list_view(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_driver")


class DriverCreateViewTests(ViewTests):
    def test_driver_create_view(self):
        form_data = {
            "username": "new_driver",
            "password1": "pass_1234",
            "password2": "pass_1234",
            "license_number": "NEW12345",
        }
        response = self.client.post(
            reverse("taxi:driver-create"),
            data=form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Driver.objects.filter(username="new_driver").exists())


class DriverLicenseUpdateViewTests(ViewTests):
    def test_driver_license_update_view(self):
        form_data = {"license_number": "NEW12345"}
        response = self.client.post(
            reverse(
                "taxi:driver-update",
                args=[self.driver.id]
            ),
            data=form_data
        )
        self.assertEqual(response.status_code, 302)
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.license_number, "NEW12345")


class DriverDeleteViewTests(ViewTests):
    success_url = "taxi.views.DriverDeleteView.success_url"

    @patch(success_url, reverse_lazy("taxi:driver-list"))
    def test_driver_delete_view(self):
        response = self.client.post(
            reverse("taxi:driver-delete", args=[self.driver.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Driver.objects.filter(username="test_driver").exists()
        )


class ToggleAssignToCarTests(ViewTests):
    def test_toggle_assign_to_car(self):
        self.client.force_login(self.driver)
        self.assertNotIn(self.car, self.driver.cars.all())

        response = self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.car, list(self.driver.cars.all()))

        # Toggle again to remove the car
        response = self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.car, list(self.driver.cars.all()))
