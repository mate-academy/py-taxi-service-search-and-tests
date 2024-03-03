from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.http import urlencode

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):

    def test_login_required(self):
        request = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(request.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="test1", country="test1")
        Manufacturer.objects.create(name="test2", country="test2")

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_filter_manufacturer_list(self):
        filter_value = "test1"
        response = self.client.get(
            f"{MANUFACTURER_URL}?{urlencode({"name": filter_value})}"
        )
        manufacturers = Manufacturer.objects.filter(
            name__icontains=filter_value
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )


class PublicCarTest(TestCase):

    def test_login_required(self):
        request = self.client.get(CAR_URL)
        self.assertNotEqual(request.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)
        manufacturer1 = Manufacturer.objects.create(name="test1",
                                                    country="test1")
        manufacturer2 = Manufacturer.objects.create(name="test2",
                                                    country="test2")
        Car.objects.create(model="test1", manufacturer=manufacturer1)
        Car.objects.create(model="test2", manufacturer=manufacturer2)

    def test_retrieve_car(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        car = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(car),
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_filter_car_list(self):
        filter_value = "test1"
        response = self.client.get(
            f"{CAR_URL}?{urlencode({"model": filter_value})}"
        )
        cars = Car.objects.filter(
            model__icontains=filter_value
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )


class PublicDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test1",
            password="test123",
        )
        self.client.force_login(self.user)

        get_user_model().objects.create(
            username="test2",
            password="test123",
            license_number="BBB12345"
        )

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "test first_name",
            "last_name": "test last_name",
            "license_number": "ABC12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_retrieve_driver(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        driver = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(driver),
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_filter_car_list(self):
        filter_value = "test2"
        response = self.client.get(
            f"{DRIVER_URL}?{urlencode({"username": filter_value})}"
        )
        drivers = get_user_model().objects.filter(
            username__icontains=filter_value
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
