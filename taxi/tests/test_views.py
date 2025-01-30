from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class PublicManufacturerTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.LOGIN_URL = reverse("taxi:index")
        self.MANUFACTURER_LOGIN_URL = reverse("taxi:manufacturer-list")
        self.MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")
        self.MANUFACTURER_UPDATE_URL = reverse(
            "taxi:manufacturer-update",
            args=[self.manufacturer.pk]
        )
        self.MANUFACTURER_DELETE_URL = reverse(
            "taxi:manufacturer-delete",
            args=[self.manufacturer.pk]
        )

    def test_login_index(self):
        result = self.client.get(self.LOGIN_URL)
        self.assertNotEqual(result.status_code, 200)

    def test_login_manufacturer(self):
        result = self.client.get(self.MANUFACTURER_LOGIN_URL)
        self.assertNotEqual(result.status_code, 200)

    def test_create_manufacturer(self):
        result = self.client.get(self.MANUFACTURER_CREATE_URL)
        self.assertNotEqual(result.status_code, 200)

    def test_update_manufacturer(self):
        result = self.client.get(self.MANUFACTURER_UPDATE_URL)
        self.assertNotEqual(result.status_code, 200)

    def test_delete_manufacturer(self):
        result = self.client.get(self.MANUFACTURER_DELETE_URL)
        self.assertNotEqual(result.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Driver",
            password="test123",
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(
            name="Manufacturer",
            country="Country")
        Manufacturer.objects.create(
            name="Manufacturer_next",
            country="Country_next"
        )

    def test_retrieve_manufactures(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        manufactures = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufactures)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PublicCarTest(TestCase):
    def setUp(self):
        manufacturer = Manufacturer.objects.create(
            name="Manufacturer",
            country="Country"
        )
        self.car = Car.objects.create(model="Model", manufacturer=manufacturer)
        self.CAR_LIST_URL = reverse("taxi:car-list")
        self.CAR_LOGIN_DETAIL_URL = reverse(
            "taxi:car-detail",
            args=[self.car.pk]
        )
        self.CAR_CREATE_URL = reverse("taxi:car-create")
        self.CAR_UPDATE_URL = reverse("taxi:car-update", args=[self.car.pk])
        self.CAR_DELETE_URL = reverse("taxi:car-delete", args=[self.car.pk])

    def test_login_car(self):
        result = self.client.get(self.CAR_LIST_URL)
        self.assertNotEqual(result.status_code, 200)

    def test_login_detail_car(self):
        result = self.client.get(self.CAR_LOGIN_DETAIL_URL)
        self.assertNotEqual(result.status_code, 200)

    def test_create_car(self):
        result = self.client.get(self.CAR_CREATE_URL)
        self.assertNotEqual(result.status_code, 200)

    def test_update_car(self):
        result = self.client.get(self.CAR_UPDATE_URL)
        self.assertNotEqual(result.status_code, 200)

    def test_delete_car(self):
        result = self.client.get(self.CAR_DELETE_URL)
        self.assertNotEqual(result.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Driver",
            password="test123",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Manufacturer",
            country="Country"
        )
        self.client.force_login(self.user)
        self.car1 = Car.objects.create(
            model="Model",
            manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="Model_2",
            manufacturer=self.manufacturer
        )

    def test_retrieve_manufactures(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PublicDriverTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="Driver",
            first_name="First",
            last_name="Last",
            license_number="ABC12345"
        )
        self.DRIVER_LIST_URL = reverse(
            "taxi:driver-list"
        )
        self.DRIVER_LOGIN_DETAIL_URL = reverse(
            "taxi:driver-detail",
            args=[self.driver.pk]
        )
        self.DRIVER_CREATE_URL = reverse(
            "taxi:driver-create"
        )
        self.DRIVER_UPDATE_URL = reverse(
            "taxi:driver-update",
            args=[self.driver.pk]
        )
        self.DRIVER_DELETE_URL = reverse(
            "taxi:driver-delete",
            args=[self.driver.pk]
        )

    def test_login_driver(self):
        result = self.client.get(self.DRIVER_LIST_URL)
        self.assertNotEqual(result.status_code, 200)

    def test_login_detail_driver(self):
        result = self.client.get(self.DRIVER_LOGIN_DETAIL_URL)
        self.assertNotEqual(result.status_code, 200)

    def test_create_driver(self):
        result = self.client.get(self.DRIVER_CREATE_URL)
        self.assertNotEqual(result.status_code, 200)

    def test_update_driver(self):
        result = self.client.get(self.DRIVER_UPDATE_URL)
        self.assertNotEqual(result.status_code, 200)

    def test_delete_driver(self):
        result = self.client.get(self.DRIVER_DELETE_URL)
        self.assertNotEqual(result.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Driver",
            password="test123",
            license_number="ABC02345"
        )
        self.client.force_login(self.user)
        self.driver1 = get_user_model().objects.create_user(
            username="Driver1",
            password="test123",
            license_number="ABC12340"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="Driver2",
            password="test123",
            license_number="ABC12346"
        )

    def test_retrieve_drivers(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver1.username)
        self.assertContains(response, self.driver2.username)
        drivers = get_user_model().objects.all()
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")
