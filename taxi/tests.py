from http.client import responses

from django.contrib.auth import get_user_model
from django.template.defaultfilters import first
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import DriverCreationForm
from taxi.models import Manufacturer, Car, Driver


# Create your tests here.
# Перевірка на роботу str методу ( Manufacturer )
class ModelsTest(TestCase):
    def test_manufacturer_format_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test", country="Ukraine")
        expected = "test Ukraine"
        self.assertEqual(str(manufacturer), expected)

# Перевірка на роботу str методу ( Car )
    def test_car_format_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test", country="Ukraine")
        car = Car.objects.create(model="BMW",
                                 manufacturer=manufacturer)
        expected = "BMW"
        self.assertEqual(str(car), expected)

    def test_driver_format_str(self):
        driver = Driver.objects.create(username="Akimbo",
                                       first_name="Alex",
                                       last_name="Gordon")
        expected = "Akimbo (Alex Gordon)"
        self.assertEqual(str(driver), expected)


class CarSearchTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Создаем пользователя и логиним
        self.user = get_user_model().objects.create_user(
            username="Admin",
            password="admin12",
        )
        self.client.login(username="Admin",
                          password="admin12")
        self.manufacturer = Manufacturer.objects.create(
            name="TestMan", country="Germany")

        # Создаем машины
        Car.objects.create(model="BMW", manufacturer=self.manufacturer)
        Car.objects.create(model="Audi", manufacturer=self.manufacturer)
        Car.objects.create(model="Mercedes", manufacturer=self.manufacturer)

    def test_search_car_by_model(self):
        # Отправляем GET-запрос с параметром поиска
        url = reverse("taxi:car-list") + "?model=BMW"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Audi")


class ManufacturerSearchTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Создаем пользователя и логиним
        self.user = get_user_model().objects.create_user(
            username="Admin",
            password="admin12",
        )
        self.client.login(username="Admin",
                          password="admin12")
        self.manufacturer = Manufacturer.objects.create(
            name="TestMan", country="Germany")
        # Создаем производителя
        Manufacturer.objects.create(name="HyperX", country="Ukraine")
        Manufacturer.objects.create(name="Razer", country="Germany")
        Manufacturer.objects.create(name="Logitech", country="France")

    def test_search_manufacturer(self):
        url = reverse("taxi:manufacturer-list") + "?name=HyperX"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "HyperX")
        self.assertNotContains(response, "Logitech")


class DriverSearchTest(TestCase):
    def setUp(self):
        self.client = Client()
    # Создаем пользователя и логиним
        self.user = get_user_model().objects.create_user(
            username="Admin",
            password="admin12",
        )
        self.client.login(username="Admin",
                          password="admin12")
        self.manufacturer = Manufacturer.objects.create(
            name="TestMan", country="Germany")
    # Создаем водителей
        Driver.objects.create(username="Driver1", license_number="ABC14345")
        Driver.objects.create(username="Driver2", license_number="ABC16745")
        Driver.objects.create(username="Driver3", license_number="ABC12115")

    def test_search_driver(self):
        url = reverse("taxi:driver-list") + "?username=Driver1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Driver1")
        self.assertNotContains(response, "Driver2")


class DriverCreationFormTest(TestCase):
    def test_form_valid_with_correct_data(self):
        form_data = {
            "username": "testdriver",
            "password1": "SecurePass123",
            "password2": "SecurePass123",
            "first_name": "John",
            "last_name": "Doe",
            "license_number": "ABC12344",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())


class DriverCreationFormTest2(TestCase):
    def test_form_invalid_with_correct_data(self):
        form_data = {
            "username": "testdriver",
            "password1": "SecurePass123",
            "password2": "SecurePass123",
            "first_name": "John",
            "last_name": "Doe",
            "license_number": "ABC1233",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
