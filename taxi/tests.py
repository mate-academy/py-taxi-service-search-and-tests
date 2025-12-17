from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Driver, Car, Manufacturer

User = get_user_model()


class DriverTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="test_driver",
            password="12345",
            license_number="ABC12345",
        )
        self.client.force_login(self.driver)

    def test_driver_list_search(self):
        self.driver = Driver.objects.create_user(
            username="driver123",
            password="12345",
            license_number="ABC22222",
        )

        response = self.client.get(reverse("taxi:driver-list")
                                   + "?q=driver123")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver123")

        response = self.client.get(reverse("taxi:driver-list")
                                   + "?q=nonexistent")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "driver123")

    def test_driver_create(self):
        response = self.client.post(
            reverse("taxi:driver-create"),
            {
                "username": "newdriver",
                "license_number": "XYZ12345",
                "password1": "complexpassword",
                "password2": "complexpassword",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Driver.objects.filter(username="newdriver").exists())

    def test_driver_update(self):
        driver = Driver.objects.create_user(
            username="upd_driver",
            password="12345",
            license_number="OLD123",
        )
        response = self.client.post(
            reverse("taxi:driver-update", args=[driver.id]),
            {"license_number": "NEW12345"},
        )
        self.assertEqual(response.status_code, 302)
        driver.refresh_from_db()
        self.assertEqual(driver.license_number, "NEW12345")

    def test_driver_delete(self):
        driver = Driver.objects.create_user(
            username="del_driver",
            password="12345",
            license_number="DEL123",
        )
        response = self.client.post(
            reverse("taxi:driver-delete", args=[driver.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Driver.objects.filter(id=driver.id).exists())


class CarTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="TestManu",
            country="TestCountry",
        )
        self.driver = Driver.objects.create_user(
            username="driver2",
            password="12345",
            license_number="DEF45678",
        )
        self.client.force_login(self.driver)

    def test_car_list_search(self):
        car = Car.objects.create(
            model="ModelX",
            manufacturer=self.manufacturer,
        )
        car.drivers.add(self.driver)

        response = self.client.get(reverse("taxi:car-list") + "?q=ModelX")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ModelX")

        response = self.client.get(reverse("taxi:car-list") + "?q=Unknown")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "ModelX")

    def test_car_create(self):
        response = self.client.post(
            reverse("taxi:car-create"),
            {
                "model": "NewCar",
                "manufacturer": self.manufacturer.id,
                "drivers": [self.driver.id],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Car.objects.filter(model="NewCar").exists())

    def test_car_update(self):
        car = Car.objects.create(
            model="OldCar",
            manufacturer=self.manufacturer,
        )
        car.drivers.add(self.driver)

        response = self.client.post(
            reverse("taxi:car-update", args=[car.id]),
            {
                "model": "UpdatedCar",
                "manufacturer": self.manufacturer.id,
                "drivers": [self.driver.id],
            },
        )
        self.assertEqual(response.status_code, 302)
        car.refresh_from_db()
        self.assertEqual(car.model, "UpdatedCar")

    def test_car_delete(self):
        car = Car.objects.create(
            model="DelCar",
            manufacturer=self.manufacturer,
        )
        car.drivers.add(self.driver)

        response = self.client.post(
            reverse("taxi:car-delete", args=[car.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Car.objects.filter(id=car.id).exists())


class ManufacturerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_admin",
            password="12345",
        )
        self.client.force_login(self.user)

    def test_manufacturer_list_search(self):
        Manufacturer.objects.create(name="Manu1", country="Country1")

        response = self.client.get(reverse("taxi:manufacturer-list")
                                   + "?q=Manu1")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Manu1")

        response = self.client.get(reverse("taxi:manufacturer-list")
                                   + "?q=Unknown")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Manu1")

    def test_manufacturer_create(self):
        response = self.client.post(
            reverse("taxi:manufacturer-create"),
            {"name": "Capsule Corp", "country": "DBZ"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Manufacturer.objects.filter(name="Capsule Corp").exists()
        )

    def test_manufacturer_update(self):
        manu = Manufacturer.objects.create(
            name="Capsule Corp",
            country="DBZ",
        )

        response = self.client.post(
            reverse("taxi:manufacturer-update", args=[manu.id]),
            {"name": "Capsule Corporation", "country": "DBZ"},
        )
        self.assertEqual(response.status_code, 302)
        manu.refresh_from_db()
        self.assertEqual(manu.name, "Capsule Corporation")

    def test_manufacturer_delete(self):
        manu = Manufacturer.objects.create(
            name="Capsule Corp",
            country="DBZ",
        )

        response = self.client.post(
            reverse("taxi:manufacturer-delete", args=[manu.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Manufacturer.objects.filter(id=manu.id).exists()
        )
