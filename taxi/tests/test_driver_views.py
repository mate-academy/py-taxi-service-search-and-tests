from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverSearchForm
from taxi.models import Manufacturer, Car, Driver


class PublicDriverViewsTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            first_name="First",
            last_name="Last",
            username="Username",
            license_number="AAA12345",
            password="1qaz3edc",
        )

    def test_driver_list_login_required(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_detail_login_required(self):
        url = reverse("taxi:driver-detail", kwargs={"pk": self.driver.pk})
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_create_login_required(self):
        url = reverse("taxi:driver-create")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_delete_login_required(self):
        url = reverse("taxi:driver-delete", kwargs={"pk": self.driver.pk})
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_update_login_required(self):
        url = reverse("taxi:driver-update", kwargs={"pk": self.driver.pk})
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverViewsTest(TestCase):
    def setUp(self):
        self.driver1 = get_user_model().objects.create_user(
            first_name="First",
            last_name="Last",
            username="Test Username",
            license_number="AAA12345",
            password="1qaz3edc",
        )
        self.driver2 = get_user_model().objects.create_user(
            first_name="First",
            last_name="Last",
            username="Another Username",
            license_number="BBB12345",
            password="2qaz3edc",
        )
        self.driver3 = get_user_model().objects.create_user(
            first_name="First",
            last_name="Last",
            username="Third Username",
            license_number="BBB12347",
            password="2qaz3edf",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        self.car1 = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer,
        )
        self.car2 = Car.objects.create(
            model="Another Model",
            manufacturer=self.manufacturer,
        )
        self.client.force_login(self.driver1)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": self.driver1.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_view_renders_correct_template(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_with_empty_data(self):
        form = DriverSearchForm(data={"username": ""})
        self.assertTrue(form.is_valid())

    def test_with_valid_data(self):
        form = DriverSearchForm(data={"username": "another"})
        self.assertTrue(form.is_valid())

    def test_search_functionality(self):
        response = self.client.get(
            reverse("taxi:driver-list"), data={"username": "another"}
        )
        self.assertContains(response, "Another Username")
        self.assertNotContains(response, "Third Username")

        response = self.client.get(
            reverse("taxi:driver-list"), data={"username": "third"}
        )
        self.assertContains(response, "Third Username")
        self.assertNotContains(response, "Another Username")

    def test_assign_car_to_driver(self):
        self.assertNotIn(self.car1, self.driver1.cars.all())
        self.assertNotIn(self.car2, self.driver1.cars.all())

        self.driver1.cars.add(self.car1)

        self.assertIn(self.car1, self.driver1.cars.all())
        self.assertNotIn(self.car1, self.driver2.cars.all())
        self.assertNotIn(self.car2, self.driver1.cars.all())

    def test_remove_car_from_driver(self):
        self.driver1.cars.add(self.car1)

        self.assertIn(self.car1, self.driver1.cars.all())

        self.driver1.cars.remove(self.car1)
        self.assertNotIn(self.car1, self.driver1.cars.all())
