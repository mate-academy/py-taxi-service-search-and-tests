from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, ManufacturerSearchForm
from taxi.forms import DriverSearchForm, CarSearchForm
from taxi.models import Driver, Car, Manufacturer


class FormsTest(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ABC12345",
        }
        self.form = DriverCreationForm(data=self.form_data)

    def test_driver_creation_form_with_license_number_first_last_name_is_valid(self):
        self.assertTrue(self.form.is_valid())
        self.assertEqual(self.form.cleaned_data, self.form_data)


class SearchTests(TestCase):
    test_password = "1234567890"

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin_test", password=self.test_password
        )
        self.client.force_login(self.user)

        Driver.objects.create(username="user1", license_number="ABC12346")
        Driver.objects.create(username="user2", license_number="CBA54321")
        self.driver_response = self.client.get(reverse("taxi:driver-list"), {"username": "user2"})

        manufacturer = Manufacturer.objects.create(name="test_manufacturer")
        self.manufacturer_response = self.client.get(reverse("taxi:manufacturer-list"),
                                                     {"name": "test_manufacturer"})
        driver = get_user_model().objects.create(
            username="driver1",
            password=self.test_password,
            first_name="test_firstname",
            last_name="test_lastname",
            license_number="ABC12345",
        )
        car1 = Car.objects.create(model="car1", manufacturer=manufacturer)
        car2 = Car.objects.create(model="car2", manufacturer=manufacturer)
        car1.drivers.set([driver])
        car2.drivers.set([driver])

        self.car_response = self.client.get(reverse("taxi:car-list"), {"model": "car1"})

    def test_search_driver_by_username_status_code_is_200(self):
        self.assertEqual(self.driver_response.status_code, 200)

    def test_search_driver_by_username_form_instance_is_created(self):
        self.assertIsInstance(self.driver_response.context["search_form"],
                              DriverSearchForm)

    def test_search_driver_by_username_returns_expected_queryset(self):
        self.assertQuerysetEqual(
            self.driver_response.context["object_list"],
            Driver.objects.filter(username__icontains="user2"),
        )

    def test_search_car_by_model_status_code_is_200(self):
        self.assertEqual(self.car_response.status_code, 200)

    def test_search_car_by_model_form_instance_is_created(self):
        self.assertIsInstance(self.car_response.context["search_form"],
                              CarSearchForm)

    def test_search_car_by_model_returns_expected_queryset(self):
        self.assertQuerysetEqual(
            self.car_response.context["object_list"],
            Car.objects.filter(model__icontains="car1"),
        )

    def test_search_manufacturer_by_name_status_code_is_200(self):
        self.assertEqual(self.manufacturer_response.status_code, 200)

    def test_search_manufacturer_by_name_form_instance_is_created(self):
        self.assertIsInstance(self.manufacturer_response.context["search_form"],
                              ManufacturerSearchForm)

    def test_search_manufacturer_by_name_returns_expected_queryset(self):
        self.assertQuerysetEqual(
            self.manufacturer_response.context["object_list"],
            Manufacturer.objects.filter(name__icontains="test_manufacturer"),
        )
