from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTests(TestCase):

    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 302)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="ATest", country="Lviv"
        )
        Manufacturer.objects.create(name="BTest2", country="Lviv2")
        Manufacturer.objects.create(name="BTest3", country="Lviv3")
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="12121212@A",
            first_name="Test",
            last_name="User",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        manufacturer_queryset = Manufacturer.objects.all()
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(
                response.context["manufacturer_list"]
            ), list(manufacturer_queryset)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_manufacturers_after_searching_by_name(self):
        manufacturer_queryset = Manufacturer.objects.filter(
            name__icontains="b"
        )
        response = self.client.get(MANUFACTURER_URL + "?name=b")

        self.assertEqual(
            list(
                response.context["manufacturer_list"]
            ), list(manufacturer_queryset)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PublicCarTests(TestCase):

    def test_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 302)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Test", country="Lviv"
        )
        self.car = Car.objects.create(
            model="BMW F20",
            manufacturer=self.manufacturer
        )
        Car.objects.create(
            model="mitsubishi lancer",
            manufacturer=self.manufacturer
        )
        Car.objects.create(
            model="mitsubishi eclipse",
            manufacturer=self.manufacturer
        )
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="12121212@A",
            first_name="Test",
            last_name="User",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        car_queryset = Car.objects.all()
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]), list(car_queryset)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_cars_after_searching_by_model(self):
        cars_queryset = Car.objects.filter(model__icontains="mi")
        response = self.client.get(CAR_URL + "?model=mi")

        self.assertEqual(
            list(response.context["car_list"]), list(cars_queryset)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PublicDriverTests(TestCase):

    def test_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 302)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="12121212@A",
            first_name="Test",
            last_name="User",
            license_number="ABC12345"
        )
        get_user_model().objects.create_user(
            username="Anatoliy",
            password="12121212@A",
            first_name="Test",
            last_name="User",
            license_number="ABC12341"
        )
        get_user_model().objects.create_user(
            username="Andrew",
            password="12121212@A",
            first_name="Test",
            last_name="User",
            license_number="ABC12342"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        car_queryset = get_user_model().objects.all()
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]
                 ), list(car_queryset))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_create_driver(self):
        form_data = {
            "username": "OrdinaryUser",
            "password1": "12121212@A",
            "password2": "12121212@A",
            "first_name": "Ordinary",
            "last_name": "User",
            "license_number": "ABC12346"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEqual(
            new_driver.first_name, form_data["first_name"]
        )
        self.assertEqual(
            new_driver.last_name, form_data["last_name"]
        )
        self.assertEqual(
            new_driver.license_number, form_data["license_number"]
        )

    def test_retrieve_drivers_after_searching_by_username(self):
        drivers_queryset = get_user_model().objects.filter(
            username__icontains="an"
        )
        response = self.client.get(DRIVER_URL + "?username=an")

        self.assertEqual(
            list(response.context["driver_list"]), list(drivers_queryset)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
