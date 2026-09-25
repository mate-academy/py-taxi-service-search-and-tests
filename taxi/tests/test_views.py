from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer
from taxi.tests.base import LoggedInTestCase


class LoginRequiredTests(TestCase):
    def test_pages_redirect_anonymous_user_to_login(self):
        login_url = reverse("login")
        for name in (
            "taxi:index",
            "taxi:manufacturer-list",
            "taxi:manufacturer-create",
            "taxi:car-list",
            "taxi:car-create",
            "taxi:driver-list",
            "taxi:driver-create",
        ):
            url = reverse(name)
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, f"{login_url}?next={url}")


class IndexViewTests(LoggedInTestCase):
    def test_visit_counter_increases_on_each_visit(self):
        for expected_visits in (1, 2, 3):
            response = self.client.get(reverse("taxi:index"))
            self.assertEqual(response.context["num_visits"], expected_visits)

    def test_shows_record_counts(self):
        manufacturer = Manufacturer.objects.create(name="Ford", country="USA")
        Car.objects.create(model="Focus", manufacturer=manufacturer)
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.context["num_drivers"], 1)
        self.assertEqual(response.context["num_cars"], 1)
        self.assertEqual(response.context["num_manufacturers"], 1)


class ManufacturerViewsTests(LoggedInTestCase):
    def test_create_manufacturer_redirects_to_list(self):
        response = self.client.post(
            reverse("taxi:manufacturer-create"),
            {"name": "Ford", "country": "USA"},
        )
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.assertTrue(Manufacturer.objects.filter(name="Ford").exists())

    def test_update_manufacturer(self):
        manufacturer = Manufacturer.objects.create(name="Ford", country="USA")
        url = reverse(
            "taxi:manufacturer-update", kwargs={"pk": manufacturer.pk}
        )
        response = self.client.post(
            url, {"name": "Ford Motor", "country": "USA"}
        )
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        manufacturer.refresh_from_db()
        self.assertEqual(manufacturer.name, "Ford Motor")

    def test_delete_manufacturer(self):
        manufacturer = Manufacturer.objects.create(name="Ford", country="USA")
        response = self.client.post(
            reverse("taxi:manufacturer-delete", kwargs={"pk": manufacturer.pk})
        )
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.assertFalse(
            Manufacturer.objects.filter(pk=manufacturer.pk).exists()
        )


class CarViewsTests(LoggedInTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.manufacturer = Manufacturer.objects.create(
            name="Ford", country="USA"
        )
        cls.car = Car.objects.create(
            model="Focus", manufacturer=cls.manufacturer
        )

    def test_create_page_shows_drivers_as_checkboxes(self):
        response = self.client.get(reverse("taxi:car-create"))
        self.assertEqual(response.status_code, 200)
        # crispy puts a class between "type" and "name", so match loosely.
        self.assertRegex(
            response.content.decode(),
            r'<input type="checkbox"[^>]*name="drivers"',
        )

    def test_create_car_redirects_to_list(self):
        response = self.client.post(
            reverse("taxi:car-create"),
            {
                "model": "Mustang",
                "manufacturer": self.manufacturer.pk,
                "drivers": [self.user.pk],
            },
        )
        self.assertRedirects(response, reverse("taxi:car-list"))
        car = Car.objects.get(model="Mustang")
        self.assertEqual(list(car.drivers.all()), [self.user])

    def test_delete_car(self):
        response = self.client.post(
            reverse("taxi:car-delete", kwargs={"pk": self.car.pk})
        )
        self.assertRedirects(response, reverse("taxi:car-list"))
        self.assertFalse(Car.objects.filter(pk=self.car.pk).exists())

    def test_toggle_assign_adds_and_removes_current_user(self):
        url = reverse("taxi:toggle-car-assign", kwargs={"pk": self.car.pk})
        detail_url = reverse("taxi:car-detail", kwargs={"pk": self.car.pk})

        response = self.client.get(url)
        self.assertRedirects(response, detail_url)
        self.assertIn(self.user, self.car.drivers.all())

        self.client.get(url)
        self.assertNotIn(self.user, self.car.drivers.all())


class DriverViewsTests(LoggedInTestCase):
    creation_data = {
        "username": "new.driver",
        "password1": "Str0ng-pass-42",
        "password2": "Str0ng-pass-42",
        "first_name": "New",
        "last_name": "Driver",
        "license_number": "NEW12345",
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.driver = get_user_model().objects.create_user(
            username="other.driver",
            password="test12345",
            license_number="OTH12345",
        )

    def test_create_page_renders(self):
        response = self.client.get(reverse("taxi:driver-create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="license_number"')

    def test_create_driver_redirects_to_driver_page(self):
        response = self.client.post(
            reverse("taxi:driver-create"), self.creation_data
        )
        new_driver = get_user_model().objects.get(username="new.driver")
        self.assertRedirects(response, new_driver.get_absolute_url())
        self.assertTrue(new_driver.check_password("Str0ng-pass-42"))

    def test_create_driver_with_invalid_license_is_rejected(self):
        response = self.client.post(
            reverse("taxi:driver-create"),
            {**self.creation_data, "license_number": "bad"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            get_user_model().objects.filter(username="new.driver").exists()
        )

    def test_update_license_with_valid_number(self):
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.driver.pk}),
            {"license_number": "NEW54321"},
        )
        self.assertRedirects(response, reverse("taxi:driver-list"))
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.license_number, "NEW54321")

    def test_update_license_with_invalid_number_is_rejected(self):
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.driver.pk}),
            {"license_number": "bad"},
        )
        self.assertEqual(response.status_code, 200)
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.license_number, "OTH12345")

    def test_delete_driver_redirects_to_list(self):
        response = self.client.post(
            reverse("taxi:driver-delete", kwargs={"pk": self.driver.pk})
        )
        self.assertRedirects(response, reverse("taxi:driver-list"))
        self.assertFalse(
            get_user_model().objects.filter(pk=self.driver.pk).exists()
        )

    def test_driver_list_marks_current_user(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertContains(response, "(Me)", count=1)
