from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Manufacturer, Car, Driver
from .forms import DriverCreationForm


DEFAULT_USER_PARAMS = {
    "username": "test",
    "password": "test123",
    "first_name": "John",
    "last_name": "Smith",
    "license_number": "ABC04308",
}


class TestDriverCreationForm(TestCase):
    def setUp(self):
        self.base_driver_dict = {
            "username": "test",
            "password1": "s3cur3 p4ssw0rd",
            "password2": "s3cur3 p4ssw0rd",
        }

    def test_correct_license_number(self):
        self.base_driver_dict["license_number"] = "ABC04308"
        form = DriverCreationForm(self.base_driver_dict)
        self.assertTrue(form.is_valid())

    def test_too_short_license_number(self):
        self.base_driver_dict["license_number"] = "ABC4308"
        form = DriverCreationForm(self.base_driver_dict)
        self.assertFalse(form.is_valid())

    def test_too_long_license_number(self):
        self.base_driver_dict["license_number"] = "ABC043081"
        form = DriverCreationForm(self.base_driver_dict)
        self.assertFalse(form.is_valid())

    def test_numeric_license_number(self):
        self.base_driver_dict["license_number"] = "12345678"
        form = DriverCreationForm(self.base_driver_dict)
        self.assertFalse(form.is_valid())

    def test_license_number_with_two_letters(self):
        self.base_driver_dict["license_number"] = "AB304308"
        form = DriverCreationForm(self.base_driver_dict)
        self.assertFalse(form.is_valid())

    def test_license_number_with_swapped_parts(self):
        self.base_driver_dict["license_number"] = "04308ABC"
        form = DriverCreationForm(self.base_driver_dict)
        self.assertFalse(form.is_valid())

    def test_license_number_with_only_letters(self):
        self.base_driver_dict["license_number"] = "ABCDEFGH"
        form = DriverCreationForm(self.base_driver_dict)
        self.assertFalse(form.is_valid())


class TestModels(TestCase):
    def test_manufacturer_str(self):
        name = "Test"
        country = "Testland"
        manufacturer = Manufacturer.objects.create(name=name, country=country)
        self.assertEqual(str(manufacturer), f"{name} {country}")

    def test_car_str(self):
        model = "Test"
        manufacturer = Manufacturer.objects.create(
            name="Test", country="Testland"
        )
        car = Car.objects.create(model=model, manufacturer=manufacturer)
        self.assertEqual(str(car), model)

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(**DEFAULT_USER_PARAMS)
        self.assertEqual(
            str(driver),
            "{username} ({first_name} {last_name})".format(
                **DEFAULT_USER_PARAMS
            ),
        )


class TestLoginRequired(TestCase):
    def test_index_login_required(self):
        url = reverse("taxi:index")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_list_login_required(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_create_login_required(self):
        url = reverse("taxi:manufacturer-create")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_update_login_required(self):
        manufacturer = Manufacturer.objects.create(
            name="Test", country="Testland"
        )
        url = reverse("taxi:manufacturer-update", args=(manufacturer.id,))
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_delete_login_required(self):
        manufacturer = Manufacturer.objects.create(
            name="Test", country="Testland"
        )
        url = reverse("taxi:manufacturer-delete", args=(manufacturer.id,))
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_car_list_login_required(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_car_detail_login_required(self):
        manufacturer = Manufacturer.objects.create(
            name="Test", country="Testland"
        )
        car = Car.objects.create(model="Test", manufacturer=manufacturer)
        url = reverse("taxi:car-detail", args=(car.id,))
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_car_create_login_required(self):
        url = reverse("taxi:car-create")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_car_update_login_required(self):
        manufacturer = Manufacturer.objects.create(
            name="Test", country="Testland"
        )
        car = Car.objects.create(model="Test", manufacturer=manufacturer)
        url = reverse("taxi:car-update", args=(car.id,))
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_car_delete_login_required(self):
        manufacturer = Manufacturer.objects.create(
            name="Test", country="Testland"
        )
        car = Car.objects.create(model="Test", manufacturer=manufacturer)
        url = reverse("taxi:car-delete", args=(car.id,))
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_car_toggle_assign_login_required(self):
        manufacturer = Manufacturer.objects.create(
            name="Test", country="Testland"
        )
        car = Car.objects.create(model="Test", manufacturer=manufacturer)
        url = reverse("taxi:toggle-car-assign", args=(car.id,))
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_list_login_required(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_detail_login_required(self):
        driver = get_user_model().objects.create_user(**DEFAULT_USER_PARAMS)
        url = reverse("taxi:driver-detail", args=(driver.id,))
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_create_login_required(self):
        url = reverse("taxi:driver-create")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_license_update_login_required(self):
        driver = get_user_model().objects.create_user(**DEFAULT_USER_PARAMS)
        url = reverse("taxi:driver-update", args=(driver.id,))
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_delete_login_required(self):
        driver = get_user_model().objects.create_user(**DEFAULT_USER_PARAMS)
        url = reverse("taxi:driver-delete", args=(driver.id,))
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateTestIndexView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(**DEFAULT_USER_PARAMS)
        self.client.force_login(self.user)

    def test_visit_counter(self):
        url = reverse("taxi:index")
        response = self.client.get(url)
        self.assertContains(response, "1 time.")
        response = self.client.get(url)
        self.assertContains(response, "2 times.")


class PrivateTestManufacturerListView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(**DEFAULT_USER_PARAMS)
        self.client.force_login(self.user)

    def test_search(self):
        name1 = "Abc"
        name2 = "Def"
        country = "Testland"
        Manufacturer.objects.create(name=name1, country=country)
        Manufacturer.objects.create(name=name2, country=country)
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "a"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, name1)
        self.assertNotContains(response, name2)


class PrivateTestCarListView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(**DEFAULT_USER_PARAMS)
        self.client.force_login(self.user)

    def test_search(self):
        model1 = "Abc"
        model2 = "Def"
        manufacturer = Manufacturer.objects.create(
            name="Test", country="Testland"
        )
        Car.objects.create(model=model1, manufacturer=manufacturer)
        Car.objects.create(model=model2, manufacturer=manufacturer)
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "a"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, model1)
        self.assertNotContains(response, model2)


class PrivateTestDriverListView(TestCase):
    def setUp(self):
        self.username1 = DEFAULT_USER_PARAMS["username"]
        self.username2 = "kate"
        self.user1 = get_user_model().objects.create_user(
            **DEFAULT_USER_PARAMS
        )
        self.user2 = get_user_model().objects.create_user(
            username="kate",
            password="test123",
            first_name="Kate",
            last_name="Black",
            license_number="KBA11312",
        )
        self.client.force_login(self.user1)

    def test_search(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "es"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.username1)
        self.assertNotContains(response, self.username2)


class PrivateTestToggleAssignToCarView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(**DEFAULT_USER_PARAMS)
        self.client.force_login(self.user)

    def test_can_toggle_driver_to_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Test", country="Testland"
        )
        car = Car.objects.create(model="Test", manufacturer=manufacturer)
        url = reverse("taxi:toggle-car-assign", args=(car.id,))
        self.client.get(url)
        self.assertIn(car, self.user.cars.all())
        self.client.get(url)
        self.assertNotIn(car, self.user.cars.all())
