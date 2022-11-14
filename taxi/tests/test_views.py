from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car

LOGIN_PAGE = reverse("login")
HOME_PAGE = reverse("taxi:index")
DRIVER_LIST = reverse("taxi:driver-list")
CAR_LIST = reverse("taxi:car-list")
MANUFACTURER_LIST = reverse("taxi:manufacturer-list")


class PublicViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_login_required(self):
        response = self.client.get(HOME_PAGE)

        self.assertNotEqual(response.status_code, 200)

    def test_driver_list_login_required(self):
        response = self.client.get(DRIVER_LIST)

        self.assertNotEqual(response.status_code, 200)

    def test_car_list_login_required(self):
        response = self.client.get(CAR_LIST)

        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_list_login_required(self):
        response = self.client.get(MANUFACTURER_LIST)

        self.assertNotEqual(response.status_code, 200)

    def test_login_page_login_not_required(self):
        response = self.client.get(LOGIN_PAGE)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")


class PrivateViewsTest(TestCase):
    def setUp(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Country"
        )
        Car.objects.create(
            model="Test",
            manufacturer=manufacturer
        )
        self.user = get_user_model().objects.create_user(
            "new_user",
            "user1234"
        )
        self.client.force_login(self.user)

    def test_user_access_to_home_page(self):
        response = self.client.get(HOME_PAGE)

        self.assertEqual(response.status_code, 200)

    def test_user_access_to_car_list(self):
        cars = Car.objects.all()
        response = self.client.get(CAR_LIST)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

    def test_user_access_to_driver_list(self):
        drivers = get_user_model().objects.all()
        response = self.client.get(DRIVER_LIST)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )

    def test_user_access_to_manufacturer_list(self):
        manufacturers = Manufacturer.objects.all()
        response = self.client.get(MANUFACTURER_LIST)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_user_access_to_login_page(self):
        response = self.client.get(LOGIN_PAGE)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")


class CreateViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "new_user",
            "user1234"
        )
        self.client.force_login(self.user)

    def test_driver_create_view(self):
        form_data = {
            "username": "test_user",
            "password1": "user1234",
            "password2": "user1234",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "LIC12345"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(user.first_name, form_data["first_name"])
        self.assertEqual(user.last_name, form_data["last_name"])
        self.assertEqual(user.license_number, form_data["license_number"])


class TestSearchField(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "user", "testuser123"
        )
        self.client.force_login(self.user)

    def test_search_driver(self):
        response = self.client.get("/drivers/?username=a/")

        self.assertQuerysetEqual(
            response.context["driver_list"],
            get_user_model().objects.filter(username__icontains="a")
        )
        self.assertEqual(response.status_code, 200)

    def test_search_manufacturer(self):
        response = self.client.get("/manufacturers/?name=a/")

        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            Manufacturer.objects.filter(name__icontains="a")
        )
        self.assertEqual(response.status_code, 200)

    def test_search_car(self):
        response = self.client.get("/cars/?model=a/")

        self.assertQuerysetEqual(
            response.context["car_list"],
            Car.objects.filter(model__icontains="a")
        )
        self.assertEqual(response.status_code, 200)
