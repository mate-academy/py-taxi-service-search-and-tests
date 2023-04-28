from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm
from taxi.models import Manufacturer, Car, Driver

CAR_LIST_URL = reverse("taxi:car-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class FormTests(TestCase):
    def test_driver_creation_is_valid(self):
        """
        Test driver creation form with
        license number, first name,
        last name is_valid
        """

        form_data = {
            "username": "new_user",
            "password1": "us123test",
            "password2": "us123test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ASD12345"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class SearchFormsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_search_car(self):
        manufacturer = Manufacturer.objects.create(name="manufacturer test")

        Car.objects.create(model="one_test", manufacturer=manufacturer)
        Car.objects.create(model="two_test", manufacturer=manufacturer)

        search_date = {"model": "one"}

        response = self.client.get(CAR_LIST_URL, data=search_date)
        car = Car.objects.filter(model__icontains="one")

        self.assertEqual(
            list(response.context["car_list"]),
            list(car)
        )

    def test_search_manufacturer(self):

        Manufacturer.objects.create(name="one_test")
        Manufacturer.objects.create(name="two_test")

        search_date = {"name": "one"}

        response = self.client.get(MANUFACTURER_LIST_URL, data=search_date)
        manufacturer = Manufacturer.objects.filter(name__icontains="one")

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer)
        )

    def test_search_driver(self):

        Driver.objects.create_user(
            username="one_test",
            license_number="ASD12345",
        )
        Driver.objects.create_user(
            username="two_test",
            license_number="QWE12345",
        )

        search_date = {"username": "one"}

        response = self.client.get(DRIVER_LIST_URL, data=search_date)
        driver = Driver.objects.filter(username__icontains="one")

        self.assertEqual(
            list(response.context["driver_list"]),
            list(driver)
        )
