from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver

DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123")
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(name="test")
        Car.objects.create(model="test first", manufacturer=manufacturer)
        Car.objects.create(model="test second", manufacturer=manufacturer)
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)

        self.assertQuerySetEqual(response.context["object_list"],
                                 Car.objects.all())

        self.assertTemplateUsed(response, "taxi/car_list.html")

        response = self.client.get(CAR_URL, {"model": "first"})
        self.assertQuerySetEqual(response.context["object_list"],
                                 Car.objects.filter(model__icontains="first"))


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123")
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="test first")
        Manufacturer.objects.create(name="test second")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)

        self.assertQuerySetEqual(response.context["object_list"],
                                 Manufacturer.objects.all())

        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

        response = self.client.get(MANUFACTURER_URL, {"name": "first"})
        self.assertQuerySetEqual(response.context["object_list"],
                                 Manufacturer.objects.filter(
                                     name__icontains="first")
                                 )


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123")
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        Driver.objects.create(
            username="test_first_user",
            password="test123",
            first_name="test_first_name",
            last_name="test_last_name",
            license_number="Test123",
        )
        Driver.objects.create(
            username="test_second_user",
            password="test123",
            first_name="test_first_name",
            last_name="test_last_name",
            license_number="Test123",
        )
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)

        self.assertQuerySetEqual(response.context["object_list"],
                                 Driver.objects.all())

        self.assertTemplateUsed(response, "taxi/driver_list.html")

        response = self.client.get(DRIVER_URL, {"username": "first"})
        self.assertQuerySetEqual(
            response.context["object_list"],
            Driver.objects.filter(username__icontains="first")
        )

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ABC12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
