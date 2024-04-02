from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

DRIVER_FORMAT_URL = reverse("taxi:driver-list")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        """
        Checking possibility for non-login user have access to Driver-list
        working LoginRequiredMixin for DriverListView
        :return:
        """
        res = self.client.get(DRIVER_FORMAT_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerFormat(TestCase):
    def setUp(self) -> None:
        number_of_drivers = 7

        for driver_id in range(number_of_drivers):
            get_user_model().objects.create_user(
                username=f"Test-username {driver_id}",
                license_number="AAA1234" + str(driver_id),
                password=f"Test-001{driver_id}",
            )
        self.client.force_login(get_user_model().objects.get(pk=1))

    def test_retrieve_driver_formats(self):
        """
        Checking access login user to DriverListView page
        """
        response = self.client.get(DRIVER_FORMAT_URL)
        self.assertEqual(response.status_code, 200)
        driver_formats = get_user_model().objects.all()[:5]
        self.assertEqual(
            list(response.context["driver_list"]),
            list(driver_formats),
        )
        # checking url path to taxi/driver_list.html
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_pagination_driver_is_five(self):
        response = self.client.get(DRIVER_FORMAT_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 5)

    def test_lists_all_drivers(self):
        # Get second page and confirm it has (exactly) remaining 2 items
        response = self.client.get(DRIVER_FORMAT_URL + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 2)


class TestToggleAssignToCar(TestCase):
    def setUp(self):
        manufacturer = Manufacturer.objects.create(
            name="Audi_test",
            country="Germany_test",
        )
        self.car = Car.objects.create(
            model="Test Model",
            manufacturer=manufacturer
        )
        self.user = get_user_model().objects.create_user(
            username="Test-username",
            password="Test0012",
        )
        self.client.force_login(self.user)

    def test_toggle_assign_to_car(self):
        self.assertNotIn(self.car, self.user.cars.all())
        # response
        self.client.post(
            reverse("taxi:toggle-car-assign",
                    kwargs={"pk": self.car.pk})
        )
        self.user.refresh_from_db()
        self.assertIn(self.car, self.user.cars.all())
        # response
        self.client.post(
            reverse("taxi:toggle-car-assign",
                    kwargs={"pk": self.car.pk})
        )
        self.user.refresh_from_db()
        self.assertNotIn(self.car, self.user.cars.all())
