from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import (Manufacturer,
                         Driver,
                         Car)

User = get_user_model()


class BaseTestSetup(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass"
        )
        self.client.login(
            username="testuser",
            password="testpass"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )


class IndexViewTest(BaseTestSetup):
    def test_index_view(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")
        self.assertIn("num_drivers", response.context)
        self.assertIn("num_cars", response.context)
        self.assertIn("num_manufacturers", response.context)


class ManufacturerListViewTest(BaseTestSetup):
    def setUp(self):
        super().setUp()
        Manufacturer.objects.create(name="Ford", country="USA")

    def test_manufacturer_list_view(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertEqual(len(response.context["manufacturer_list"]), 2)


class ManufacturerCreateViewTest(BaseTestSetup):
    def test_manufacturer_create_view(self):
        response = self.client.post(
            reverse("taxi:manufacturer-create"),
            {"name": "BMW", "country": "Germany"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Manufacturer.objects.filter(name="BMW").exists())


class CarListViewTest(BaseTestSetup):
    def test_car_list_view(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertEqual(len(response.context["car_list"]), 1)


class CarDetailViewTest(BaseTestSetup):
    def test_car_detail_view(self):
        response = self.client.get(
            reverse("taxi:car-detail",
                    args=[self.car.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")
        self.assertEqual(response.context["car"], self.car)


class DriverListViewTest(BaseTestSetup):
    def setUp(self):
        super().setUp()
        Driver.objects.create(
            username="driver1",
            license_number="ABC123456"
        )
        Driver.objects.create(
            username="driver2",
            license_number="XYZ987654"
        )

    def test_driver_list_view(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertEqual(len(response.context["driver_list"]), 3)


class ToggleAssignToCarViewTest(BaseTestSetup):
    def setUp(self):
        super().setUp()
        self.user.license_number = "ABC123456"
        self.user.save()

    def test_toggle_assign_to_car_add(self):
        response = self.client.post(reverse(
            "taxi:toggle-car-assign",
            args=[self.car.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.car in self.user.cars.all())

    def test_toggle_assign_to_car_remove(self):
        self.user.cars.add(self.car)
        response = self.client.post(
            reverse(
                "taxi:toggle-car-assign",
                args=[self.car.id])
        )
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertFalse(self.car in self.user.cars.all())
