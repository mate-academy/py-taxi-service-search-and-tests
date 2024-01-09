from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

URL_MANUFACTURER_LIST = reverse("taxi:manufacturer-list")
URL_MANUFACTURER_CREATE = reverse("taxi:manufacturer-create")
URL_CAR_LIST = reverse("taxi:car-list")
URL_DRIVER_LIST = reverse("taxi:driver-list")


class PublicManufacturerViewTests(TestCase):
    def test_login_required(self):
        response = self.client.get(URL_MANUFACTURER_LIST)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_admin",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_retrieve_all_manufacturers(self):
        Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        response = self.client.get(URL_MANUFACTURER_LIST)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class ManufacturerSearchTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test_admin",
            password="test_password"
        )
        self.client.force_login(self.user)

        Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        Manufacturer.objects.create(
            name="Mercedes-Benz",
            country="Germany"
        )

    def test_search_manufacturers(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "Mercedes-Benz"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mercedes-Benz")
        self.assertNotContains(response, "Audi")
        self.assertNotContains(response, "BMW")


class ManufacturerCreateViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="serhii_b",
            password="test_pass",
        )
        self.client.force_login(self.user)

    def test_manufacturer_create_view(self):
        data = {
           "name": "Mercedes-Benz",
           "country": "Germany"
        }
        url = reverse("taxi:manufacturer-create")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Manufacturer.objects.filter(name="Mercedes-Benz").exists()
        )
        self.assertRedirects(
            response,
            reverse("taxi:manufacturer-list")
        )


class ManufacturerUpdateViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password",
        )
        self.client.force_login(self.user)

        self.manufacturer_test_update = Manufacturer.objects.create(
            name="BMW",
            country="USA"
        )

    def test_manufacturer_update_view(self):
        update_manufacturer = {
            "name": "Mercedes-Benz",
            "country": "Germany",
        }
        url = reverse("taxi:manufacturer-update", kwargs={"pk": self.manufacturer_test_update.id})
        response = self.client.post(url, data=update_manufacturer)

        self.assertEqual(response.status_code, 302)

        self.manufacturer_test_update.refresh_from_db()

        self.assertEqual(self.manufacturer_test_update.name, "BMW")
        self.assertEqual(self.manufacturer_test_update.country, "Germany")

        self.assertRedirects(
            response,
            reverse("taxi:manufacturer-list")
        )


class ManufacturerDeleteViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password",
        )
        self.client.force_login(self.user)

        self.manufacturer_test_delete = Manufacturer.objects.create(
            name="Mercedes-Benz",
            country="Germany"
        )

    def test_manufacturer_delete_view(self):
        url = reverse("taxi:manufacturer-delete", kwargs={"pk": self.manufacturer_test_delete.id})
        count_manufacturer_before_delete = Manufacturer.objects.count()
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)

        self.assertEqual(Manufacturer.objects.count(), count_manufacturer_before_delete - 1)

        self.assertFalse(Manufacturer.objects.filter(pk=self.manufacturer_test_delete.id).exists())
        self.assertRedirects(
            response,
            reverse("taxi:manufacturer-list")
        )


class PublicCarTest(TestCase):
    def test_login_required(self):
        response = self.client.get(URL_CAR_LIST)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_admin",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_retrieve_all_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        Car.objects.create(
            model="M5 F90",
            manufacturer=manufacturer
        )

        response = self.client.get(URL_CAR_LIST)
        self.assertEqual(response.status_code, 200)
        list_of_cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(list_of_cars)
        )
        self.assertTemplateUsed(
            response, "taxi/car_list.html"
        )


class CarSearchTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password"
        )
        self.client.force_login(self.user)

        manufacturer_test1 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        Car.objects.create(
            model="M5 F90",
            manufacturer=manufacturer_test1
        )
        manufacturer_test2 = Manufacturer.objects.create(
            name="Mercedes-Benz",
            country="Germany"
        )
        Car.objects.create(
            model="E63S AMG",
            manufacturer=manufacturer_test2
        )

    def test_car_search(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "M5"})
        self.assertContains(response, "M5 F90")
        self.assertNotContains(response, "E63S AMG")


class PublicDriverTests(TestCase):
    def test_login_required(self):
        response = self.client.get(URL_DRIVER_LIST)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_admin",
            password="test_password",
        )

        self.client.force_login(self.user)

    def test_retrieve_all_drivers(self):
        response = self.client.get(URL_DRIVER_LIST)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(
            response, "taxi/driver_list.html")


class DriverSearchTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_admin",
            password="test_password"
        )
        self.client.force_login(self.user)

        Driver.objects.create(
            username="serhii_driver1",
            password="test_password1",
            license_number="ABC11111"
        )
        Driver.objects.create(
            username="test_user1",
            password="test_password2",
            license_number="ABC22222"
        )
        Driver.objects.create(
            username="driver_test3",
            password="test_password3",
            license_number="ABC33333"
        )

    def test_driver_search(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "serhii"})
        self.assertContains(response, "serhii_driver1")
        self.assertNotContains(response, "test_user1")
        self.assertNotContains(response, "driver_test3")
