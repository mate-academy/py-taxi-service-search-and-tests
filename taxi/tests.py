from django.test import TestCase
from django.urls import reverse

from .forms import DriverCreationForm
from .models import Manufacturer, Car, Driver
from django.contrib.auth import get_user_model


class ManufacturerSearchTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create some manufacturer instances
        cls.manufacturer1 = Manufacturer.objects.create(name="Toyota",
                                                        country="Japan")
        cls.manufacturer2 = Manufacturer.objects.create(name="Ford",
                                                        country="USA")
        cls.manufacturer3 = Manufacturer.objects.create(name="Honda",
                                                        country="Japan")

        # Create a user to login
        cls.user = get_user_model().objects.create_user(username="testuser",
                                                        password="password")

    def test_search_by_name(self):
        # Login the user
        self.client.login(username="testuser", password="password")

        # Test search for manufacturers by name
        response = self.client.get(reverse("taxi:manufacturer-list")
                                   + "?name=Toyota")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")
        self.assertNotContains(response, "Honda")

        # Test another search
        response = self.client.get(reverse("taxi:manufacturer-list")
                                   + "?name=Toyota")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        response = self.client.get(reverse("taxi:manufacturer-list")
                                   + "?name=Honda")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Honda")


class CarModelSearchTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create some manufacturer and car instances
        manufacturer = Manufacturer.objects.create(name="Toyota",
                                                   country="Japan")
        cls.car1 = Car.objects.create(model="Camry",
                                      manufacturer=manufacturer)
        cls.car2 = Car.objects.create(model="Corolla",
                                      manufacturer=manufacturer)

        # Create a user to login
        cls.user = get_user_model().objects.create_user(username="testuser",
                                                        password="password")

    def test_search_by_model(self):
        # Login the user
        self.client.login(username="testuser", password="password")

        # Test search for cars by model
        response = self.client.get(reverse("taxi:car-list") + "?model=Camry")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camry")
        self.assertNotContains(response, "Corolla")

        # Test another search with partial model name
        response = self.client.get(reverse("taxi:car-list") + "?model=Cor")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Camry")


class DriverUsernameSearchTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create some driver instances
        cls.driver1 = Driver.objects.create(username="john_doe",
                                            first_name="John",
                                            last_name="Doe",
                                            license_number="ABC12345")
        cls.driver2 = Driver.objects.create(username="jane_doe",
                                            first_name="Jane",
                                            last_name="Doe",
                                            license_number="ABC12346")

        # Create a user to login
        cls.user = get_user_model().objects.create_user(username="testuser",
                                                        password="password")

    def test_search_by_username(self):
        # Login the user
        self.client.login(username="testuser", password="password")

        # Test search for drivers by username
        response = self.client.get(reverse("taxi:driver-list")
                                   + "?username=john")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john_doe")
        self.assertNotContains(response, "jane_doe")

        # Test search for non-existent driver
        response = self.client.get(reverse("taxi:driver-list")
                                   + "?username=nonexistent")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no drivers in the service.")


class DriverCreationFormTest(TestCase):

    def test_license_number_valid(self):
        form_data = {
            "username": "newdriver",
            "password1": "QAZwsxedc123!",
            "password2": "QAZwsxedc123!",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Doe"
        }
        form = DriverCreationForm(data=form_data)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())

    def test_license_number_invalid_length(self):
        form_data = {
            "username": "newdriver",
            "password1": "QAZwsxedc123!",
            "password2": "QAZwsxedc123!",
            "license_number": "ABC1234",  # Invalid length
            "first_name": "John",
            "last_name": "Doe"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_license_number_invalid_format(self):
        form_data = {
            "username": "newdriver",
            "password1": "password123",
            "password2": "password123",
            # Invalid format (should be uppercase)
            "license_number": "abc12345",
            "first_name": "John",
            "last_name": "Doe"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class ToggleAssignToCarTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create some drivers and cars
        cls.manufacturer = Manufacturer.objects.create(name="Toyota")
        cls.driver = Driver.objects.create_user(username="driver1",
                                                password="password123")
        cls.car = Car.objects.create(model="Toyota",
                                     manufacturer=cls.manufacturer)

    def test_add_driver_to_car(self):
        self.client.login(username="driver1", password="password123")
        # Initially the driver should not be assigned to the car
        self.assertFalse(self.car.drivers.filter(id=self.driver.id).exists())

        # Add the driver to the car
        response = self.client.get(reverse("taxi:toggle-car-assign",
                                           kwargs={"pk": self.car.pk}))
        self.assertRedirects(response, reverse("taxi:car-detail",
                                               kwargs={"pk": self.car.pk}))

        # Now the driver should be assigned to the car
        self.assertTrue(self.car.drivers.filter(id=self.driver.id).exists())

    def test_remove_driver_from_car(self):
        self.client.login(username="driver1", password="password123")
        self.car.drivers.add(self.driver)

        # Initially the driver is assigned to the car
        self.assertTrue(self.car.drivers.filter(id=self.driver.id).exists())

        # Remove the driver from the car
        response = self.client.get(reverse("taxi:toggle-car-assign",
                                           kwargs={"pk": self.car.pk}))
        self.assertRedirects(response, reverse("taxi:car-detail",
                                               kwargs={"pk": self.car.pk}))

        # Now the driver should be removed from the car
        self.assertFalse(self.car.drivers.filter(id=self.driver.id).exists())


class CarListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a manufacturer and some cars
        manufacturer = Manufacturer.objects.create(name="Toyota",
                                                   country="Japan")
        cls.car1 = Car.objects.create(model="Camry",
                                      manufacturer=manufacturer)
        cls.car2 = Car.objects.create(model="Corolla",
                                      manufacturer=manufacturer)

        # Create a user to login
        cls.user = get_user_model().objects.create_user(username="testuser",
                                                        password="password123")

    def test_car_model_search(self):
        self.client.login(username="testuser", password="password123")

        # Test searching for cars by model
        response = self.client.get(reverse("taxi:car-list") + "?model=Camry")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camry")
        self.assertNotContains(response, "Corolla")

    def test_empty_car_search(self):
        self.client.login(username="testuser", password="password123")

        # Test searching for cars by a non-existent model
        response = self.client.get(reverse("taxi:car-list")
                                   + "?model=NonExistent")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no cars in taxi")


class DriverModelTest(TestCase):

    def setUp(self):
        self.driver = Driver.objects.create(username="driver1",
                                            first_name="John",
                                            last_name="Doe",
                                            license_number="ABC12345")

    def test_get_absolute_url(self):
        expected_url = reverse("taxi:driver-detail",
                               kwargs={"pk": self.driver.pk})
        self.assertEqual(self.driver.get_absolute_url(), expected_url)
