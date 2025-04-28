from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car, Driver


class PublicIndexViewTests(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertNotEqual(response.status_code, 200)


class PrivateIndexViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.login(username="testuser", password="testpass")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertTemplateUsed(response, "taxi/index.html")

    def test_index_counts(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Car.objects.create(
            model="X5",
            manufacturer=Manufacturer.objects.first()
        )
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.context["num_manufacturers"], 1)
        self.assertEqual(response.context["num_cars"], 1)
        self.assertEqual(response.context["num_drivers"], 1)


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser2", password="testpass2"
        )
        self.client.login(username="testuser2", password="testpass2")
        self.manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )

    def test_manufacturer_list_view(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Audi")

    def test_manufacturer_create_view(self):
        response = self.client.post(
            reverse("taxi:manufacturer-create"),
            {"name": "Tesla", "country": "USA"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Manufacturer.objects.filter(name="Tesla").exists())

    def test_manufacturer_update_view(self):
        response = self.client.post(
            reverse("taxi:manufacturer-update", args=[self.manufacturer.id]),
            {"name": "Audi Updated", "country": "Germany"},
        )
        self.assertEqual(response.status_code, 302)
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, "Audi Updated")

    def test_manufacturer_delete_view(self):
        response = self.client.post(
            reverse("taxi:manufacturer-delete", args=[self.manufacturer.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Manufacturer.objects.filter(id=self.manufacturer.id).exists()
        )


class PrivateCarTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser3",
            password="testpass3",
            license_number="ABC12345"
        )
        self.client.login(username="testuser3", password="testpass3")
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )

    def test_car_list_view(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")

    def test_car_detail_view(self):
        response = self.client.get(
            reverse("taxi:car-detail", args=[self.car.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")

    def test_car_create_view(self):
        response = self.client.post(
            reverse("taxi:car-create"),
            {
                "model": "Camry",
                "manufacturer": self.manufacturer.id,
                "drivers": [self.user.id]
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_car_update_view(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")

    def test_car_delete_view(self):
        response = self.client.post(
            reverse("taxi:car-delete", args=[self.car.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Car.objects.filter(id=self.car.id).exists())


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser4",
            password="testpass4",
            license_number="ABC12345"
        )
        self.client.login(username="testuser4", password="testpass4")
        self.driver = Driver.objects.create_user(
            username="driver2", password="pass12345", license_number="DEF67890"
        )

    def test_driver_list_view(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver2")

    def test_driver_detail_view(self):
        response = self.client.get(
            reverse("taxi:driver-detail", args=[self.driver.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver2")

    def test_driver_create_view(self):
        response = self.client.post(
            reverse("taxi:driver-create"),
            {
                "username": "newdriver",
                "password1": "Testpass123",
                "password2": "Testpass123",
                "license_number": "XYZ12345",
                "first_name": "New",
                "last_name": "Driver",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Driver.objects.filter(username="newdriver").exists())

    def test_driver_update_license_view(self):
        response = self.client.post(
            reverse("taxi:driver-update", args=[self.driver.id]),
            {"license_number": "GHI12345"},
        )
        self.assertEqual(response.status_code, 302)
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.license_number, "GHI12345")


class ToggleAssignToCarViewTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="testdriver",
            password="testdriverpass",
            license_number="JKL12345"
        )
        self.car = Car.objects.create(
            model="Supra",
            manufacturer=Manufacturer.objects.create(
                name="Toyota", country="Japan"
            ),
        )
        self.client.login(username="testdriver", password="testdriverpass")

    def test_toggle_assign_to_car(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car.id])

        response = self.client.post(url)
        self.assertRedirects(
            response,
            reverse("taxi:car-detail", args=[self.car.id])
        )
        self.assertTrue(self.car in self.driver.cars.all())

        response = self.client.post(url)
        self.assertRedirects(
            response,
            reverse("taxi:car-detail", args=[self.car.id]))
        self.assertFalse(self.car in self.driver.cars.all())
