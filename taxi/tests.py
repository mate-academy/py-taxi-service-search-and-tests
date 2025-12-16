from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverSearchForm
from taxi.models import Car, Manufacturer


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin",

        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="author",
            password="testdriver",
            license_number="MVL93412"
        )

    def test_driver_listed(self):
        """
        Test get driver's license number is
        in list_display on driver admin page.
        :return:
        """
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_pseudonym_listed(self):
        """
        Test get driver's license number is on driver detail admin page.
        :return:
        """
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)


class FormsTests(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "driver1",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ABC99999"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


TOGGLE_URL = reverse("taxi:toggle-car-assign",
                     kwargs={"pk": 1})


class PublicViewsTests(TestCase):
    def test_toggle_assign_login_required(self):
        response = self.client.post(TOGGLE_URL)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)


class PrivateViewsTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "driver12",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test ffirst",
            "last_name": "Test llast",
            "license_number": "ABB99999"
        }
        self.client.post(
            reverse("taxi:driver-create"), data=form_data)
        new_user = (get_user_model()
                    .objects.get(license_number=form_data["license_number"]))

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])


class SearchFormTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_search_driver_form_is_valid(self):
        form_data = {
            "username": "driver12"
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_search_driver_by_username(self):
        self.driver1 = get_user_model().objects.create_user(
            username="driver1",
            password="test123",
            license_number="ABC12345",
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver2",
            password="test123",
            license_number="DEF67890",
        )
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "driver1"},
        )

        drivers = response.context.get("driver_list")

        self.assertIn(self.driver1, drivers)
        self.assertNotIn(self.driver2, drivers)

    def test_search_car_by_model(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        self.car1 = Car.objects.create(
            model="X5",
            manufacturer=manufacturer,
        )
        self.car2 = Car.objects.create(
            model="A4",
            manufacturer=manufacturer,
        )
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "X5"},
        )

        self.assertEqual(response.status_code, 200)

        cars = response.context["car_list"]

        self.assertIn(self.car1, cars)
        self.assertNotIn(self.car2, cars)

    def test_search_manufacturer_by_name(self):
        self.manufacturer1 = Manufacturer.objects.create(
            name="Audi",
            country="Germany",
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Audi"},
        )

        self.assertEqual(response.status_code, 200)

        manufacturers = response.context["manufacturer_list"]

        self.assertIn(self.manufacturer1, manufacturers)
        self.assertNotIn(self.manufacturer2, manufacturers)
