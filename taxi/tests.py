from django.contrib.auth import get_user_model
from django.urls import reverse
from taxi.forms import DriverCreationForm, DriverSearchForm, CarSearchForm, \
    ManufacturerSearchForm
from taxi.models import Manufacturer, Driver, Car
from django.test import TestCase

# Create your tests here.
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class ModelsTests(TestCase):
    def test_manufacturer_str(self) -> None:
        manufacturer = (Manufacturer.objects
                        .create(name="BMW", country="Germany"))
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self) -> None:
        driver = Driver.objects.create(
            username="test",
            first_name="Sebastian",
            last_name="Sokolowski",
            license_number="1QAZXSW2",
        )
        self.assertEqual(
            str(driver), f"{driver.username} "
                         f"({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self) -> None:
        manufacturer = (Manufacturer.objects
                        .create(name="BMW", country="Germany"))
        car = Car.objects.create(model="X5", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)


class AdminTest(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="admin123"
        )
        self.client.force_login(self.admin_user)

        self.driver = Driver.objects.create_user(
            username="test",
            password="test123",
            license_number="1QAZCDE3",
        )

    def test_driver_licencse(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)


class FormTest(TestCase):
    def test_driver_search_form(self):
        username = {"username": "admin"}
        username_search = DriverSearchForm(data=username)
        self.assertTrue(username_search.is_valid())
        self.assertEqual(username_search.cleaned_data, username)

    def test_car_search_form(self):
        model = {"model": "Lincoln"}
        model_search = CarSearchForm(data=model)
        self.assertTrue(model_search.is_valid())
        self.assertEqual(model_search.cleaned_data, model)

    def test_manufacturer_search_form(self):
        name = {"name": "BMW"}
        name_search = ManufacturerSearchForm(data=name)
        self.assertTrue(name_search.is_valid())
        self.assertEqual(name_search.cleaned_data, name)


class ViewsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin", password="admin"
        )
        self.client.force_login(self.user)

    def test_manufacturer_by_name_matching(self):
        ford = Manufacturer.objects.create(name="Ford", country="USA")
        honda = Manufacturer.objects.create(name="Honda", country="Japan")

        response = self.client.get(MANUFACTURER_URL)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, honda.name)
        self.assertContains(response, ford.name)

    def test_manufacturer_by_name_non_matching(self):
        honda = Manufacturer.objects.create(name="Honda", country="Japan")

        response = self.client.get(MANUFACTURER_URL, {"name": "Ford"})
        self.assertNotContains(response, honda.name)

    def test_manufacturer_by_name(self):
        honda = Manufacturer.objects.create(name="Honda", country="Japan")

        response = self.client.get(MANUFACTURER_URL, {"name": "Honda"})
        self.assertContains(response, honda.name)

    def test_car_by_name(self):
        manufacturer = (Manufacturer.objects
                        .create(name="Honda", country="Japan"))
        car = Car.objects.create(model="Civic", manufacturer=manufacturer)
        car.drivers.add(self.user)

        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Civic")
