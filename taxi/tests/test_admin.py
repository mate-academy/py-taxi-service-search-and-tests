from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Manufacturer, Car


class DriverAdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin_pass"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver_name",
            password="driver_pass",
            license_number="FGH12345"
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_driver_detailed_license_number_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_driver_creation_fieldsets(self):
        form_data = {
            "username": "Kozak",
            "password1": "23f#gf34",
            "password2": "23f#gf34",
            "first_name": "Petro",
            "last_name": "Nezlamnyi",
            "license_number": "ZXD48139"
        }

        self.client.post(reverse("admin:taxi_driver_add"), data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"])

        self.assertEqual(
            new_driver.first_name,
            form_data["first_name"]
        )
        self.assertEqual(
            new_driver.last_name,
            form_data["last_name"]
        )
        self.assertEqual(
            new_driver.license_number,
            form_data["license_number"]
        )


class CarAdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="Porsche",
            country="Germany",
        )

        number_of_cars = 7

        for car_id in range(number_of_cars):
            Car.objects.create(
                model=f"Mdl {car_id}",
                manufacturer=manufacturer,
            )

    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin_pass"
        )
        self.client.force_login(self.admin_user)

    def test_car_search_field(self):
        response = self.client.get(
            reverse("admin:taxi_car_changelist"),
            data={"model": "Mdl 1"}
        )

        self.assertContains(
            response, "Mdl 1"
        )
