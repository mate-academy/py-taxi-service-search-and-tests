from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriversSearchForm
from taxi.models import Driver, Car, Manufacturer

DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicDriversViewTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertRedirects(
            response,
            f"{settings.LOGIN_URL}?next={DRIVER_LIST_URL}"
        )


class PrivateDriversViewTests(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="testuser",
            password="test_123",
        )
        self.client.force_login(self.user)

        self.driver1 = Driver.objects.create_user(
            username="alice",
            password="pass123",
            license_number="ABC12345"
        )
        self.driver2 = Driver.objects.create_user(
            username="bob",
            password="pass456",
            license_number="XYZ67890"
        )

    def test_toggle_assign_to_car(self):
        car = Car.objects.create(
            model="X5",
            manufacturer=Manufacturer.objects.create(
                name="BMW",
                country="USA"
            )
        )
        url = reverse("taxi:toggle-car-assign", args=[car.id])
        response = self.client.get(url)
        self.assertRedirects(
            response,
            reverse("taxi:car-detail", args=[car.id])
        )
        self.assertIn(car, self.user.cars.all())

    def test_list_view_displays_drivers(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertIn(self.driver1, response.context["driver_list"])
        self.assertIn(self.driver2, response.context["driver_list"])

    def test_search_filters_queryset(self):
        """
        Search form should filter drivers by username.
        """
        response = self.client.get(DRIVER_LIST_URL, {"username": "ali"})

        driver_list = response.context["driver_list"]

        self.assertIn(self.driver1, driver_list)
        self.assertNotIn(self.driver2, driver_list)

    def test_context_contains_search_form(self):
        """
        The view context should include the DriversSearchForm.
        """
        response = self.client.get(DRIVER_LIST_URL)

        form = response.context.get("search_form")
        self.assertIsInstance(form, DriversSearchForm)
        self.assertIn("username", form.fields)

    def test_search_no_results_returns_empty_list(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "nope"})
        self.assertFalse(response.context["driver_list"].exists())

    def test_search_empty_query_returns_full_list(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": ""})
        driver_list = response.context["driver_list"]
        self.assertIn(self.driver1, driver_list)
        self.assertIn(self.driver2, driver_list)
