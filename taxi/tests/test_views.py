from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car


class BaseTestCase(TestCase):
    def setUp(self):
        user = get_user_model()
        self.user = user.objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)


# ---------- Manufacturer CRUD ----------

class ManufacturerCrudTests(BaseTestCase):
    def test_create_manufacturer(self):
        url = reverse("taxi:manufacturer-create")
        data = {"name": "Mazda", "country": "Japan"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Manufacturer.objects.filter(name="Mazda").exists())

    def test_update_manufacturer(self):
        manu = Manufacturer.objects.create(name="BWM", country="Germany")
        url = reverse("taxi:manufacturer-update", args=[manu.pk])

        response = self.client.post(url, {"name": "BMW", "country": "Germany"})

        self.assertEqual(response.status_code, 302)
        manu.refresh_from_db()
        self.assertEqual(manu.name, "BMW")

    def test_delete_manufacturer(self):
        manu = Manufacturer.objects.create(name="Ford", country="USA")
        url = reverse("taxi:manufacturer-delete", args=[manu.pk])

        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Manufacturer.objects.filter(pk=manu.pk).exists())


# ---------- Car CRUD ----------


class CarCrudTests(TestCase):
    def setUp(self):
        user = get_user_model()
        self.user = user.objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

    def test_create_car(self):
        url = reverse("taxi:car-create")
        data = {
            "model": "X5",
            "manufacturer": self.manufacturer.pk,
            "drivers": [self.user.pk],
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Car.objects.filter(
                model="X5",
                manufacturer=self.manufacturer
            ).exists()
        )

    def test_update_car(self):
        car = Car.objects.create(model="X5", manufacturer=self.manufacturer)
        car.drivers.add(self.user)

        url = reverse("taxi:car-update", args=[car.pk])
        data = {
            "model": "X6",
            "manufacturer": self.manufacturer.pk,
            "drivers": [self.user.pk],
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        car.refresh_from_db()
        self.assertEqual(car.model, "X6")

    def test_delete_car(self):
        car = Car.objects.create(model="X5", manufacturer=self.manufacturer)
        url = reverse("taxi:car-delete", args=[car.pk])

        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Car.objects.filter(pk=car.pk).exists())


# ---------- Driver CRUD ----------

class DriverViewsTests(TestCase):
    def setUp(self):
        user = get_user_model()
        self.user = user.objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

    def test_driver_detail(self):
        url = reverse("taxi:driver-detail", args=[self.user.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["driver"], self.user)

    def test_driver_license_update(self):
        url = reverse("taxi:driver-update", args=[self.user.pk])
        data = {"license_number": "XYZ98765"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.license_number, "XYZ98765")


class SearchViewsTests(TestCase):
    def setUp(self):

        user = get_user_model()
        self.user = user.objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

    def test_manufacturer_search_by_name(self):
        m1 = Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Toyota", country="Japan")

        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "bm"})

        manufacturers = list(response.context["manufacturer_list"])
        self.assertEqual(manufacturers, [m1])

    def test_car_search_by_model(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        c1 = Car.objects.create(model="X5", manufacturer=manufacturer)
        Car.objects.create(model="Civic", manufacturer=manufacturer)

        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "x"})

        cars = list(response.context["car_list"])
        self.assertEqual(cars, [c1])

    def test_driver_search_by_username(self):
        user = get_user_model()
        d1 = user.objects.create_user(
            username="alex",
            password="123",
            license_number="AAA11111",
        )
        user.objects.create_user(
            username="maria",
            password="123",
            license_number="BBB22222",
        )

        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "lex"})

        drivers = list(response.context["driver_list"])
        self.assertEqual(drivers, [d1])
