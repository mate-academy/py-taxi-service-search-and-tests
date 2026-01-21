from django.contrib.auth import get_user_model
from django.urls import reverse
from taxi.forms import DriverCreationForm
from taxi.models import Manufacturer, Driver, Car
from django.test import TestCase


class ModelsTests(TestCase):
    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self) -> None:
        driver = Driver.objects.create(
            username="choppa",
            first_name="Leonid",
            last_name="Popkin",
            license_number="UNIQUE001"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        car = Car.objects.create(
            model="X5",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)


class AdminPanelTest(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123"
        )
        self.client.force_login(self.admin_user)

        self.driver = Driver.objects.create(
            username="choppa",
            first_name="Leonid",
            last_name="Popkin",
            license_number="UNIQUE002"
        )

    def test_driver_in_admin_list(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, "choppa")
        self.assertContains(response, "Leonid")
        self.assertContains(response, "Popkin")


class FormTest(TestCase):
    def test_form_is_valid(self):
        form_data = {
            "username": "testuser",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
            "license_number": "LOL12345",  # ✅ валідне
            "first_name": "Pavlo",
            "last_name": "Semenikhin",
        }
        form = DriverCreationForm(data=form_data)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())


class ViewsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123",
            license_number="UNIQUE002"
        )
        self.client.force_login(self.user)

    def test_driver_list_view(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_driver_detail_view(self):
        response = self.client.get(
            reverse(
                "taxi:driver-detail",
                args=(self.user.id,)
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_manufacturer_list_view(self):
        Manufacturer.objects.create(name="Honda", country="Japan")
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Honda")

    def test_car_list_view(self):
        manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        car = Car.objects.create(model="A6", manufacturer=manufacturer)
        car.drivers.add(self.user)

        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A6")

    def test_create_manufacturer_view(self):
        response = self.client.post(reverse("taxi:manufacturer-create"), {
            "name": "Mazda",
            "country": "Japan"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Manufacturer.objects.filter(name="Mazda").exists())

    def test_driver_search(self):
        response = self.client.get(
            reverse(
                "taxi:driver-list"
            ),
            {"username": "admin"})
        self.assertContains(response, "admin")
