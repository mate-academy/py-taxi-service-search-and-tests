from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Car, Driver, Manufacturer


class IndexViewTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="index_driver",
            password="testpassword",
            license_number="ABC12345",
        )
        self.client.force_login(self.driver)

    def test_index_view_counts_objects_and_visits(self):
        manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA",
        )
        Car.objects.create(
            model="Model S",
            manufacturer=manufacturer,
        )

        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_drivers"], 1)
        self.assertEqual(response.context["num_manufacturers"], 1)
        self.assertEqual(response.context["num_cars"], 1)
        self.assertEqual(response.context["num_visits"], 1)

    def test_index_view_increases_number_of_visits(self):
        self.client.get(reverse("taxi:index"))
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.context["num_visits"], 2)


class SearchViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.driver = Driver.objects.create_user(
            username="search_driver",
            password="testpassword",
            license_number="ABC12345",
        )
        cls.other_driver = Driver.objects.create_user(
            username="another_driver",
            password="testpassword",
            license_number="DEF67890",
        )

        cls.manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA",
        )
        cls.other_manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

        cls.car = Car.objects.create(
            model="Model S",
            manufacturer=cls.manufacturer,
        )
        cls.other_car = Car.objects.create(
            model="Corolla",
            manufacturer=cls.other_manufacturer,
        )

    def setUp(self):
        self.client.force_login(self.driver)

    def test_driver_search_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"name": "SEARCH"},
        )

        self.assertEqual(
            list(response.context["driver_list"]),
            [self.driver],
        )

    def test_car_search_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"name": "model"},
        )

        self.assertEqual(
            list(response.context["car_list"]),
            [self.car],
        )

    def test_manufacturer_search_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "tes"},
        )

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            [self.manufacturer],
        )

    def test_empty_driver_search_returns_all_drivers(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertEqual(response.context["driver_list"].count(), 2)

    def test_empty_car_search_returns_all_cars(self):
        response = self.client.get(reverse("taxi:car-list"))

        self.assertEqual(response.context["car_list"].count(), 2)

    def test_empty_manufacturer_search_returns_all_manufacturers(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(response.context["manufacturer_list"].count(), 2)


class ManufacturerCrudTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="manufacturer_driver",
            password="testpassword",
            license_number="ABC12345",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA",
        )
        self.client.force_login(self.driver)

    def test_create_manufacturer(self):
        response = self.client.post(
            reverse("taxi:manufacturer-create"),
            {
                "name": "BMW",
                "country": "Germany",
            },
        )

        self.assertRedirects(
            response,
            reverse("taxi:manufacturer-list"),
        )
        self.assertTrue(Manufacturer.objects.filter(name="BMW").exists())

    def test_update_manufacturer(self):
        response = self.client.post(
            reverse(
                "taxi:manufacturer-update",
                kwargs={"pk": self.manufacturer.pk},
            ),
            {
                "name": "Tesla Motors",
                "country": "USA",
            },
        )

        self.assertRedirects(
            response,
            reverse("taxi:manufacturer-list"),
        )
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, "Tesla Motors")

    def test_delete_manufacturer(self):
        response = self.client.post(
            reverse(
                "taxi:manufacturer-delete",
                kwargs={"pk": self.manufacturer.pk},
            ),
        )

        self.assertRedirects(
            response,
            reverse("taxi:manufacturer-list"),
        )
        self.assertFalse(
            Manufacturer.objects.filter(pk=self.manufacturer.pk).exists()
        )


class CarCrudAndAssignmentTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="car_driver",
            password="testpassword",
            license_number="ABC12345",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA",
        )
        self.car = Car.objects.create(
            model="Model S",
            manufacturer=self.manufacturer,
        )
        self.client.force_login(self.driver)

    def test_create_car(self):
        response = self.client.post(
            reverse("taxi:car-create"),
            {
                "model": "Model 3",
                "manufacturer": self.manufacturer.pk,
                "drivers": [self.driver.pk],
            },
        )

        self.assertRedirects(response, reverse("taxi:car-list"))
        self.assertTrue(Car.objects.filter(model="Model 3").exists())

    def test_update_car(self):
        response = self.client.post(
            reverse(
                "taxi:car-update",
                kwargs={"pk": self.car.pk},
            ),
            {
                "model": "Model X",
                "manufacturer": self.manufacturer.pk,
                "drivers": [self.driver.pk],
            },
        )

        self.assertRedirects(response, reverse("taxi:car-list"))
        self.car.refresh_from_db()
        self.assertEqual(self.car.model, "Model X")

    def test_delete_car(self):
        response = self.client.post(
            reverse(
                "taxi:car-delete",
                kwargs={"pk": self.car.pk},
            ),
        )

        self.assertRedirects(response, reverse("taxi:car-list"))
        self.assertFalse(Car.objects.filter(pk=self.car.pk).exists())

    def test_assign_driver_to_car(self):
        response = self.client.get(
            reverse(
                "taxi:toggle-car-assign",
                kwargs={"pk": self.car.pk},
            ),
        )

        self.assertRedirects(
            response,
            reverse(
                "taxi:car-detail",
                kwargs={"pk": self.car.pk},
            ),
        )
        self.assertIn(self.driver, self.car.drivers.all())

    def test_unassign_driver_from_car(self):
        self.car.drivers.add(self.driver)

        self.client.get(
            reverse(
                "taxi:toggle-car-assign",
                kwargs={"pk": self.car.pk},
            ),
        )

        self.assertNotIn(self.driver, self.car.drivers.all())


class DriverCrudAndFormTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="main_driver",
            password="testpassword",
            license_number="ABC12345",
        )
        self.client.force_login(self.driver)

    def test_create_driver(self):
        response = self.client.post(
            reverse("taxi:driver-create"),
            {
                "username": "new_driver",
                "password1": "StrongPassword123",
                "password2": "StrongPassword123",
                "license_number": "DEF67890",
                "first_name": "John",
                "last_name": "Smith",
            },
        )

        new_driver = Driver.objects.get(username="new_driver")

        self.assertRedirects(response, new_driver.get_absolute_url())
        self.assertEqual(new_driver.license_number, "DEF67890")

    def test_update_driver_license_number(self):
        response = self.client.post(
            reverse(
                "taxi:driver-update",
                kwargs={"pk": self.driver.pk},
            ),
            {
                "license_number": "XYZ54321",
            },
        )

        self.assertRedirects(response, reverse("taxi:driver-list"))
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.license_number, "XYZ54321")

    def test_delete_driver(self):
        driver_to_delete = Driver.objects.create_user(
            username="delete_driver",
            password="testpassword",
            license_number="DEF67890",
        )

        response = self.client.post(
            reverse(
                "taxi:driver-delete",
                kwargs={"pk": driver_to_delete.pk},
            ),
        )

        self.assertRedirects(response, reverse("taxi:driver-list"))
        self.assertFalse(
            Driver.objects.filter(pk=driver_to_delete.pk).exists()
        )

    def test_driver_creation_form_with_valid_license(self):
        form = DriverCreationForm(
            data={
                "username": "valid_license_driver",
                "password1": "StrongPassword123",
                "password2": "StrongPassword123",
                "license_number": "QWE12345",
            },
        )

        self.assertTrue(form.is_valid())

    def test_driver_creation_form_with_invalid_license(self):
        form = DriverCreationForm(
            data={
                "username": "invalid_license_driver",
                "password1": "StrongPassword123",
                "password2": "StrongPassword123",
                "license_number": "abc123",
            },
        )

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_license_update_form_with_invalid_license(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "ABC123"},
            instance=self.driver,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
