from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy

from taxi.models import Manufacturer, Car, Driver

TestCase.fixtures = ["taxi_service_db_data.json"]


class PublicViewsTest(TestCase):
    def test_index_required(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_list_required(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_cars_list_required(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_driver_list_required(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(response.status_code, 200)


class PrivateHomeTest(TestCase):
    def setUp(self):
        self.client.force_login(get_user_model().objects.get(id=1))

    def test_index(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")

    def test_visit_home_page(self):
        visits = 5

        for visit in range(visits):
            response = self.client.get(reverse("taxi:index"))
            self.assertEqual(response.context["num_visits"], visit + 1)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="TestName", country="TestCountry"
        )

        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

    def test_manufacturer_list(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers[0 : len(
                response.context["manufacturer_list"]
            )]),
        )

    def test_manufacturer_created(self):
        data = {
            "name": "NewTestName",
            "country": "NewTestCountry",
        }
        url = reverse_lazy("taxi:manufacturer-create")
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("taxi:manufacturer-list"))

        manufacturer = Manufacturer.objects.get(name="NewTestName")
        self.assertEqual(manufacturer.name, "NewTestName")
        self.assertEqual(manufacturer.country, "NewTestCountry")

    def test_manufacturer_update(self):
        data = {
            "name": "TestName2",
            "country": "TestCountry2",
        }
        url = reverse_lazy(
            "taxi:manufacturer-update",
            args=[self.manufacturer.pk]
        )
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("taxi:manufacturer-list"))

        manufacturer = Manufacturer.objects.get(pk=self.manufacturer.pk)
        self.assertEqual(manufacturer.name, "TestName2")
        self.assertEqual(manufacturer.country, "TestCountry2")

    def test_manufacturer_delete(self):
        url = reverse_lazy(
            "taxi:manufacturer-delete",
            args=[self.manufacturer.pk]
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse_lazy("taxi:manufacturer-list")
        )

        self.assertFalse(Manufacturer.objects.filter(
            pk=self.manufacturer.pk
        ).exists())


class PrivateCarTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="TestName", country="TestCountry"
        )
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")
        self.car = Car.objects.create(
            model="TestModel",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.user)

    def test_car_list(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

        car = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(car[0 : len(response.context["car_list"])]),
        )

    def test_car_created(self):
        data = {
            "model": "Camry",
            "manufacturer": self.manufacturer.pk,
            "drivers": [self.user.pk],
        }
        url = reverse_lazy("taxi:car-create")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("taxi:car-list"))

        car = Car.objects.get(model="Camry")
        self.assertEqual(car.model, "Camry")
        self.assertEqual(car.manufacturer, self.manufacturer)
        self.assertEqual(list(car.drivers.all()), [self.user])

    def test_car_update(self):
        data = {
            "model": "CAMRY",
            "manufacturer": self.manufacturer.pk,
            "drivers": [self.user.pk],
        }
        url = reverse_lazy("taxi:car-update", args=[self.car.pk])
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("taxi:car-list"))

        car = Car.objects.get(pk=self.car.pk)
        self.assertEqual(car.model, "CAMRY")

    def test_manufacturer_delete(self):
        url = reverse_lazy("taxi:car-delete", args=[self.car.pk])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("taxi:car-list"))

        self.assertFalse(Car.objects.filter(pk=self.car.pk).exists())


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.driver = Driver.objects.create_user(
            username="testdriver",
            password="testpassword",
            first_name="John",
            last_name="Doe",
            license_number="OLD12322",
        )
        self.client.force_login(self.driver)

    def test_driver_list(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers[0 : len(response.context["driver_list"])]),
        )

    def test_driver_created(self):
        data = {
            "username": "driver1",
            "password1": "strongpassword",
            "password2": "strongpassword",
            "first_name": "John",
            "last_name": "Doe",
            "license_number": "ABC12355",
        }

        response = self.client.post(reverse("taxi:driver-create"), data)

        self.assertEqual(response.status_code, 302)

        driver = Driver.objects.get(username="driver1")
        self.assertEqual(driver.username, "driver1")
        self.assertEqual(driver.first_name, "John")
        self.assertEqual(driver.last_name, "Doe")
        self.assertEqual(driver.license_number, "ABC12355")

    def test_driver_license_update(self):
        data = {
            "license_number": "NEW45611",
        }
        url = reverse_lazy("taxi:driver-update", args=[self.driver.pk])
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("taxi:driver-list"))

        updated_driver = Driver.objects.get(pk=self.driver.pk)
        self.assertEqual(updated_driver.license_number, "NEW45611")
