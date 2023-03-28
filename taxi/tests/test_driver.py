from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class PublicDriverTests(TestCase):
    def test_driver_list_login_required(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_driver_create_login_required(self):
        url = reverse("taxi:driver-create")
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_driver_update_login_required(self):
        user = get_user_model().objects.create_user(
            username="test_user",
            password="test12345",
            license_number="ABC12345"
        )
        url = reverse("taxi:driver-update", args=[user.id])
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_delete_delete_login_required(self):
        user = get_user_model().objects.create_user(
            username="test_user",
            password="test12345",
            license_number="ABC12345"
        )
        url = reverse("taxi:driver-delete", args=[user.id])
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_superuser(
            username="admin_user",
            password="test98765"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver_list(self):
        get_user_model().objects.create_user(
            username="test_1",
            password="test12345",
            license_number="ABC12345")
        get_user_model().objects.create_user(
            username="test_2",
            password="test54321",
            license_number="ABC54321"
        )

        url = reverse("taxi:driver-list")
        response = self.client.get(url)

        users = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(users)
        )

    def test_retrieve_driver_detail_page(self):
        user = get_user_model().objects.create_user(
            username="test_1",
            password="test12345",
            license_number="ABC12345")
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        car = Car.objects.create(
            model="Camry",
            manufacturer=manufacturer
        )
        car.drivers.add(user)

        url = reverse("taxi:driver-detail", args=[user.id])
        response = self.client.get(url)
        print(user)

        cars = user.cars.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver"].cars.all()),
            list(cars)
        )

    def test_driver_search_by_username(self):
        get_user_model().objects.create_user(
            username="test_1",
            password="test12345",
            license_number="ABC12345")
        get_user_model().objects.create_user(
            username="test_2",
            password="test54321",
            license_number="ABC54321"
        )
        get_user_model().objects.create_user(
            username="test_12",
            password="test12354",
            license_number="XYZ12345"
        )

        url = reverse("taxi:driver-list") + "?username=2"
        response = self.client.get(url)

        username_contains_a = get_user_model().objects.filter(
            username__icontains="2"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(username_contains_a)
        )

    def test_driver_create(self):
        data = {
            "username": "test_1",
            "password1": "test12345",
            "password2": "test12345",
            "license_number": "ABC12345",
            "first_name": "",
            "last_name": "",
        }
        url = reverse("taxi:driver-create")
        response = self.client.post(url, data=data)

        new_user = get_user_model().objects.last()
        self.assertEqual(new_user.username, "test_1")
        self.assertRedirects(response, reverse(
            "taxi:driver-detail", args=[new_user.id]
        ))

    def test_driver_update(self):
        user = get_user_model().objects.create_user(
            username="test_1",
            password="test12345",
            license_number="ABC12345"
        )
        data = {
            "username": user.username,
            "password1": user.password,
            "password2": user.password,
            "license_number": "XYZ56789",
            "first_name": "",
            "last_name": "",
        }
        url = reverse("taxi:driver-update", args=[user.id])
        response = self.client.post(url, data=data)

        self.assertEqual(
            get_user_model().objects.get(id=user.id).license_number, "XYZ56789"
        )
        self.assertRedirects(response, reverse("taxi:driver-list"))

    def test_driver_delete(self):
        user = get_user_model().objects.create_user(
            username="test_1",
            password="test12345",
            license_number="ABC12345"
        )
        url = reverse("taxi:driver-delete", args=[user.id])
        response = self.client.post(url)

        users = get_user_model().objects.all()

        self.assertFalse(user in users)
        self.assertRedirects(response, reverse("taxi:driver-list"))

    def test_assign_to_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        car = Car.objects.create(model="Camry", manufacturer=manufacturer)

        url = reverse("taxi:toggle-car-assign", args=[car.id])
        response = self.client.get(url)

        self.assertEqual(list(car.drivers.all()), [response.wsgi_request.user])
        self.assertRedirects(
            response, reverse("taxi:car-detail", args=[car.id])
        )

    def test_discharge_from_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        car = Car.objects.create(model="Camry", manufacturer=manufacturer)
        car.drivers.add(self.user)

        url = reverse("taxi:toggle-car-assign", args=[car.id])
        response = self.client.get(url)

        self.assertEqual(list(car.drivers.all()), [])
        self.assertRedirects(
            response, reverse("taxi:car-detail", args=[car.id])
        )
