from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Manufacturer, Car
from django.forms import ModelMultipleChoiceField, CheckboxSelectMultiple
from taxi.forms import CarForm

from taxi.forms import DriverLicenseUpdateForm


class ValidLicenseNumberFormTests(TestCase):
    @staticmethod
    def create_form(test_license_number):
        return DriverLicenseUpdateForm(
            data={"license_number": test_license_number}
        )

    def test_validation_license_number_with_valid_data(self):
        self.assertTrue(self.create_form("TES12345").is_valid())

    def test_length_of_license_number_should_be_not_more_than_8(self):
        self.assertFalse(self.create_form("TES123456").is_valid())

    def test_length_of_license_number_should_be_not_less_than_8(self):
        self.assertFalse(self.create_form("TES1234").is_valid())

    def test_first_3_characters_should_be_uppercase_letters(self):
        self.assertFalse(self.create_form("TE123456").is_valid())

    def test_last_5_characters_should_be_be_digits(self):
        self.assertFalse(self.create_form("TEST2345").is_valid())


class DriverViewsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            license_number="ADM12345",
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

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


class TestAdminPanel(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            license_number="ROB12345",
            username="admin",
            password="admin123"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="pass123",
            license_number="BOB01234"
        )

    def test_list_display(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)


class TestViews(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_index(self):
        res = self.client.get(reverse("taxi:index"))
        self.assertNotEqual(res.status_code, 200)


class FormsTests(TestCase):
    def test_car_form(self):
        self.manufacturer = Manufacturer.objects.create(name="ZAZ",
                                                        country="Ukraine")
        self.driver = (get_user_model().objects.
                       create(username="driver",
                              password="pass123",
                              license_number="BOB01234"))
        form_data = {
            "model": "Daewoo",
            "manufacturer": self.manufacturer,
            "drivers": [self.driver]
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Daewoo")
        self.assertEqual(form.cleaned_data["manufacturer"], self.manufacturer)
        self.assertQuerysetEqual(
            form.cleaned_data["drivers"],
            [self.driver],
            transform=lambda x: x,
            ordered=False
        )
        field = form.fields["drivers"]
        self.assertTrue(isinstance(field, ModelMultipleChoiceField))
        self.assertTrue(isinstance(field.widget,
                                   CheckboxSelectMultiple))


class TestSearch(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            license_number="ROB12345",
            username="admin",
            password="admin123"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="pass123",
            license_number="BOB01234"
        )
        self.manufacturer = Manufacturer.objects.create(name="ZAZ",
                                                        country="Ukraine")
        self.car = Car.objects.create(
            model="Daewoo",
            manufacturer=self.manufacturer
        )
        self.car.drivers.set([self.driver])

    def test_manufacturer_empty(self):
        test_name = ""
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            data={"manufacturer-search": test_name},
        )
        queryset = Manufacturer.objects.all()
        self.assertEqual(list(response.context["manufacturer_list"]),
                         list(queryset))

    def test_manufacturer_missing(self):
        test_name = "wrong name"
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            data={"manufacturer-search": test_name},
        )
        queryset = Manufacturer.objects.filter(name=test_name)
        self.assertEqual(list(response.context["manufacturer_list"]),
                         list(queryset))

    def test_manufacturer_valid(self):
        test_name = "ZAZ"
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            data={"manufacturer-search": test_name},
        )
        queryset = Manufacturer.objects.filter(name=test_name)
        self.assertEqual(list(response.context["manufacturer_list"]),
                         list(queryset))

    def test_car_missing(self):
        test_model = "wrong model"
        response = self.client.get(
            reverse("taxi:car-list"),
            data={"car-search": test_model},
        )
        queryset = Car.objects.filter(model=test_model)
        self.assertEqual(list(response.context["car_list"]), list(queryset))

    def test_car_empty(self):
        test_model = ""
        response = self.client.get(
            reverse("taxi:car-list"),
            data={"car-search": test_model},
        )
        queryset = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]), list(queryset))

    def test_car_valid(self):
        test_model = "Daewoo"
        response = self.client.get(
            reverse("taxi:car-list"),
            data={"car-search": test_model},
        )
        queryset = Car.objects.filter(model=test_model)
        self.assertEqual(list(response.context["car_list"]), list(queryset))

    def test_driver_missing(self):
        test_username = "wrong username"
        response = self.client.get(
            reverse("taxi:driver-list"),
            data={"driver-search": test_username},
        )
        queryset = get_user_model().objects.filter(username=test_username)
        self.assertEqual(list(response.context["driver_list"]), list(queryset))

    def test_driver_empty(self):
        test_username = ""
        response = self.client.get(
            reverse("taxi:driver-list"),
            data={"driver-search": test_username},
        )
        queryset = get_user_model().objects.all()
        self.assertEqual(list(response.context["driver_list"]), list(queryset))

    def test_driver_valid(self):
        test_username = "driver"
        response = self.client.get(
            reverse("taxi:driver-list"),
            data={"driver-search": test_username},
        )
        queryset = get_user_model().objects.filter(username=test_username)
        self.assertEqual(list(response.context["driver_list"]), list(queryset))
