from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import CarSearchForm
from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        result = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(result.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="PASSWOrd&123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Volkswagen", country="Germany")
        Manufacturer.objects.create(name="Tesla", country="USA")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)

        manufacturers = Manufacturer.objects.all()

        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            manufacturers,
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class CarListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        toyota = Manufacturer.objects.create(name="Toyota", country="Japan")
        honda = Manufacturer.objects.create(name="Honda", country="Japan")
        ford = Manufacturer.objects.create(name="Ford", country="USA")
        Car.objects.create(model="Corolla", manufacturer=toyota)
        Car.objects.create(model="Civic", manufacturer=honda)
        Car.objects.create(model="Mustang", manufacturer=ford)

    def test_search_functionality(self):
        form_data = {"model": "Corolla"}
        CarSearchForm(data=form_data)

        expected_result = Car.objects.filter(
            model__icontains=form_data["model"]
        )

        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(
            username="admin", password="Admin1991"
        )
        self.client.force_login(self.admin)
        response = self.client.get(reverse("taxi:car-list"), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["car_list"], expected_result)


class CarCreateViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test_user", password="User_1991"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "license_number": "ABC12345",
            "password1": "userPass123",
            "password2": "userPass123",
            "first_name": "new_first_name",
            "last_name": "new_last_name",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.username, form_data["username"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
