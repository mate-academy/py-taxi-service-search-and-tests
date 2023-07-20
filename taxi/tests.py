from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm
from taxi.models import Manufacturer, Car


MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
CARS_URL = reverse("taxi:car-list")
DRIVERS_URL = reverse("taxi:driver-list")
MAIN_PAGE_URL = reverse("taxi:index")
REDIRECT_TO_LOGIN_PAGE = reverse("login")


class ModelsTests(TestCase):
    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="CountryTest"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self) -> None:
        driver = get_user_model().objects.create_user(
            username="username.test",
            password="TestPass1906",
            first_name="John",
            last_name="Brown"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="CountryTest"
        )
        car = Car.objects.create(
            model="ModelTest",
            manufacturer=manufacturer
        )
        self.assertEqual(
            str(car),
            car.model
        )

    def test_create_driver_with_license_number(self) -> None:
        username = "username.test"
        password = "TestPass1906"
        license_number = "TES19065"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)


class PublicViewsTests(TestCase):

    def test_manufacturers_login_required(self) -> None:
        res = self.client.get(MANUFACTURERS_URL)
        next_page = REDIRECT_TO_LOGIN_PAGE + "?next=/manufacturers/"

        self.assertNotEqual(res.status_code, 200)
        self.assertRedirects(res, next_page)

    def test_cars_login_required(self) -> None:
        res = self.client.get(CARS_URL)
        next_page = REDIRECT_TO_LOGIN_PAGE + "?next=/cars/"

        self.assertNotEqual(res.status_code, 200)
        self.assertRedirects(res, next_page)

    def test_drivers_login_required(self) -> None:
        res = self.client.get(DRIVERS_URL)
        next_page = REDIRECT_TO_LOGIN_PAGE + "?next=/drivers/"

        self.assertNotEqual(res.status_code, 200)
        self.assertRedirects(res, next_page)

    def test_main_page_login_required(self) -> None:
        res = self.client.get(MAIN_PAGE_URL)
        next_page = REDIRECT_TO_LOGIN_PAGE + "?next=/"

        self.assertNotEqual(res.status_code, 200)
        self.assertRedirects(res, next_page)


class PrivateViewsTests(TestCase):

    def setUp(self) -> None:
        username = "username.test"
        password = "TestPass1906"
        self.user = get_user_model().objects.create_user(
            username=username,
            password=password
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self) -> None:
        Manufacturer.objects.create(name="ManName1", country="ManCountry1")
        Manufacturer.objects.create(name="ManName2", country="ManCountry2")

        res = self.client.get(MANUFACTURERS_URL)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_retrieve_drivers(self) -> None:
        get_user_model().objects.create_user(
            username="DrivName1",
            password="DrivPass121",
            license_number="DRI12096"
        )
        get_user_model().objects.create_user(
            username="DrivName2",
            password="PassDriv111",
            license_number="DRI12034"
        )

        res = self.client.get(DRIVERS_URL)

        drivers = get_user_model().objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_retrieve_cars(self) -> None:
        manufacturers = [
            Manufacturer.objects.create
            (
                name="ManufacturerName1",
                country="ManufacturerCountry1"
            ),
            Manufacturer.objects.create
            (
                name="ManufacturerName2",
                country="ManufacturerCountry2"
            )
        ]

        Car.objects.create(model="CarModel1", manufacturer=manufacturers[0])
        Car.objects.create(model="CarModel2", manufacturer=manufacturers[1])
        Car.objects.create(model="CarModel3", manufacturer=manufacturers[1])

        res = self.client.get(CARS_URL)

        cars = Car.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")


class DriverFormTest(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "user.name.test",
            "license_number": "AVB12345",
            "first_name": "NameTest",
            "last_name": "LastNameTest",
            "password1": "passTest907",
            "password2": "passTest907",
        }

    def test_creation_driver_with_license_number(self) -> None:
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_create_driver_with_license_number_longer_than_8(self) -> None:
        self.form_data["license_number"] = "BOB12345678"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_create_driver_with_license_number_too_much_chars(self) -> None:
        self.form_data["license_number"] = "BOBBOB12"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_create_driver_with_license_number_too_much_numbers(self) -> None:
        self.form_data["license_number"] = "B1212121"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_create_driver_with_license_number_incorrect_order(self) -> None:
        self.form_data["license_number"] = "12121BOB"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())


class SearchFormsTest(TestCase):
    def setUp(self) -> None:
        username = "username.test"
        password = "TestPass1906"
        self.user = get_user_model().objects.create_user(
            username=username,
            password=password
        )
        self.client.force_login(self.user)

    def test_search_drivers(self) -> None:
        get_user_model().objects.create_user(
            username="DrivName1",
            password="DrivPass121",
            license_number="DRI12096"
        )
        get_user_model().objects.create_user(
            username="DrivName2",
            password="PassDriv111",
            license_number="DRI12034"
        )

        res = self.client.get(DRIVERS_URL + "?username=h")

        drivers = get_user_model().objects.filter(username__icontains="h")

        self.assertEqual(
            list(res.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_search_cars(self) -> None:
        manufacturers = [
            Manufacturer.objects.create
            (
                name="ManName1",
                country="ManCountry1"
            ),
            Manufacturer.objects.create
            (
                name="ManName2",
                country="ManCountry2"
            )
        ]

        Car.objects.create(model="CarModel1", manufacturer=manufacturers[0])
        Car.objects.create(model="CarModel2", manufacturer=manufacturers[1])
        Car.objects.create(model="CarModel3", manufacturer=manufacturers[1])

        res = self.client.get(CARS_URL + "?model=c")

        cars = Car.objects.filter(model__icontains="c")

        self.assertEqual(
            list(res.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_search_manufacturers(self) -> None:
        Manufacturer.objects.create(name="ManName1", country="ManCountry1"),
        Manufacturer.objects.create(name="ManName2", country="ManCountry2")

        res = self.client.get(MANUFACTURERS_URL + "?name=M")

        manufacturers = Manufacturer.objects.filter(name__icontains="M")

        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")
