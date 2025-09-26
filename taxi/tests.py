from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Driver, Car, Manufacturer
from taxi.forms import DriverCreationForm


class ModelTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create(
            username="testdriver",
            first_name="John",
            last_name="Doe",
            license_number="ABC123"
        )

    def test_driver_str_method(self):
        """Test driver string representation"""
        self.assertEqual(str(self.driver), "testdriver (John Doe)")


class FormTests(TestCase):
    def test_driver_creation_form_valid(self):
        """Test driver creation form with valid data"""
        form_data = {
            "username": "newdriver",
            "first_name": "Jane",
            "last_name": "Smith",
            "license_number": "XYZ98765",
            "password1": "testpass123",
            "password2": "testpass123",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_license(self):
        """Test driver creation form with invalid license"""
        form_data = {
            "username": "newdriver",
            "license_number": "invalid",  # Invalid format
            "password1": "testpass123",
            "password2": "testpass123",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class SearchTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Driver.objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345"
        )

        # Create test drivers
        self.john_driver = Driver.objects.create_user(
            username="john_driver",
            first_name="John",
            last_name="Driver",
            password="testpass",
            license_number="JOH12345"
        )
        self.jane_driver = Driver.objects.create_user(
            username="jane_driver",
            first_name="Jane",
            last_name="Driver",
            password="testpass",
            license_number="JAN98765"
        )

        # Create test manufacturers
        self.toyota = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.honda = Manufacturer.objects.create(
            name="Honda",
            country="Japan",
        )
        self.bmw = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        # Create test cars
        self.camry = Car.objects.create(
            model="Camry",
            manufacturer=self.toyota,
        )
        self.civic = Car.objects.create(
            model="Civic",
            manufacturer=self.honda,
        )
        self.corolla = Car.objects.create(
            model="Corolla",
            manufacturer=self.toyota,
        )

        self.client.login(username="testuser", password="testpass123")

    def test_driver_list_contains_search_form(self):
        """Test that driver list page contains search form"""
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'placeholder="Search by username"')
        self.assertContains(response, 'type="submit"')
        self.assertContains(response, 'value="Search"')

    def test_driver_search_form_preserves_input(self):
        """Test that search form preserves user input after search"""
        search_term = "john"
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": search_term},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'value="{search_term}"')

    def test_driver_search_case_insensitive(self):
        """Test case-insensitive driver search"""
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "JOHN"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john_driver")
        self.assertNotContains(response, "jane_driver")

    def test_driver_search_partial_match_multiple(self):
        """Test partial search returns multiple matches"""
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "driver"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john_driver")
        self.assertContains(response, "jane_driver")

    def test_car_list_contains_search_form(self):
        """Test that car list page contains search form"""
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="model"')
        self.assertContains(response, 'placeholder="Search by model"')

    def test_manufacturer_list_contains_search_form(self):
        """Test that manufacturer list page contains search form"""
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="name"')
        self.assertContains(response, 'placeholder="Search by name"')

    def test_driver_search_by_username(self):
        """Test driver search by username - finds matching results"""
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "john"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john_driver")
        self.assertNotContains(response, "jane_driver")

    def test_driver_search_no_results(self):
        """Test driver search with no matching results"""
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "nonexistent"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "john_driver")
        self.assertNotContains(response, "jane_driver")

    def test_driver_search_empty_shows_all(self):
        """Test driver search with empty query shows all drivers"""
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": ""},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john_driver")
        self.assertContains(response, "jane_driver")

    def test_car_search_by_model(self):
        """Test car search by model - finds matching results"""
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "cam"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camry")
        self.assertNotContains(response, "Civic")
        self.assertNotContains(response, "Corolla")

    def test_car_search_case_insensitive(self):
        """Test car search is case insensitive"""
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "CIVIC"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Civic")

    def test_car_search_partial_match(self):
        """Test car search with partial match"""
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "co"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Camry")

    def test_manufacturer_search_by_name(self):
        """Test manufacturer search by name - finds matching results"""
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "toy"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Honda")
        self.assertNotContains(response, "BMW")

    def test_manufacturer_search_exact_match(self):
        """Test manufacturer search with exact match"""
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "BMW"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Toyota")

    def test_manufacturer_search_no_results(self):
        """Test manufacturer search with no matching results"""
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Ferrari"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Toyota")
        self.assertNotContains(response, "Honda")
        self.assertNotContains(response, "BMW")


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Driver.objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345"
        )

    def test_index_view_works(self):
        """Test index view loads correctly"""
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)

    def test_driver_list_requires_login(self):
        """Test driver list requires login"""
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertRedirects(
            response,
            "/accounts/login/?next=/drivers/",
        )

    def test_driver_list_works_when_logged_in(self):
        """Test driver list works when logged in"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
