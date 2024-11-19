from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import CarSearchForm
from taxi.models import Car, Manufacturer


class PublicCarViewsTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        self.car = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer,
        )

    def test_car_list_login_required(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_car_detail_login_required(self):
        response = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": self.car.pk})
        )
        self.assertNotEqual(response.status_code, 200)

    def test_car_create_login_required(self):
        response = self.client.get(reverse("taxi:car-create"))
        self.assertNotEqual(response.status_code, 200)

    def test_car_update_login_required(self):
        response = self.client.get(
            reverse("taxi:car-update", kwargs={"pk": self.car.pk})
        )
        self.assertNotEqual(response.status_code, 200)

    def test_car_delete_login_required(self):
        response = self.client.get(
            reverse("taxi:car-delete", kwargs={"pk": self.car.pk})
        )
        self.assertNotEqual(response.status_code, 200)


class PrivateCarViewsTest(TestCase):
    def setUp(self):
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
        self.driver = get_user_model().objects.create(
            first_name="First",
            last_name="Last",
            username="Username",
            license_number="AAA12345",
            password="1qaz3edc",
        )
        self.client.force_login(self.driver)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": self.car1.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_view_renders_correct_template(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_with_empty_data(self):
        form = CarSearchForm(data={"model": ""})
        self.assertTrue(form.is_valid())

    def test_search_with_valid_data(self):
        form = CarSearchForm(data={"model": "Test"})
        self.assertTrue(form.is_valid())

    def test_search_functionality(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            data={"model": "test"}
        )
        self.assertContains(response, "Test Model")
        self.assertNotContains(response, "Another Model")

        response = self.client.get(
            reverse("taxi:car-list"),
            data={"model": "another"}
        )
        self.assertContains(response, "Another Model")
        self.assertNotContains(response, "Test Model")
