from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import DriverCreationForm, DriverLicenseUpdateForm
from .models import Manufacturer, Car


INDEX_URL = reverse("taxi:index")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test",
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="Test",
            password="<PASSWORD>",
            first_name="test_first",
            last_name="test_last",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test",
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer,
        )

        self.assertEqual(str(car), f"{car.model}")

    def test_create_driver_with_license_number(self):
        username = "test_username"
        password = "test_password"
        license_number = "test_license_number"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )

        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))


class PublicHomePageTest(TestCase):
    def test_login_required(self):
        res = self.client.get(INDEX_URL)
        self.assertNotEqual(res.status_code, 200)


class ManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers_list(self):
        Manufacturer.objects.create(
            name="test_name_1",
            country="test_country_1",
        )
        Manufacturer.objects.create(
            name="test_name_2",
            country="test_country_2",
        )
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(manufacturers),
            list(response.context["manufacturer_list"]),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class CarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_retrieve_cars_list(self):
        manufacturer_1 = Manufacturer.objects.create(
            name="test_name_1",
            country="test_country_1",
        )
        manufacturer_2 = Manufacturer.objects.create(
            name="test_name_2",
            country="test_country_2",
        )
        Car.objects.create(
            model="test_model_1",
            manufacturer=manufacturer_1,
        )
        Car.objects.create(
            model="test_model_2",
            manufacturer=manufacturer_2,
        )
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(cars),
            list(response.context["car_list"]),
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class DriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers_list(self):
        get_user_model().objects.create_user(
            username="test_username_1",
            password="test_password_1",
            license_number="test_license_number_1",
        )
        get_user_model().objects.create_user(
            username="test_username_2",
            password="test_password_2",
            license_number="test_license_number_2",
        )
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(drivers),
            list(response.context["driver_list"]),
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class FormTest(TestCase):

    def test_driver_creation_form(self):
        form_data = {
            "username": "test_username",
            "password1": "test_password",
            "password2": "test_password",
            "license_number": "ABC12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_number_update(self):
        form_data = {
            "license_number": "CBA54321",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.data["license_number"],
            form_data["license_number"]
        )


class ManufacturerSearchViewTest(TestCase):
    def setUp(self):
        self.m1 = Manufacturer.objects.create(name="Toyota", country="Japan")
        self.m2 = Manufacturer.objects.create(name="Ford", country="USA")
        self.m3 = Manufacturer.objects.create(name="Tesla", country="USA")
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_search_returns_filtered_results(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "Tes"})

        self.assertEqual(response.status_code, 200)
        manufacturer_list = response.context["manufacturer_list"]
        self.assertIn(self.m3, manufacturer_list)
        self.assertNotIn(self.m1, manufacturer_list)
        self.assertNotIn(self.m2, manufacturer_list)

    def test_search_empty_returns_all(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        manufacturer_list = response.context["manufacturer_list"]
        self.assertIn(self.m1, manufacturer_list)
        self.assertIn(self.m2, manufacturer_list)
        self.assertIn(self.m3, manufacturer_list)

    def test_search_form_in_context(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "BMW"})

        self.assertEqual(response.status_code, 200)
        search_form = response.context["search_form"]
        self.assertEqual(search_form.initial["name"], "BMW")


class CarSearchViewTest(TestCase):
    def setUp(self):
        self.m1 = Manufacturer.objects.create(name="Toyota", country="Japan")
        self.m2 = Manufacturer.objects.create(name="Ford", country="USA")
        self.m3 = Manufacturer.objects.create(name="Tesla", country="USA")
        self.c1 = Car.objects.create(model="model_1", manufacturer=self.m1)
        self.c2 = Car.objects.create(model="model_2", manufacturer=self.m2)
        self.c3 = Car.objects.create(model="model_3", manufacturer=self.m3)
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_search_returns_filtered_results(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "model_1"})

        self.assertEqual(response.status_code, 200)
        car_list = response.context["car_list"]
        self.assertIn(self.c1, car_list)
        self.assertNotIn(self.c2, car_list)
        self.assertNotIn(self.c3, car_list)

    def test_search_empty_returns_all(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        car_list = response.context["car_list"]
        self.assertIn(self.c1, car_list)
        self.assertIn(self.c2, car_list)
        self.assertIn(self.c3, car_list)

    def test_search_form_in_context(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "model_4"})

        self.assertEqual(response.status_code, 200)
        search_form = response.context["search_form"]
        self.assertEqual(search_form.initial["model"], "model_4")


class DriverSearchViewTest(TestCase):
    def setUp(self):
        self.d1 = get_user_model().objects.create_user(
            username="username_1",
            password="password_1",
            license_number="license_number_1",
        )
        self.d2 = get_user_model().objects.create_user(
            username="username_2",
            password="password_2",
            license_number="license_number_2",
        )
        self.d3 = get_user_model().objects.create_user(
            username="username_3",
            password="password_3",
            license_number="license_number_3",
        )
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_search_returns_filtered_results(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "username_1"})

        self.assertEqual(response.status_code, 200)
        driver_list = response.context["driver_list"]
        self.assertIn(self.d1, driver_list)
        self.assertNotIn(self.d2, driver_list)
        self.assertNotIn(self.d3, driver_list)

    def test_search_empty_returns_all(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        driver_list = response.context["driver_list"]
        self.assertIn(self.d1, driver_list)
        self.assertIn(self.d2, driver_list)
        self.assertIn(self.d3, driver_list)

    def test_search_form_in_context(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "username_4"})

        self.assertEqual(response.status_code, 200)
        search_form = response.context["search_form"]
        self.assertEqual(search_form.initial["username"], "username_4")
