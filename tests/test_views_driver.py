from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


DRIVER_URL = reverse("taxi:driver-list")


class PublicFormatTest(TestCase):

    def test_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "new_first_name",
            "last_name": "new_last_name",
            "license_number": "TES12345",
        }
        response = self.client.post(
            reverse("taxi:driver-create"),
            data=form_data
        )
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
        self.assertRedirects(response, f"/drivers/{new_user.pk}/")

    def test_query_search_filter_by_part_of_model(self):
        driver1 = get_user_model().objects.create(
            username="new_user1",
            first_name="test_first_name1",
            last_name="test_last_name1",
            license_number="TEX12345",
        )
        driver2 = get_user_model().objects.create(
            username="new_user2",
            first_name="test_first_name2",
            last_name="test_last_name2",
            license_number="TED12345",
        )

        response = self.client.get("/drivers/", {"username": "user"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["object_list"]),
            [driver1, driver2]
        )

    def test_search_with_empty_query(self):
        response = self.client.get("/drivers/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["object_list"]),
            get_user_model().objects.count()
        )

    def test_search_with_invalid_data(self):
        response = self.client.get("/drivers/", {"username": "model"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["object_list"]), 0)

    def test_toggle_assign_to_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Audi_test",
            country="Germany_test",
        )
        car = Car.objects.create(
            model="Test Model",
            manufacturer=manufacturer
        )

        self.assertNotIn(car, self.user.cars.all())
        self.client.post(
            reverse("taxi:toggle-car-assign",
                    kwargs={"pk": car.pk})
        )
        self.user.refresh_from_db()
        self.assertIn(car, self.user.cars.all())
        self.client.post(
            reverse("taxi:toggle-car-assign",
                    kwargs={"pk": car.pk})
        )
        self.user.refresh_from_db()
        self.assertNotIn(car, self.user.cars.all())
