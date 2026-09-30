from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

PROTECTED_URLS = (
    "taxi:index",
    "taxi:manufacturer-list",
    "taxi:car-list",
    "taxi:driver-list",
)


class PublicAccessTests(TestCase):
    def test_protected_pages_redirect_to_login(self):
        for url_name in PROTECTED_URLS:
            with self.subTest(url_name=url_name):
                url = reverse(url_name)
                response = self.client.get(url)
                self.assertRedirects(
                    response,
                    f"{reverse('login')}?next={url}",
                )


class PrivateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test.user",
            password="test12345",
            license_number="TES12345",
        )
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.car = Car.objects.create(
            model="Camry",
            manufacturer=manufacturer,
        )

    def test_protected_pages_available_for_logged_in_user(self):
        for url_name in PROTECTED_URLS:
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))
                self.assertEqual(response.status_code, 200)

    def test_car_toggle_assigns_current_user(self):
        url = reverse("taxi:toggle-car-assign", kwargs={"pk": self.car.id})
        response = self.client.post(url)
        self.assertIn(self.user, self.car.drivers.all())
        self.assertRedirects(
            response,
            reverse("taxi:car-detail", kwargs={"pk": self.car.id}),
        )

    def test_car_toggle_removes_current_user(self):
        self.car.drivers.add(self.user)
        url = reverse("taxi:toggle-car-assign", kwargs={"pk": self.car.id})
        self.client.post(url)

        self.assertNotIn(self.user, self.car.drivers.all())

    def test_create_driver_with_valid_license_number(self):
        form_data = {
            "username": "new.driver",
            "password1": "Str0ngPass123!",
            "password2": "Str0ngPass123!",
            "first_name": "New",
            "last_name": "Driver",
            "license_number": "NEW12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)

        driver = get_user_model().objects.get(username="new.driver")
        self.assertEqual(driver.license_number, "NEW12345")

    def test_create_driver_with_invalid_license_number(self):
        form_data = {
            "username": "new.driver",
            "password1": "Str0ngPass123!",
            "password2": "Str0ngPass123!",
            "license_number": "bad",
        }
        response = self.client.post(
            reverse("taxi:driver-create"),
            data=form_data,
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            get_user_model().objects.filter(username="new.driver").exists()
        )
