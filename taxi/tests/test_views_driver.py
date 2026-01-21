from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import CarSearchForm, DriverSearchForm
from taxi.models import Car, Manufacturer


class PublicDriverlistTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            first_name="First",
            last_name="Last",
            username="Username",
            license_number="AAA12345",
            password="1qaz3edc",
        )

    def test_driver_detail_login_required(self):
        url = reverse("taxi:driver-detail", kwargs={"pk": self.driver.pk})
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_list(self):
        res = self.client.get(
            reverse("taxi:driver-list")
        )
        self.assertNotEqual(res.status_code, 200)

    def test_driver_update_login_required(self):
        url = reverse("taxi:driver-update", kwargs={"pk": 1})
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


class PrivateAlllistTest(TestCase):
    def setUp(self):
        self.driver1 = get_user_model().objects.create_user(
            first_name="First",
            last_name="Last",
            username=" First Username",
            license_number="BAA12345",
            password="1qaz3edc",
        )
        self.driver2 = get_user_model().objects.create_user(
            first_name="First",
            last_name="Last",
            username="Second Username",
            license_number="AAB12345",
            password="1qaz3edb",
        )
        self.driver3 = get_user_model().objects.create_user(
            first_name="First",
            last_name="Last",
            username="Third Username",
            license_number="ABA12345",
            password="1qaz3edg",
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

    def test_car_list(self):
        form = DriverSearchForm(data={"username": "another"})
        respons = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(respons.status_code, 200)
        self.assertTrue(form.is_valid())
        self.assertTemplateUsed(respons, "taxi/driver_list.html")

    def test_search_functionality(self):
        response = self.client.get(
            reverse("taxi:driver-list"), data={"username": "second"}
        )
        self.assertContains(response, "Second Username")
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
