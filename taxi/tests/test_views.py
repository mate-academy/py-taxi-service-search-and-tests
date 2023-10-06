from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Car, Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PagesOverviewPermissionTest(TestCase):

    def test_login_required(self) -> None:
        pages = {
            "Home page": reverse("taxi:index"),
            "Manufacturer List": MANUFACTURER_URL,
            "Driver List": DRIVER_URL,
            "Car List": CAR_URL,
        }
        for page_name, page_url in pages.items():
            response = self.client.get(page_url)
            self.assertNotEquals(
                response.status_code,
                200,
                f"The page '{page_name}' shouldn not to "
                f"be accessible to the public."
            )


class PrivateManufacturerTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testUser",
            password="testpass"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self) -> None:
        Manufacturer.objects.create(name="MOTOR-SICH")
        Manufacturer.objects.create(name="KHARKIV-TRACTOR-PLANT")

        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEquals(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_display_manufacturers_on_page(self) -> None:
        for number in range(1, 7):
            Manufacturer.objects.create(name=f"Test{number}")

        response = self.client.get(MANUFACTURER_URL)
        manufacturers = list(response.context["manufacturer_list"])
        self.assertEquals(len(manufacturers), 5)

        url = MANUFACTURER_URL + "?page=2"
        response2 = self.client.get(url)
        manufacturers_on_second_page = list(
            response2.context["manufacturer_list"]
        )
        self.assertEquals(len(manufacturers_on_second_page), 1)


class PrivateDriverTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_create_driver(self) -> None:
        form_data = {
            "username": "new_user",
            "license_number": "TES12345",
            "first_name": "Test_first",
            "last_name": "Test_last",
            "password1": "user12test",
            "password2": "user12test",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEquals(new_user.first_name, form_data["first_name"])
        self.assertEquals(new_user.last_name, form_data["last_name"])
        self.assertEquals(new_user.license_number, form_data["license_number"])

    def test_display_drivers_on_page(self) -> None:
        for number in range(1, 7):
            get_user_model().objects.create_user(
                username=f"Test{number}",
                password="1234test",
                license_number=f"TES{number}2345"
            )

        response = self.client.get(DRIVER_URL)
        drivers = list(response.context["driver_list"])
        self.assertEquals(len(drivers), 5)

        url = DRIVER_URL + "?page=2"
        response2 = self.client.get(url)
        drivers_on_second_page = list(
            response2.context["driver_list"]
        )
        self.assertEquals(len(drivers_on_second_page), 2)


class PrivateCarTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testUser",
            password="testpass"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self) -> None:
        manufacturer = Manufacturer.objects.create(name="MOTOR-SICH")
        Car.objects.create(model="Zaporozhec", manufacturer=manufacturer)
        Car.objects.create(model="Toyota", manufacturer=manufacturer)

        response = self.client.get(CAR_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEquals(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_str_method(self) -> None:
        manufacturer = Manufacturer.objects.create(name="MOTOR-SICH")
        car = Car.objects.create(model="Zaporozhec", manufacturer=manufacturer)

        self.assertEqual(str(car), car.model)
