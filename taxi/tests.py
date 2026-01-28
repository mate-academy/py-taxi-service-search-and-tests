from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverLicenseUpdateForm
from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self):
        password = "test123"
        driver = get_user_model().objects.create_user(
            username="test",
            password=password,
            first_name="test_first",
            last_name="test_last",
            license_number="test_license",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} "
            f"({driver.first_name} {driver.last_name})"
        )
        self.assertTrue(driver.check_password(password))

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        car = Car.objects.create(model="Camry", manufacturer=manufacturer)
        self.assertEqual(str(car), str(car.model))


CAR_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        user = get_user_model()
        self.user = user.objects.create_user(
            username="test",
            password="test12345",
            license_number="TES12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        Car.objects.create(model="lexus", manufacturer=manufacturer)
        Car.objects.create(model="audi", manufacturer=manufacturer)
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)


class FormTest(TestCase):
    def test_license_form_valid(self):
        form_data = {"license_number": "ABG12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_license_form_invalid(self):
        form_data = {"license_number": "ab123"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())


class FilterListTest(TestCase):
    def setUp(self) -> None:
        user = get_user_model()
        self.user = user.objects.create_user(
            username="notshowed2",
            password="test16790",
            license_number="TES76548",
        )
        self.client.force_login(self.user)

    def test_driver_filter_list(self):
        driver1 = get_user_model().objects.create_user(
            username="test1",
            password="test12345",
            license_number="TES12345",
        )
        driver2 = get_user_model().objects.create_user(
            username="notshowed",
            password="test67890",
            license_number="EST12345",
        )
        driver3 = get_user_model().objects.create_user(
            username="test3",
            password="test09876",
            license_number="SET12345",
        )
        response = self.client.get(reverse("taxi:driver-list"), {"username": "test"})
        resp_list = response.context["driver_list"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(resp_list), 2)
        self.assertIn(driver1, resp_list)
        self.assertIn(driver3, resp_list)
        self.assertNotIn(driver2, resp_list)

    def test_manufacturer_filter_list(self):
        manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Skoda",
            country="Ukraine"
        )
        manufacturer3 = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        response = self.client.get(reverse("taxi:manufacturer-list"), {"name": "t"})
        resp_list = response.context["manufacturer_list"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(resp_list), 2)
        self.assertContains(response, manufacturer1.name)
        self.assertContains(response, manufacturer3.name)
        self.assertNotContains(response, manufacturer2.name)

    def test_car_filter_list(self):
        manufacturer = Manufacturer.objects.create(
            name="John",
            country="Japan"
        )
        car1 = Car.objects.create(
            model="Camry",
            manufacturer=manufacturer,
        )
        car2 = Car.objects.create(
            model="Camry89",
            manufacturer=manufacturer,
        )
        car3 = Car.objects.create(
            model="Toyota",
            manufacturer=manufacturer,
        )
        response = self.client.get(reverse("taxi:car-list"), {"model": "camry"})
        resp_list = response.context["car_list"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(resp_list), 2)
        self.assertIn(car1, resp_list)
        self.assertIn(car2, resp_list)
        self.assertNotIn(car3, resp_list)
