from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="manufacturer1",
            country="country1"
        )
        Manufacturer.objects.create(
            name="manufacturer2",
            country="country2"
        )
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturer = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

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


class PrivateSearchTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_search_driver(self):
        search_username = "test1"
        self.user = get_user_model().objects.create_user(
            username=search_username,
            password="test123",
            license_number="BCD12345",
        )
        self.user = get_user_model().objects.create_user(
            username="test2",
            password="test123",
            license_number="CDE12345",
        )
        self.user = get_user_model().objects.create_user(
            username="test11",
            password="test123",
            license_number="DEF12345",
        )
        response = self.client.get(
            reverse("taxi:driver-list") + f"?username={search_username}"
        )
        self.assertEqual(response.status_code, 200)
        search_result = get_user_model().objects.filter(
            username__icontains=search_username
        )
        self.assertEqual(
            list(response.context["driver_list"]),
            list(search_result),
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_car(self):
        search_model = "test1"
        manufacturer = Manufacturer.objects.create(
            name="manufacturer",
            country="country"
        )
        Car.objects.create(
            model=search_model,
            manufacturer=manufacturer,
        )
        Car.objects.create(
            model="test2",
            manufacturer=manufacturer,
        )
        Car.objects.create(
            model="test11",
            manufacturer=manufacturer,
        )
        response = self.client.get(
            reverse("taxi:car-list") + f"?model={search_model}"
        )
        self.assertEqual(response.status_code, 200)
        search_result = Car.objects.filter(model__icontains=search_model)
        self.assertEqual(
            list(response.context["car_list"]),
            list(search_result),
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_manufacturer(self):
        search_name = "manufacturer1"
        Manufacturer.objects.create(
            name=search_name,
            country="country1"
        )
        Manufacturer.objects.create(
            name="manufacturer2",
            country="country2"
        )
        Manufacturer.objects.create(
            name="manufacturer11",
            country="country3"
        )
        response = self.client.get(MANUFACTURER_URL + f"?name={search_name}")
        self.assertEqual(response.status_code, 200)
        search_result = Manufacturer.objects.filter(
            name__icontains=search_name
        )
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(search_result),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
