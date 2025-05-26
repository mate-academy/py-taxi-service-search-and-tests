from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Driver, Car, Manufacturer

DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testdriver",
            password="driver123",
            license_number="ABC55555"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        Driver.objects.create(
            username="user1",
            license_number="ABC12345",
            first_name="Bob",
            last_name="User",
            password="user1123"
        )
        Driver.objects.create(
            username="user2",
            license_number="ABC54321",
            first_name="Dan",
            last_name="User",
            password="user2123"
        )
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "license_number": "ABC12345",
            "first_name": "New",
            "last_name": "User",
            "password1": "123user123",
            "password2": "123user123",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_update_driver(self):
        form_data = {
            "license_number": "ABC12345"
        }
        self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.id}),
            data=form_data
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.license_number, form_data["license_number"])

    def test_toggle_assign_to_car_remove_add(self):
        manufacturer = Manufacturer.objects.create(
            name="KIA",
            country="Korea"
        )
        car = Car.objects.create(
            model="KIA Soul",
            manufacturer=manufacturer
        )
        self.client.get(
            reverse("taxi:toggle-car-assign", kwargs={"pk": car.id})
        )
        self.assertIn(car, self.user.cars.all())
        self.client.get(
            reverse("taxi:toggle-car-assign", kwargs={"pk": car.id})
        )
        self.assertNotIn(car, self.user.cars.all())
