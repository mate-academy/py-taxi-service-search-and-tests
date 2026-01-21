from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import CarSearchForm
from taxi.models import Driver, Car, Manufacturer


class ToggleAssignToCarTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Driver.objects.create(username=self.client)
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer"
        )

        self.car = Car.objects.create(
            model="Test Car",
            manufacturer=self.manufacturer
        )
        self.client.login(username="testuser", password="12345")
        self.client.force_login(self.user)

    def test_toggle_assign_to_car_add(self):
        response = self.client.post(
            reverse("taxi:toggle-car-assign", args=[self.car.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("taxi:car-detail",
                    args=[self.car.id])
        )
        self.assertIn(self.car, self.user.cars.all())

    def test_toggle_assign_to_car_remove(self):
        self.user.cars.add(self.car)
        response = self.client.post(
            reverse("taxi:toggle-car-assign",
                    args=[self.car.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("taxi:car-detail",
                    args=[self.car.id])
        )

        self.assertNotIn(self.car, self.user.cars.all())


class CarListViewTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username="testuser",
            password="testpass",
            license_number="12345"
        )
        self.client.force_login(self.user)

    def test_driver_view_url_exists_at_desired_location(self):
        response = self.client.get("/drivers/")
        self.assertEqual(response.status_code, 200)

    def test_driver_view_uses_correct_template(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_lists_all_drivers(self):
        response = self.client.get(reverse("taxi:driver-list") + "?page=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 1)

    def test_driver_search_functionality(self):
        response = self.client.get(
            reverse("taxi:driver-list")
            + "?username=testuser"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 1)
        self.assertEqual(
            response.context["driver_list"][0].username,
            "testuser"
        )

    def test_driver_invalid_search_form(self):
        response = self.client.get(reverse("taxi:driver-list") + "?username=")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 1)

    def test_get_queryset_with_driver_username(self):
        response = self.client.get("/drivers/?username=testuser")
        queryset = response.context["driver_list"]

        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset[0].username, "testuser")

    def test_driver_search_case_insensitive(self):
        response = self.client.get("/drivers/?model=TEST USER")
        self.assertEqual(len(response.context["driver_list"]), 1)
