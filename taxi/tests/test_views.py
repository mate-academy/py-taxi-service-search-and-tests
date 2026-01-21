from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car
from django.contrib.auth import get_user_model


HOME_PAGE_URL = reverse("taxi:index")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")
User = get_user_model()


class PublicIndexTest(TestCase):
    def test_login_required(self):
        res = self.client.get(HOME_PAGE_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateIndexTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            password="test34534",
        )
        self.client.force_login(self.user)

    def test_retrieve_index(self):
        response = self.client.get(HOME_PAGE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "base.html"
        )


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            password="test34534",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        Manufacturer.objects.create(
            name="TOYOTA",
            country="Japan",
        )
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(
            response, "taxi/manufacturer_list.html"
        )


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            password="test34534",
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        manufacturer = Manufacturer.objects.create(
            name="TOYOTA",
            country="Japan",
        )
        Car.objects.create(
            model="M5competition",
            manufacturer=manufacturer,
        )
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "taxi/car_list.html"
        )


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test", password="test_password"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "taxi/driver_list.html"
        )

    def test_create_driver(self):
        form_data = {
            "username": "test_user",
            "password1": "test123test",
            "password2": "test123test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "TES44422",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = User.objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
