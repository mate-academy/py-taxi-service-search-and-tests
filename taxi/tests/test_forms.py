from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import (
    CarModelSearchForm,
    ManufacturerNameSearchForm,
    DriverUsernameSearchForm,
)
from taxi.models import Car, Manufacturer


class CarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            license_number="ADM12345",
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Lincoln",
            country="USA",
        )

    def test_create_car(self):
        response = self.client.post(
            reverse("taxi:car-create"),
            {
                "model": "Continental",
                "manufacturer": self.manufacturer.id,
                "drivers": [self.user.id],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Car.objects.get(id=self.user.cars.first().id).model, "Continental"
        )

    def test_update_car(self):
        car = Car.objects.create(
            model="Continental",
            manufacturer=self.manufacturer,
        )
        response = self.client.post(
            reverse("taxi:car-update", kwargs={"pk": car.id}),
            {
                "pk": car.id,
                "model": "Not Continental",
                "manufacturer": self.manufacturer.id,
                "drivers": [self.user.id],
            },
        )
        Car.objects.get(id=car.id).refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Car.objects.get(id=car.id).model, "Not Continental")

    def test_delete_car(self):
        car = Car.objects.create(
            model="Continental",
            manufacturer=self.manufacturer,
        )
        response = self.client.post(
            reverse("taxi:car-delete", kwargs={"pk": car.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Car.objects.filter(id=car.id).exists())


class ManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            license_number="ADM12345",
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_create_manufacturer(self):
        response = self.client.post(
            reverse(
                "taxi:manufacturer-create",
            ),
            {"name": "Lincoln", "country": "USA"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Manufacturer.objects.get(id=1).name, "Lincoln")

    def test_update_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="Lincoln",
            country="USA",
        )
        response = self.client.post(
            reverse(
                "taxi:manufacturer-update", kwargs={"pk": manufacturer.id}
            ),
            {"name": "Not Lincoln", "country": "USA"},
        )
        Manufacturer.objects.get(id=manufacturer.id).refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Manufacturer.objects.get(id=manufacturer.id).name, "Not Lincoln"
        )

    def test_delete_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="Lincoln",
            country="USA",
        )
        response = self.client.post(
            reverse("taxi:manufacturer-delete", kwargs={"pk": manufacturer.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Manufacturer.objects.filter(id=manufacturer.id).exists()
        )


class DriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            license_number="ADM12345",
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "Bobby",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
            "first_name": "Admin",
            "last_name": "User",
            "license_number": "ADM17345",
        }

        response = self.client.post(
            reverse("taxi:driver-create"), data=form_data
        )
        new_driver = get_user_model().objects.get(username="Bobby")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])
        self.assertEqual(
            new_driver.license_number, form_data["license_number"]
        )
        self.assertTrue(new_driver.check_password("1qazcde3"))

    def test_update_driver_license_number(self):
        driver = get_user_model().objects.create_user(
            username="Bob.user",
            license_number="ADM12945",
            password="1qazcde3",
        )
        response = self.client.post(
            reverse(
                "taxi:driver-update",
                kwargs={"pk": driver.id}),
            {
                "license_number": "ADM12855",
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            get_user_model().objects.get(id=driver.id).license_number,
            "ADM12855"
        )

    def test_driver_delete(self):
        driver = get_user_model().objects.create(
            username="Ivan.user",
            first_name="Ivan",
            last_name="Boss",
            password="1qazcde3",
            license_number="ADM12855",
        )
        response = self.client.post(
            reverse("taxi:driver-delete", kwargs={"pk": driver.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            get_user_model().objects.filter(id=driver.id).exists()
        )


class SearchFormTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_search_car_form(self):
        lincoln = Manufacturer.objects.create(
            name="Lincoln",
            country="USA",
        )
        toyota = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        Car.objects.create(
            model="Continental",
            manufacturer=lincoln,
        )
        Car.objects.create(
            model="Camry",
            manufacturer=toyota,
        )
        form = CarModelSearchForm(data={"car_model": "Camry"})
        form.is_valid()
        self.assertEqual(
            list(
                Car.objects.filter(
                    model__icontains=form.cleaned_data.get("car_model")
                )
            ),
            list(Car.objects.filter(model__icontains="Camry"))
        )

    def test_search_manufacturer_form(self):
        Manufacturer.objects.create(
            name="Lincoln",
            country="USA",
        )
        Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        form = ManufacturerNameSearchForm(data={"name": "Toyota"})
        form.is_valid()
        self.assertEqual(
            list(
                Manufacturer.objects.filter(
                    name__icontains=form.cleaned_data.get("name")
                )
            ),
            list(Manufacturer.objects.filter(name__icontains="Toyota"))
        )

    def test_search_driver_form(self):
        get_user_model().objects.create_user(
            username="Frank12",
            first_name="Frank",
            last_name="Franklyn",
            password="1qazcde3",
            license_number="ADM12245",
        )
        get_user_model().objects.create_user(
            username="David123",
            first_name="David",
            last_name="Danya",
            password="1qazcde3",
            license_number="ADM12355",
        )
        form = DriverUsernameSearchForm(data={"username": "David123"})
        form.is_valid()
        self.assertEqual(
            list(
                get_user_model().objects.filter(
                    username__icontains=form.cleaned_data.get("username")
                )
            ),
            list(
                get_user_model().objects.filter(
                    username__icontains="David123"
                )
            )
        )
