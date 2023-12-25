from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import CarSearchForm
from taxi.models import Driver, Car, Manufacturer


class FormsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="admin", password="password",
            license_number="VAT12345")
        self.driver = get_user_model().objects.create_user(
            username="stefan", password="12345")

    def test_login_form(self):
        self.client.post(reverse("login"),
                         {"username": "stefan", "password": "12345"})
        res = self.client.get(reverse("taxi:index"))
        self.assertEqual(res.context["user"], self.driver)

    def test_create_driver(self):
        self.client.force_login(self.user)
        data = {"username": "stepan123",
                "first_name": "stepan",
                "last_name": "shevchuk",
                "password1": "12345",
                "password2": "12345",
                "license_number": "NED12345"}
        self.client.post(reverse("taxi:driver-create"), data=data)
        new_user = get_user_model().objects.get(username="stepan123")
        self.assertEqual(new_user.license_number, data["license_number"])


class SearchFormTest(TestCase):
    def test_car_search_form(self):
        self.user = get_user_model().objects.create_superuser(
            username="admin",
            password="password",
            license_number="VAT12345")
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="BMW", country="Germany")
        Car.objects.create(model="M4", manufacturer_id="1")
        Car.objects.create(model="3", manufacturer_id="1")
        res = self.client.get("/cars/?model=m")
        self.assertEqual(list(res.context["car_list"]),
                         list(Car.objects.filter(model__icontains="m")))

    def test_car_search_form_with_data(self):
        form = CarSearchForm()
        self.assertFalse(form.is_valid())
        form = CarSearchForm({"model": "M"})
        self.assertTrue(form.is_valid())
