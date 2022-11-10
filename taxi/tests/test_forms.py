from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverLicenseUpdateForm
from taxi.models import Manufacturer, Car


class ValidLicenseNumberFromTest(TestCase):
    @staticmethod
    def create_form(test_license_number):
        return DriverLicenseUpdateForm(
            data={"license_number": test_license_number}
        )

    def test_empty_license_number(self):
        self.assertFalse(self.create_form("").is_valid())

    def test_license_number_more_than_8_characters(self):
        self.assertFalse(self.create_form("ANE1122334455").is_valid())

    def test_license_number_less_than_8_characters(self):
        self.assertFalse(self.create_form("ANE1").is_valid())

    def test_first_3_characters_uppercase(self):
        self.assertFalse(self.create_form("AnE01234").is_valid())

    def test_first_5_characters_digits(self):
        self.assertFalse(self.create_form("AN012345").is_valid())

    def test_license_number_with_valid_data(self):
        self.assertTrue(self.create_form("ANA12345").is_valid())


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test1234"
        )
        self.driver = get_user_model().objects.create_user(
            username="driver.user",
            license_number="TST12345",
            first_name="TEST",
            last_name="USER",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "test.user",
            "license_number": "NOT12345",
            "first_name": "Test Name",
            "last_name": "Test Surname",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_update_user_with_valid_license_number(self):
        test_license_number = "ADM22345"
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.driver.id}),
            data={"license_number": test_license_number},
        )
        self.assertEqual(response.status_code, 302)

    def test_update_user_with_not_valid_license_number(self):
        test_license_number = "AA4"
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.driver.id}),
            data={"license_number": test_license_number},
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_driver(self):
        response = self.client.post(
            reverse("taxi:driver-delete", kwargs={"pk": self.driver.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            get_user_model().objects.filter(id=self.driver.id).exists()
        )

    def test_search_car_form(self):
        get_user_model().objects.create_user(
            username="test.username",
            license_number="TSS23345",
            first_name="TEST",
            last_name="USER",
            password="1qazcde3",
        )
        response = self.client.get(
            reverse("taxi:driver-list") + "?model=d"
        )
        drivers = get_user_model().objects.filter(username__icontains="d")

        self.assertNotEqual(list(response.context["driver_list"]), list(
            drivers))
        self.assertEqual(len(response.context["driver_list"]), 3)
        self.assertEqual(len(drivers), 1)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            password="1qazcde3",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="Narnia",
        )

    def test_create_car(self):
        response = self.client.post(
            reverse("taxi:car-create"),
            data={
                "model": "Doors",
                "manufacturer": self.manufacturer.id,
                "drivers": [self.user.id],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Car.objects.first().model, "Doors")

    def test_update_car(self):
        car = Car.objects.create(
            model="Test",
            manufacturer=self.manufacturer,
        )
        form_data = {
            "pk": car.id,
            "model": "Test Test",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.user.id],
        }
        response = self.client.post(
            reverse("taxi:car-update", kwargs={"pk": car.id}), data=form_data
        )

        Car.objects.get(id=car.id).refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Car.objects.get(id=car.id).model, "Test Test")

    def test_delete_car(self):
        car = Car.objects.create(
            model="Test",
            manufacturer=self.manufacturer,
        )
        response = self.client.post(
            reverse("taxi:car-delete", kwargs={"pk": car.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Car.objects.filter(id=car.id).exists())

    def test_search_car_form(self):
        Car.objects.create(model="Test", manufacturer=self.manufacturer)
        Car.objects.create(model="TestModel", manufacturer=self.manufacturer)
        Car.objects.create(model="DesdModel", manufacturer=self.manufacturer)
        response = self.client.get(
            reverse("taxi:car-list") + "?model=t"
        )
        cars = Car.objects.filter(model__icontains="t")

        self.assertEqual(list(response.context["car_list"]), list(
            cars))
        self.assertEqual(Car.objects.count(), 3)
        self.assertEqual(len(cars), 2)


class ManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_create_manufacturer(self):
        form_data = {"name": "Narnia", "country": "Doors"}
        response = self.client.post(
            reverse("taxi:manufacturer-create"), data=form_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Manufacturer.objects.get(id=1).name, "Narnia")

    def test_update_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="Doors",
            country="Narnia",
        )
        form_data = {"name": "Not Doors", "country": "Not Narnia"}
        response = self.client.post(
            reverse(
                "taxi:manufacturer-update", kwargs={"pk": manufacturer.id}
            ),
            data=form_data,
        )
        Manufacturer.objects.get(id=manufacturer.id).refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Manufacturer.objects.get(id=manufacturer.id).name, "Not Doors"
        )

    def test_delete_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="Doors",
            country="Narnia",
        )
        response = self.client.post(
            reverse("taxi:manufacturer-delete", kwargs={"pk": manufacturer.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Manufacturer.objects.filter(id=manufacturer.id).exists()
        )

    def test_search_manufacturer_form(self):
        Manufacturer.objects.create(name="SanYong", country="Korea")
        Manufacturer.objects.create(name="TesYong", country="Test")
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=a"
        )
        manufacturers = Manufacturer.objects.filter(name__icontains="a")

        self.assertEqual(list(response.context["manufacturer_list"]), list(
            manufacturers))
        self.assertEqual(Manufacturer.objects.count(), 2)
        self.assertEqual(len(manufacturers), 1)
