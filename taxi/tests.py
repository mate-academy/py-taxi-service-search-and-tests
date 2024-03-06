from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import (
    DriverCreationForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm,
)
from taxi.models import Manufacturer, Car, Driver


INDEX_URL = reverse("taxi:index")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class ModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test", country="TestCountry"
        )
        self.driver = get_user_model().objects.create(
            username="Username",
            first_name="FirstName",
            last_name="LastName",
            license_number="AAA12345",
            email="testemail@gmail.com",
            password="test123",
        )
        self.car = Car.objects.create(
            model="Model",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}",
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})",
        )

    def test_car_str(self):
        self.assertEqual(str(self.car), "Model")


class AdminTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="admin123"
        )
        self.client.force_login(self.admin_user)
        self.driver = Driver.objects.create_user(
            username="driver",
            password="driver123",
            license_number="AAA12345",
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)


class FormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="new_user",
            password="user123user",
            first_name="Test first",
            last_name="Test last",
            license_number="AAA12345",
        )
        self.client.force_login(self.user)

    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user123user",
            "password2": "user123user",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "AAA12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_update_license_number_with_valid_data(self):
        new_license_number = "BBB11111"
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.id}),
            data={"license_number": new_license_number},
        )
        self.assertEqual(response.status_code, 302)

    def test_update_license_number_with_invalid_data(self):
        new_license_number = "00000QWE"
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.id}),
            data={"license_number": new_license_number},
        )
        self.assertEqual(response.status_code, 200)


class PublicViewTest(TestCase):
    def test_index(self):
        res = self.client.get(INDEX_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_manufacturer_list(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_car_list(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_driver_list(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Username",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(name="TestM", country="USA")
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)


class SearchFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(username="testuser", password="12345")
        cls.create_test_data()

    @classmethod
    def create_test_data(cls):
        Driver.objects.create(
            username="testuser1",
            first_name="John",
            last_name="Doe",
            license_number="ABC123",
        )
        Driver.objects.create(
            username="testuser2",
            first_name="Jane",
            last_name="Smith",
            license_number="DEF456",
        )
        Manufacturer.objects.create(
            name="Test Manufacturer 1", country="Test Country 1"
        )
        Manufacturer.objects.create(
            name="Test Manufacturer 2", country="Test Country 2"
        )
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="Test Country"
        )
        Car.objects.create(model="Test Model 1", manufacturer=manufacturer)
        Car.objects.create(model="Test Model 2", manufacturer=manufacturer)

    def setUp(self):
        self.client.login(username="testuser", password="12345")

    def test_driver_search_form(self):
        form = DriverSearchForm(data={"username": "test_user"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "test_user")

    def test_search_driver_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "testuser1"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser1")

    def test_car_search_form(self):
        form = CarSearchForm(data={"model": "test_model"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "test_model")

    def test_manufacturer_search_form(self):
        form = ManufacturerSearchForm(data={"name": "test_name"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "test_name")

    def test_manufacturer_list_display_correctly(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertContains(response, "Test Manufacturer 1")
        self.assertContains(response, "Test Manufacturer 2")

    def test_car_list_display_correctly(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertContains(response, "Test Model 1")
        self.assertContains(response, "Test Model 2")
