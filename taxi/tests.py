from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from .forms import CarForm, DriverCreationForm
from .models import Manufacturer, Driver, Car

manufacturer_list_url = reverse("taxi:manufacturer-list")
car_list_url = reverse("taxi:car-list")
driver_list_url = reverse("taxi:driver-list")


class ModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = (Manufacturer.objects.create
                        (name="test", country="case"))
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self):
        driver = Driver.objects.create(username="test",
                                       first_name="case",
                                       last_name="nr1")
        self.assertEqual(str(driver), "test (case nr1)")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="manufacturer",
                                                   country="mtest")
        car = Car.objects.create(model="test model", manufacturer=manufacturer)
        driver = Driver.objects.create(username="driver", first_name="dtest",
                                       last_name="dtest")
        car.drivers.set([driver])
        self.assertEqual(str(car), "test model")

    def test_create_driver_with_license_number(self):
        driver = Driver.objects.create(license_number="test1234")

        self.assertEqual(driver.license_number, "test1234")


class AdminPanelTest(TestCase):
    def setUp(self):
        user = get_user_model()
        self.admin_user = user.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123"
        )
        self.client.login(username="admin", password="admin123")
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Testland"
        )
        self.driver = Driver.objects.create(
            username="testdriver",
            first_name="Test",
            last_name="Driver",
            license_number="ABC123"
        )
        self.car = Car.objects.create(
            model="Test Car",
            manufacturer=self.manufacturer
        )
        self.car.drivers.set([self.driver])

    def test_driver_list_display(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.driver.username)
        self.assertContains(res, self.driver.license_number)

    def test_car_list_display(self):
        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.car.model)
        self.assertContains(res, self.manufacturer.name)

    def test_manufacturer_list_display(self):
        url = reverse("admin:taxi_manufacturer_changelist")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.manufacturer.name)
        self.assertContains(res, self.manufacturer.country)


class PublicManufacturerViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(manufacturer_list_url)
        self.assertNotEqual(res.status_code, 200)


class PublicCarViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(car_list_url)
        self.assertNotEqual(res.status_code, 200)


class PublicDriverViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(driver_list_url)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="driver",
            first_name="dtest",
            last_name="dtest",
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = (Manufacturer.objects.create
                        (name="manufacturer",
                            country="mtest"))
        car = Car.objects.create(model="test model",
                                 manufacturer=manufacturer)
        driver = self.user
        car.drivers.set([driver])

        response = self.client.get(car_list_url)
        self.assertEqual(response.status_code, 200)


class CarFormTest(TestCase):
    def setUp(self):
        self.driver1 = Driver.objects.create(
            username="testdriver",
            first_name="Test",
            last_name="Driver",
            license_number="ABC123"
        )

        self.manufacturer = Manufacturer.objects.create(
            name="TestManuf",
            country="TestLand"
        )

    def test_form_is_valid(self):
        form_data = {
            "model": "Test Car Model",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver1.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())


class DriverCreationFormTest(TestCase):
    def test_form_is_valid(self):
        form_data = {
            "username": "testdriver",
            "first_name": "test_guy",
            "last_name": "testowski",
            "license_number": "LUB12345",
            "password1": "JURIRURI@21",
            "password2": "JURIRURI@21",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())


class DriverSearchBasicTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(username="john_doe",
                                                 password="PASSWORD@1",
                                                 license_number="SWD12345")

        self.driver1 = Driver.objects.create_user(username="jane_smith",
                                                  password="PASSWORD#1",
                                                  license_number="LUB12345")
        self.client.login(username="john_doe", password="PASSWORD@1")

    def test_search_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=john")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john_doe")
        self.assertNotContains(response, "jane_smith")


class CarSearchBasicTest(TestCase):

    def setUp(self):
        manufacturer = (Manufacturer.objects.create
                        (name="manufacturer",
                         country="mtest"))
        car = Car.objects.create(model="test model",
                                 manufacturer=manufacturer)
        driver = Driver.objects.create_user(username="john_doe",
                                            password="pass123")
        car.drivers.set([driver])
        self.client.login(username="john_doe", password="pass123")

    def test_search_by_model(self):
        response = self.client.get(reverse(
            "taxi:car-list") + "?model=test model")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test model")


class ManufacturerSearchBasicTest(TestCase):
    def setUp(self):
        Manufacturer.objects.create(name="manufacturer", country="mtest")
        Driver.objects.create_user(username="john_doe", password="pass123")
        self.client.login(username="john_doe", password="pass123")

    def test_search_by_name(self):
        response =\
            (self.client.get(reverse(
                "taxi:manufacturer-list") + "?name=manufacturer"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "manufacturer")
