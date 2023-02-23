from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test import RequestFactory
from django.urls import reverse

from taxi.models import Manufacturer
from taxi.views import ManufacturerListView

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class OnlyLoggedIn(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin123"
        )

        self.client.force_login(self.user)


class PublicManufacturerTest(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(OnlyLoggedIn, TestCase):

    def test_retrieve_manufacturers(self) -> None:
        Manufacturer.objects.create(
            name="Volkswagen",
            country="Germany"
        )
        Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_get_queryset(self):
        Manufacturer.objects.create(
            name="Volkswagen",
            country="Germany"
        )
        Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        name = "Audi"
        request = RequestFactory().get("taxi:manufacturer-list")
        request.GET = {"name": name}
        view = ManufacturerListView()
        view.request = request
        manufacturers = Manufacturer.objects.all()

        queryset = view.get_queryset()

        self.assertQuerysetEqual(queryset, (manufacturers.filter(
            name__icontains=name
        )))


class PrivateDriverTest(OnlyLoggedIn, TestCase):

    def test_create_driver(self):
        form_data = {
            "username": "test",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "Volkswagen",
            "last_name": "Germany",
            "license_number": "VOL12345"
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
