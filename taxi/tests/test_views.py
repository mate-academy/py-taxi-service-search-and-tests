from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import SearchForm
from taxi.models import Manufacturer, Car

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
DRIVERS_URL = reverse("taxi:driver-list")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURERS_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    # @classmethod
    # def setUpTestData(cls):
    #     Manufacturer.objects.create(name="Toyota")
    #     Manufacturer.objects.create(name="Subaru")
    #     Manufacturer.objects.create(name="Mitsubishi")
    #     Manufacturer.objects.create(name="Mercedes")

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )

        self.client.force_login(self.user)

    def test_create_manufacturer(self):
        form_data = {
            "name": "test_name",
            "country": "test_country"
        }

        self.client.post(reverse("taxi:manufacturer-create"), data=form_data)
        new_manufacturer = Manufacturer.objects.get(name=form_data["name"])

        self.assertEqual(new_manufacturer.name, form_data["name"])
        self.assertEqual(new_manufacturer.country, form_data["country"])

    def test_update_manufacturer(self):
        manufacturer = Manufacturer.objects.create(name="Test Manufacturer", country="Test Country")
        new_name = "Updated Manufacturer"
        response = self.client.post(
            reverse("taxi:manufacturer-update", kwargs={"pk": manufacturer.id}),
            data={"name": new_name},
        )

        self.assertEqual(response.status_code, 200)
        manufacturer.refresh_from_db()
        updated_manufacturer = Manufacturer.objects.get(pk=manufacturer.id)
        self.assertEqual(updated_manufacturer.name, new_name)

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURERS_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_form_works(self):
        response = self.client.get(MANUFACTURERS_URL, {"title": "M"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertIsInstance(response.context["search_form"], SearchForm)
        self.assertEqual(len(response.context["manufacturer_list"]), 2)

        for manufacturer in response.context["manufacturer_list"]:
            self.assertIn("M", manufacturer.name)

    def test_search_form_empty(self):
        response = self.client.get(MANUFACTURERS_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertIsInstance(response.context["search_form"], SearchForm)
        self.assertEqual(len(response.context["manufacturer_list"]), 4)


class PublicDriverTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVERS_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverCase(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )

        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "first_name": "test First",
            "last_name": "test Last",
            "username": "test_username",
            "password1": "test12345",
            "password2": "test12345",
            "license_number": "ABC12345"
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_update_driver_license_number_with_valid_data(self):
        test_license_number = "ADM22345"
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.id}),
            data={"license_number": test_license_number},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("taxi:driver-list"))

    def test_update_driver_license_number_with_not_valid_data(self):
        test_license_number = "a5"
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.id}),
            data={"license_number": test_license_number},
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_driver(self):
        driver = get_user_model().objects.create(
            username="not_admin.user",
            license_number="NOT12345",
            first_name="Not Admin",
            last_name="User",
            password="1qazcde3",
        )
        response = self.client.post(
            reverse("taxi:driver-delete", kwargs={"pk": driver.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            get_user_model().objects.filter(id=driver.id).exists()
        )

    def test_pagination_is_five(self):
        number_of_drivers = 7

        for driver_id in range(number_of_drivers):
            get_user_model().objects.create(
                username=f"test_user_name{driver_id}",
                first_name=f"test_name{driver_id}",
                last_name=f"test_surname{driver_id}",
                license_number=f"ABD1234{driver_id}",
            )

        response = self.client.get(reverse("taxi:driver-list") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 3)

    def test_remove_driver_if_assigned_to_car(self):
        driver = get_user_model().objects.get(id=self.user.id)
        manufacturer = Manufacturer.objects.create()
        car = Car.objects.create(manufacturer=manufacturer)
        driver.cars.add(car)
        driver.save()

        self.assertTrue(
            get_user_model().objects.filter(id=driver.id).get() in car.drivers.all()
        )

        response = self.client.post(
            reverse("taxi:toggle-car-assign", kwargs={"pk": car.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            get_user_model().objects.filter(id=driver.id).get() in car.drivers.all()
        )

    def test_assign_driver_to_car_if_not_assigned(self):
        driver = get_user_model().objects.get(id=self.user.id)
        manufacturer = Manufacturer.objects.create()
        car = Car.objects.create(manufacturer=manufacturer)

        self.assertFalse(
            get_user_model().objects.filter(id=driver.id).get()
            in car.drivers.all()
        )

        response = self.client.post(
            reverse("taxi:toggle-car-assign", kwargs={"pk": car.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            get_user_model().objects.filter(id=driver.id).get()
            in car.drivers.all()
        )
