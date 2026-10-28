from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer, Driver, Car

DRIVER_LIST_URL = reverse("taxi:driver-list")
CAR_LIST_URL = reverse("taxi:car-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
INDEX_URL = reverse("taxi:index")


class ModelsTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.driver = get_user_model().objects.create_user(
            username="testdriver",
            password="test12345",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345",
        )
        self.car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer,
        )

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
        self.assertEqual(str(self.car), self.car.model)

    def test_driver_get_absolute_url(self):
        self.assertEqual(
            self.driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": self.driver.pk}),
        )


class DriverFormsTests(TestCase):
    def test_driver_creation_form_valid_license(self):
        form_data = {
            "username": "newdriver",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
            "license_number": "ABC12345",
            "first_name": "Jane",
            "last_name": "Smith",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_license_wrong_length(self):
        form_data = {
            "username": "newdriver",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
            "license_number": "ABC1234",
            "first_name": "Jane",
            "last_name": "Smith",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_creation_form_license_not_uppercase(self):
        form_data = {
            "username": "newdriver",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
            "license_number": "abc12345",
            "first_name": "Jane",
            "last_name": "Smith",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_creation_form_license_last_not_digits(self):
        form_data = {
            "username": "newdriver",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
            "license_number": "ABCDEFGH",
            "first_name": "Jane",
            "last_name": "Smith",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_license_update_form_valid(self):
        form = DriverLicenseUpdateForm(data={"license_number": "XYZ98765"})
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid_length(self):
        form = DriverLicenseUpdateForm(data={"license_number": "XY98765"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_license_update_form_not_uppercase(self):
        form = DriverLicenseUpdateForm(data={"license_number": "xyz98765"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_license_update_form_last_not_digits(self):
        form = DriverLicenseUpdateForm(data={"license_number": "XYZABCDE"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class LoginRequiredTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.manufacturer = Manufacturer.objects.create(
            name="Honda",
            country="Japan",
        )
        self.driver = get_user_model().objects.create_user(
            username="driver1",
            password="test12345",
            license_number="ABC12345",
        )
        self.car = Car.objects.create(
            model="Civic",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)

    def test_index_login_required(self):
        response = self.client.get(INDEX_URL)
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_driver_list_login_required(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_car_list_login_required(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_manufacturer_list_login_required(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_driver_detail_login_required(self):
        url = reverse("taxi:driver-detail", args=[self.driver.id])
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_car_detail_login_required(self):
        url = reverse("taxi:car-detail", args=[self.car.id])
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_driver_create_login_required(self):
        response = self.client.get(reverse("taxi:driver-create"))
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_car_create_login_required(self):
        response = self.client.get(reverse("taxi:car-create"))
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_manufacturer_create_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_toggle_assign_login_required(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car.id])
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(response.url.startswith("/accounts/login/"))


class AuthenticatedViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="authuser",
            password="test12345",
            license_number="ABC12345",
            first_name="Auth",
            last_name="User",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        self.car = Car.objects.create(
            model="X5",
            manufacturer=self.manufacturer,
        )

    def test_index_status_code(self):
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.status_code, 200)

    def test_index_context_counts(self):
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.context["num_drivers"], 1)
        self.assertEqual(response.context["num_cars"], 1)
        self.assertEqual(response.context["num_manufacturers"], 1)

    def test_index_num_visits_increments(self):
        response1 = self.client.get(INDEX_URL)
        self.assertEqual(response1.context["num_visits"], 1)
        response2 = self.client.get(INDEX_URL)
        self.assertEqual(response2.context["num_visits"], 2)

    def test_driver_list_status_code(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_car_list_status_code(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_list_status_code(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_driver_detail_status_code(self):
        url = reverse("taxi:driver-detail", args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_car_detail_status_code(self):
        url = reverse("taxi:car-detail", args=[self.car.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class DriverSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="test12345",
            license_number="AAA11111",
        )
        self.client.force_login(self.user)
        get_user_model().objects.create_user(
            username="alice",
            password="test12345",
            license_number="BBB22222",
        )
        get_user_model().objects.create_user(
            username="bob",
            password="test12345",
            license_number="CCC33333",
        )
        get_user_model().objects.create_user(
            username="alicia",
            password="test12345",
            license_number="DDD44444",
        )

    def test_search_by_username_partial(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "ali"})
        self.assertEqual(response.status_code, 200)
        drivers = list(response.context["driver_list"])
        usernames = [driver.username for driver in drivers]
        self.assertIn("alice", usernames)
        self.assertIn("alicia", usernames)
        self.assertNotIn("bob", usernames)

    def test_search_by_username_case_insensitive(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "BOB"})
        drivers = list(response.context["driver_list"])
        self.assertEqual(len(drivers), 1)
        self.assertEqual(drivers[0].username, "bob")

    def test_search_empty_returns_all(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": ""})
        self.assertEqual(len(response.context["driver_list"]), 4)

    def test_search_no_match(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "zzz"})
        self.assertEqual(len(response.context["driver_list"]), 0)


class CarSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="test12345",
            license_number="AAA11111",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        Car.objects.create(model="Camry", manufacturer=self.manufacturer)
        Car.objects.create(model="Corolla", manufacturer=self.manufacturer)
        Car.objects.create(model="Prius", manufacturer=self.manufacturer)

    def test_search_by_model_partial(self):
        response = self.client.get(CAR_LIST_URL, {"model": "Co"})
        cars = list(response.context["car_list"])
        models = [car.model for car in cars]
        self.assertIn("Corolla", models)
        self.assertNotIn("Camry", models)
        self.assertNotIn("Prius", models)

    def test_search_by_model_case_insensitive(self):
        response = self.client.get(CAR_LIST_URL, {"model": "camry"})
        cars = list(response.context["car_list"])
        self.assertEqual(len(cars), 1)
        self.assertEqual(cars[0].model, "Camry")

    def test_search_empty_returns_all(self):
        response = self.client.get(CAR_LIST_URL, {"model": ""})
        self.assertEqual(len(response.context["car_list"]), 3)

    def test_search_no_match(self):
        response = self.client.get(CAR_LIST_URL, {"model": "Tesla"})
        self.assertEqual(len(response.context["car_list"]), 0)

    def test_car_list_has_manufacturer(self):
        response = self.client.get(CAR_LIST_URL)
        for car in response.context["car_list"]:
            self.assertEqual(car.manufacturer.name, "Toyota")


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="test12345",
            license_number="AAA11111",
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Tesla", country="USA")
        Manufacturer.objects.create(name="BMW", country="Germany")

    def test_search_by_name_partial(self):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": "Te"})
        manufacturers = list(response.context["manufacturer_list"])
        names = [item.name for item in manufacturers]
        self.assertIn("Tesla", names)
        self.assertNotIn("Toyota", names)
        self.assertNotIn("BMW", names)

    def test_search_by_name_case_insensitive(self):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": "bmw"})
        manufacturers = list(response.context["manufacturer_list"])
        self.assertEqual(len(manufacturers), 1)
        self.assertEqual(manufacturers[0].name, "BMW")

    def test_search_empty_returns_all(self):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": ""})
        self.assertEqual(len(response.context["manufacturer_list"]), 3)

    def test_search_no_match(self):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": "Ford"})
        self.assertEqual(len(response.context["manufacturer_list"]), 0)


class ToggleAssignToCarTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="test12345",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany",
        )
        self.car = Car.objects.create(
            model="A4",
            manufacturer=self.manufacturer,
        )

    def test_toggle_assign_adds_driver(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car.id])
        response = self.client.get(url)
        self.assertRedirects(
            response,
            reverse("taxi:car-detail", args=[self.car.id]),
        )
        self.assertIn(self.user, self.car.drivers.all())

    def test_toggle_assign_removes_driver(self):
        self.car.drivers.add(self.user)
        url = reverse("taxi:toggle-car-assign", args=[self.car.id])
        response = self.client.get(url)
        self.assertRedirects(
            response,
            reverse("taxi:car-detail", args=[self.car.id]),
        )
        self.assertNotIn(self.user, self.car.drivers.all())


class DriverDeleteTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="test12345",
            license_number="AAA11111",
        )
        self.client.force_login(self.user)
        self.driver = get_user_model().objects.create_user(
            username="todelete",
            password="test12345",
            license_number="BBB22222",
        )

    def test_driver_delete_redirects_to_list(self):
        url = reverse("taxi:driver-delete", args=[self.driver.id])
        response = self.client.post(url)
        self.assertRedirects(response, DRIVER_LIST_URL)
        self.assertFalse(
            get_user_model().objects.filter(id=self.driver.id).exists()
        )
