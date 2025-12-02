from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import (CarSearchForm,
                        ManufacturerSearchForm,
                        DriverSearchForm)
from taxi.models import Manufacturer, Car


class FormsTests(TestCase):
    def setUp(self):
        """Create some test data for the forms to use."""
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            license_number="ABC12399"
        )
        self.client.force_login(self.user)

        self.m1 = Manufacturer.objects.create(name="Tesla", country="USA")
        self.m2 = Manufacturer.objects.create(name="BMW", country="Germany")
        self.m3 = Manufacturer.objects.create(name="Audi", country="Germany")

        self.c1 = Car.objects.create(model="Model S", manufacturer=self.m1)
        self.c2 = Car.objects.create(model="M8", manufacturer=self.m2)
        self.c3 = Car.objects.create(model="mega car", manufacturer=self.m3)

        self.d1 = get_user_model().objects.create(
            username="johndoe",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345",
        )
        self.d2 = get_user_model().objects.create(
            username="doejohn",
            first_name="Doe",
            last_name="John",
            license_number="ABC12346",
        )
        self.d3 = get_user_model().objects.create(
            username="nejohndoe",
            first_name="Nejohn",
            last_name="Doe",
            license_number="ABC12347",
        )

    def test_manufacturer_overinput_search(self):
        """Test max length of manufacturer name search field"""

        form_data = {"name": "1" * 56}
        form = ManufacturerSearchForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_car_overinput_search(self):
        form_data = {"model": "1" * 56}
        form = CarSearchForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_overinput_search(self):
        form_data = {"username": "1" * 56}
        form = DriverSearchForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_manufacturer_search_results(self):
        search_term = "a"
        response = self.client.get(
            reverse("taxi:manufacturer-list") + f"?name={search_term}"
        )
        results = response.context["manufacturer_list"]
        self.assertEqual(results.count(), 2)

    def test_car_search_results(self):
        search_term = "M8"
        response = self.client.get(
            reverse("taxi:car-list") + f"?model={search_term}"
        )
        results = response.context["car_list"]
        self.assertEqual(results.count(), 1)

    def test_driver_search_results(self):
        search_term = "doe"
        response = self.client.get(
            reverse("taxi:driver-list") + f"?username={search_term}"
        )
        results = response.context["driver_list"]
        self.assertEqual(results.count(), 3)
