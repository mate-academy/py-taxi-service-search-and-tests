from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.forms import DriverCreationForm
from taxi.models import Car


class DriverCreationFormTest(TestCase):
    def test_driver_creation_with_license_is_valid(self):
        form_data = {
            "username": "test1",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class SearchFeatureTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="search_tester",
            password="test12345",
        )
        self.client.force_login(self.user)

    def test_driver_search_feature(self):
        name_query = "search_tester"
        response = self.client.get(
            reverse("taxi:driver-list"),
            data={"name": name_query}
        )
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["driver_list"],
            get_user_model().objects.filter(username__icontains=name_query),
        )

    def test_car_search_feature(self):
        model_query = "test"
        response = self.client.get(
            reverse("taxi:car-list"),
            data={"model": model_query}
        )
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["car_list"],
            Car.objects.filter(model__icontains=model_query),
        )
