from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import CarSearchForm
from taxi.models import Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")
CAR_CREATE_URL = reverse("taxi:car-create")
CAR_UPDATE_URL = reverse("taxi:car-update", args=["1"])
CAR_DELETE_URL = reverse("taxi:car-delete", args=["1"])


class PublicCarTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_list_required(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_create_required(self):
        response = self.client.get(CAR_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_update_required(self):
        response = self.client.get(CAR_UPDATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_delete_required(self):
        response = self.client.get(CAR_DELETE_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarListTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="Test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_content(self):
        response = self.client.get(CAR_LIST_URL)
        car_list = Car.objects.all()

        self.assertEqual(
            list(response.context["car_list"]),
            list(car_list)
        )

    def test_template(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_type_of_search_form(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(
            type(response.context["search_form"]), type(CarSearchForm())
        )


class PrivateCarCreateTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="Test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_car_create(self):
        response = self.client.get(CAR_CREATE_URL)
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get(CAR_CREATE_URL)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_success_url(self):
        response = self.client.get(CAR_CREATE_URL)
        self.assertEqual(
            response.context_data["view"].success_url,
            reverse("taxi:car-list")
        )


class PrivateCarUpdateTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="Test1234"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test country"
        )
        self.car = Car.objects.create(
            model="Test",
            manufacturer=self.manufacturer
        )
        self.client.force_login(self.user)

    def test_retrieve_car_create(self):
        response = self.client.get(CAR_UPDATE_URL)
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get(CAR_UPDATE_URL)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_success_url(self):
        response = self.client.get(CAR_UPDATE_URL)
        self.assertEqual(
            response.context_data["view"].success_url,
            reverse("taxi:car-list")
        )


class PrivateCarDeleteTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="Test1234"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test country"
        )
        self.car = Car.objects.create(
            model="Test",
            manufacturer=self.manufacturer
        )
        self.client.force_login(self.user)

    def test_retrieve_car_create(self):
        response = self.client.get(CAR_DELETE_URL)
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get(CAR_DELETE_URL)
        self.assertTemplateUsed(response, "taxi/car_confirm_delete.html")

    def test_success_url(self):
        response = self.client.get(CAR_DELETE_URL)
        self.assertEqual(
            response.context_data["view"].success_url,
            reverse("taxi:car-list")
        )
