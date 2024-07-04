from django.test import TestCase
from taxi.models import Driver, Manufacturer, Car
from taxi.forms import DriverCreationForm, CarForm, DriverLicenseUpdateForm
from django.urls import reverse


class ModelTests(TestCase):

    def test_creating_a_driver(self):
        user = Driver.objects.create_user(username="testuser",
                                          password="password123",
                                          first_name="John",
                                          last_name="Doe",
                                          license_number="ABC1234")
        self.assertIsInstance(user, Driver)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.license_number, "ABC1234")

    def test_creating_a_manufacturer(self):
        manufacturer = Manufacturer.objects.create(name="Tesla", country="USA")
        self.assertIsInstance(manufacturer, Manufacturer)
        self.assertEqual(manufacturer.name, "Tesla")
        self.assertEqual(manufacturer.country, "USA")

    def test_creating_a_car(self):
        manufacturer = Manufacturer.objects.create(name="Toyota",
                                                   country="Japan")
        car = Car.objects.create(model="Camry", manufacturer=manufacturer)
        self.assertIsInstance(car, Car)
        self.assertEqual(car.model, "Camry")
        self.assertEqual(car.manufacturer.name, "Toyota")


class FormTests(TestCase):

    def test_driver_creation_form_valid(self):
        form = DriverCreationForm(data={"username": "testuser",
                                        "password1": "TEMU9Uzu26UNfrT",
                                        "password2": "TEMU9Uzu26UNfrT",
                                        "first_name": "John",
                                        "last_name": "Doe",
                                        "license_number": "ABC12345"})
        form.is_valid()
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_license_number(self):
        form = DriverCreationForm(data={"username": "testuser",
                                        "password1": "password123",
                                        "password2": "password123",
                                        "first_name": "John",
                                        "last_name": "Doe",
                                        "license_number": "12345"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["license_number"],
                         ["License number should consist of 8 characters"])

    def test_car_form_valid(self):
        manufacturer = Manufacturer.objects.create(name="Tesla", country="USA")
        drivers = Driver.objects.create_user(
            username="TestUsername",
            password="TestPassword123@?",
            first_name="TestFirstName",
            last_name="TestLastName",
            license_number="ABC12345"
        )
        form = CarForm(data={"model": "Model S",
                             "manufacturer": manufacturer,
                             "drivers": [drivers.pk]})
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_valid(self):
        user = Driver.objects.create_user(username="testuser",
                                          password="password123")
        form = DriverLicenseUpdateForm(instance=user,
                                       data={"license_number": "DEF56789"})
        self.assertTrue(form.is_valid())


class ViewTests(TestCase):

    def setUp(self):
        self.user = Driver.objects.create_user(username="testuser",
                                               password="password123",
                                               first_name="John",
                                               last_name="Doe",
                                               license_number="ABC1234")
        self.client.force_login(self.user)

    def test_index_view_returns_correct_context(self):
        self.client.login(username="testuser",
                          password="password123")
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_visits"], 1)
        self.assertEqual(response.context["num_drivers"], 1)

    def test_create_driver_view_redirects_to_login_when_not_logged_in(self):
        self.client.logout()
        response = self.client.post(reverse("taxi:driver-create"),
                                    data={"username": "testuser",
                                          "password1": "password123",
                                          "password2": "password123",
                                          "first_name": "John",
                                          "last_name": "Doe",
                                          "license_number": "ABC1234"})
        self.assertEqual(response.status_code, 302)

    def test_car_list_view_returns_correct_context_when_logged_in(self):
        self.client.login(username="testuser", password="password123")
        manufacturer = Manufacturer.objects.create(name="Tesla", country="USA")
        Car.objects.create(model="Model S", manufacturer=manufacturer)
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["object_list"]), 1)

    def test_car_detail_view_returns_correct_context_when_logged_in(self):
        self.client.login(username="testuser",
                          password="password123")
        manufacturer = Manufacturer.objects.create(name="Tesla",
                                                   country="USA")
        car = Car.objects.create(model="Model S",
                                 manufacturer=manufacturer)
        response = self.client.get(reverse(
            "taxi:car-detail",
            args=[car.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], car)

    def test_create_car_view_redirects_to_login_when_not_logged_in(self):
        manufacturer = Manufacturer.objects.create(name="Tesla",
                                                   country="USA")
        drivers = Driver.objects.create_user(
            username="TestUsername",
            password="TestPassword123@?",
            first_name="TestFirstName",
            last_name="TestLastName",
            license_number="ABC12345"
        )
        response = self.client.post(reverse("taxi:car-create"),
                                    data={"model": "Model X",
                                          "manufacturer": manufacturer.id,
                                          "drivers": [drivers.pk]})
        self.assertEqual(response.status_code, 302)

    def test_create_car_view_creates_car_when_logged_in(self):
        driver = Driver.objects.create_user(
            username="TestUsername",
            password="TestPassword123@?",
            first_name="TestFirstName",
            last_name="TestLastName",
            license_number="ABC12345"
        )
        self.client.login(username="testuser",
                          password="password123")
        manufacturer = Manufacturer.objects.create(name="Tesla", country="USA")
        data = {"model": "Model X",
                "manufacturer": manufacturer.id,
                "drivers": [driver.pk]}
        response = self.client.post(reverse("taxi:car-create"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Car.objects.count(), 1)
        self.assertEqual(response.url, reverse("taxi:car-list"))
