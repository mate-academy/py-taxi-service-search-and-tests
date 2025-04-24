from faker import Faker
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import (ManufacturerNameSearchForm,
                        DriverUsernameSearchForm,
                        CarModelSearchForm)
from taxi.models import Manufacturer, Car


class ViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        fake = Faker()
        self.driver1 = get_user_model().objects.create(
            username="driver1",
            password="password",
            first_name="first_name",
            last_name="last_name",
            email="test@example.com",
            license_number="test",
        )
        self.manufacturer1 = Manufacturer.objects.create(
            name="manufacturer1",
            country="USA",
        )
        self.car1 = Car.objects.create(
            model="car1",
            manufacturer=self.manufacturer1,
        )
        self.car1.drivers.add(self.driver1)
        self.car1.save()

        self.manufacturers = []
        for _ in range(5):
            manufacturer = Manufacturer.objects.create(
                name=fake.unique.word(),
                country=fake.country(),
            )
            self.manufacturers.append(manufacturer)

        self.drivers = []
        for _ in range(5):
            driver = get_user_model().objects.create(
                username=fake.user_name(),
                password=fake.password(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                license_number=fake.unique.word(),
            )
            self.drivers.append(driver)

        self.cars = []
        for _ in range(5):
            car = Car.objects.create(
                model=fake.word(),
                manufacturer=self.manufacturer1,
            )
            car.drivers.add(self.driver1)
            car.save()
            self.cars.append(car)

    def test_toggle_assign_to_car_view(self):
        """Test that a driver can toggle the assignment of a car."""
        self.client.force_login(self.driver1)
        car_to_toggle = self.cars[0]
        self.assertIn(car_to_toggle, self.driver1.cars.all())

        response = self.client.post(
            reverse(
                "taxi:toggle-car-assign",
                kwargs={"pk": car_to_toggle.pk}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.driver1.refresh_from_db()
        self.assertNotIn(car_to_toggle, self.driver1.cars.all())

        response = self.client.post(
            reverse("taxi:toggle-car-assign", kwargs={"pk": car_to_toggle.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.driver1.refresh_from_db()
        self.assertIn(car_to_toggle, self.driver1.cars.all())

    def test_car_list_view(self):
        self.client.force_login(self.driver1)
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertEqual(len(response.context["car_list"]), 5)
        self.assertIsInstance(
            response.context["search_form"],
            CarModelSearchForm
        )

    def test_car_list_view_filtered(self):
        self.client.force_login(self.driver1)
        response = self.client.get(reverse("taxi:car-list") + "?model=car1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 1)
        self.assertIn(self.car1, response.context["car_list"])

        response = self.client.get(
            reverse("taxi:car-list") + "?model=CAR1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 1)
        self.assertIn(self.car1, response.context["car_list"])

    def test_car_list_view_login_required(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("login") + "?next=" + reverse("taxi:car-list")
        )

    def test_driver_list_view(self):
        self.client.force_login(self.driver1)
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertEqual(len(response.context["driver_list"]), 5)
        self.assertIsInstance(
            response.context["search_form"], DriverUsernameSearchForm
        )

    def test_driver_list_view_filtered(self):
        self.client.force_login(self.driver1)
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=driver1"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 1)
        self.assertIn(self.driver1, response.context["driver_list"])

        response = self.client.get(
            reverse("taxi:driver-list") + "?username=DRIVER1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 1)
        self.assertIn(self.driver1, response.context["driver_list"])

    def test_driver_list_view_login_required(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("login") + "?next=" + reverse("taxi:driver-list")
        )

    def test_manufacturer_list_view(self):
        """
        Test the ManufacturerListView without any search query.
        Verifies that all manufacturers are displayed
        and the correct template is used.
        """
        self.client.force_login(self.driver1)
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertEqual(len(response.context["manufacturer_list"]), 5)
        self.assertIsInstance(
            response.context["search_form"], ManufacturerNameSearchForm
        )

    def test_manufacturer_list_view_filtered(self):
        """
        Test the ManufacturerListView with a search query.
        Verifies that the view correctly filters manufacturers by name.
        """
        self.client.force_login(self.driver1)
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=manufacturer1"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 1)
        self.assertIn(
            self.manufacturer1, response.context["manufacturer_list"]
        )

        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=MANUFACTURER1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 1)
        self.assertIn(
            self.manufacturer1, response.context["manufacturer_list"]
        )

    def test_manufacturer_list_view_login_required(self):
        """
        Test that the ManufacturerListView requires a login.
        Verifies that an unauthenticated user is redirected to the login page.
        """
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("login") + "?next=" + reverse("taxi:manufacturer-list")
        )

    def test_index_view_authenticated(self):
        """Test the index view for an authenticated user."""
        self.client.force_login(self.driver1)
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")
        self.assertEqual(response.context["num_visits"], 1)

        # Simulate a second visit
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.context["num_visits"], 2)

    def test_index_view_unauthenticated(self):
        """Test the index view for an unauthenticated user."""
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("login") + "?next=" + reverse("taxi:index")
        )
