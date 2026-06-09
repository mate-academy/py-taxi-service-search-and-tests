from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car


class ViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.driver = Driver.objects.create_user(
            username="UsernameTest",
            password="DriverPassword",
            first_name="DriverFirstName",
            last_name="DriverLastName",
            license_number="ADM12345",
        )
        cls.manufacturer_toyota = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        cls.manufacturer_volkswagen = Manufacturer.objects.create(
            name="Volkswagen",
            country="Germany",
        )

        cls.car_supra = Car.objects.create(
            model="Supra",
            manufacturer=cls.manufacturer_toyota,
        )
        cls.car_volkswagen = Car.objects.create(
            model="Touareg",
            manufacturer=cls.manufacturer_volkswagen
        )

    def test_anonymous_user_redirect_to_login(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 302)

    def test_index_page(self):
        self.client.force_login(self.driver)
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_visits"], 1)
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.context["num_visits"], 2)

    def test_manufacturer_name_search(self):
        self.client.force_login(self.driver)
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            data={"name": "Toyota"}
        )
        self.assertIn(
            self.manufacturer_toyota,
            response.context["manufacturer_list"]
        )
        self.assertNotIn(
            self.manufacturer_volkswagen,
            response.context["manufacturer_list"]
        )

    def test_car_model_search(self):
        self.client.force_login(self.driver)
        response = self.client.get(
            reverse("taxi:car-list"),
            data={"model": "Supra"}
        )
        self.assertIn(
            self.car_supra,
            response.context["car_list"]
        )
        self.assertNotIn(
            self.car_volkswagen,
            response.context["car_list"]
        )

    def test_driver_username_search(self):
        self.client.force_login(self.driver)
        response = self.client.get(
            reverse("taxi:driver-list"),
            data={"username": "UsernameTest"}
        )
        self.assertIn(
            self.driver,
            response.context["driver_list"]
        )

    def test_toggle_assign_to_car(self):
        self.client.force_login(self.driver)
        response = self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car_supra.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.car_supra, self.driver.cars.all())
