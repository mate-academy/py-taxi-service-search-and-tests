from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Car, Manufacturer
from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm

User = get_user_model()


class DriverCreationFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            "username": "driver1",
            "password1": "testpass123",
            "password2": "testpass123",
            "license_number": "ABC12345",
            "first_name": "Ivan",
            "last_name": "Ivanov",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_license_number(self):
        form_data = {
            "username": "driver2",
            "password1": "testpass123",
            "password2": "testpass123",
            "license_number": "abc12345",
            "first_name": "Ivan",
            "last_name": "Ivanov",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user3",
            password="pass",
            license_number="ABC12345"
        )

    def test_valid_license(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "DEF67890"},
            instance=self.user
        )
        self.assertTrue(form.is_valid())

    def test_invalid_license(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "123"},
            instance=self.user
        )
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            license_number="ABC12345"
        )
        self.client = Client()
        self.client.login(username="testuser", password="testpass")

        Manufacturer.objects.create(name="TestMan", country="Japan")
        Manufacturer.objects.create(name="AnotherMan", country="Japan")

    def test_search_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "TestMan"}
        )
        self.assertContains(response, "TestMan")
        self.assertNotContains(response, "AnotherMan")

    def test_search_by_part_of_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Test"}
        )
        self.assertContains(response, "TestMan")
        self.assertNotContains(response, "AnotherMan")

    def test_key_insensitive_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "TESTMAN"}
        )
        self.assertContains(response, "TestMan")
        self.assertNotContains(response, "AnotherMan")


class CarListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            license_number="ABC12345"
        )
        self.client = Client()
        self.client.login(username="testuser", password="testpass")
        man = Manufacturer.objects.create(name="TestMan", country="UA")

        Car.objects.create(model="TestCar", manufacturer=man)
        Car.objects.create(model="OtherCar", manufacturer=man)

    def test_search_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "TestCar"}
        )
        self.assertContains(response, "TestCar")
        self.assertNotContains(response, "OtherCar")

    def test_search_by_part_of_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Car"}
        )
        self.assertContains(response, "TestCar")
        self.assertContains(response, "OtherCar")

    def test_key_insensitive_search(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "TEST"}
        )
        self.assertContains(response, "TestCar")
        self.assertNotContains(response, "OtherCar")


class DriverListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            license_number="ABC12345"
        )
        self.client = Client()
        self.client.login(username="testuser", password="testpass")

        User.objects.create_user(
            username="driver1",
            password="pass",
            license_number="DEF67890"
        )
        User.objects.create_user(
            username="driver2",
            password="pass",
            license_number="GHI12345"
        )

    def test_search_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "driver1"}
        )
        self.assertContains(response, "driver1")
        self.assertNotContains(response, "driver2")

    def test_search_by_part_of_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "dri"}
        )
        self.assertContains(response, "driver1")
        self.assertContains(response, "driver2")

    def test_key_insensitive_search(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "DRIVER1"}
        )
        self.assertContains(response, "driver1")
        self.assertNotContains(response, "driver2")


class ToggleAssignToCarViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            license_number="ABC12345"
        )
        self.client = Client()
        self.client.login(username="testuser", password="testpass")

        self.manufacturer = Manufacturer.objects.create(
            name="TestMan",
            country="UA"
        )
        self.car = Car.objects.create(
            model="TestCar",
            manufacturer=self.manufacturer
        )

    def test_toggle_assign_adds_and_removes(self):
        # Add
        self.client.post(reverse("taxi:toggle-car-assign", args=[self.car.id]))
        self.user.refresh_from_db()
        self.assertIn(self.car, self.user.cars.all())
        # Remove
        self.client.post(reverse("taxi:toggle-car-assign", args=[self.car.id]))
        self.user.refresh_from_db()
        self.assertNotIn(self.car, self.user.cars.all())


class IndexViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            license_number="ABC12345"
        )
        self.client = Client()
        self.client.login(username="testuser", password="testpass")

        man1, man2, man3 = Manufacturer.objects.bulk_create((
            Manufacturer(name="TestMan1", country="UA"),
            Manufacturer(name="TestMan2", country="UA"),
            Manufacturer(name="TestMan3", country="UA"),
        ))
        Car.objects.bulk_create((
            Car(model="TestCar1", manufacturer=man1),
            Car(model="TestCar2", manufacturer=man2),
            Car(model="TestCar3", manufacturer=man3),
            Car(model="TestCar4", manufacturer=man2),
            Car(model="TestCar5", manufacturer=man1),
        ))

    def test_index_view_counts_and_visits(self):
        url = reverse("taxi:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_drivers"], User.objects.count())
        self.assertEqual(response.context["num_cars"], Car.objects.count())
        self.assertEqual(
            response.context["num_manufacturers"],
            Manufacturer.objects.count()
        )
        self.assertEqual(response.context["num_visits"], 1)

        response2 = self.client.get(url)
        self.assertEqual(response2.context["num_visits"], 2)
