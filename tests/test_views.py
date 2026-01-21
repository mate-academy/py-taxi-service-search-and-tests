from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        Car.objects.create(model="Corolla", manufacturer=self.manufacturer1)
        Car.objects.create(model="Focus", manufacturer=self.manufacturer2)
        Car.objects.create(model="Fusion", manufacturer=self.manufacturer2)
        Car.objects.create(model="Camry", manufacturer=self.manufacturer1)
        self.user = get_user_model().objects.create_user(
            username="driver1",
            password="password123",
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.select_related("manufacturer").order_by("id")
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars),
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_list_view_without_search(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")
        self.assertContains(response, "Focus")
        self.assertContains(response, "Fusion")
        self.assertContains(response, "Camry")

    def test_search_form_is_present_in_get_request(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)

    def test_car_list_view_with_search(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=Corolla")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Focus")
        self.assertNotContains(response, "Fusion")
        self.assertNotContains(response, "Camry")

    def test_car_list_view_with_search_no_results(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?model=Mustang"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no cars in taxi")
        self.assertNotContains(response, "Corolla")
        self.assertNotContains(response, "Focus")
        self.assertNotContains(response, "Fusion")
        self.assertNotContains(response, "Camry")


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="driver1",
            password="password123",
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "pass12test",
            "password2": "pass12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ABC12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
