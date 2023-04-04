from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverSearchForm, CarSearchForm
from taxi.models import Manufacturer, Car, Driver


class TestCarSearch(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer", country="test_country"
        )
        self.car1 = Car.objects.create(
            model="car1_test", manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="car2_test", manufacturer=self.manufacturer
        )
        self.car3 = Car.objects.create(
            model="CAR1_test", manufacturer=self.manufacturer
        )

    def test_search_car_by_model(self):
        form_data = {"model": "car1"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        queryset = Car.objects.filter(
            model__icontains=form.cleaned_data["model"]
        )

        self.assertIn(self.car1, queryset)
        self.assertNotIn(self.car2, queryset)
        self.assertIn(self.car3, queryset)


class TestDriverSearch(TestCase):
    def setUp(self):
        self.driver1 = Driver.objects.create(
            username="test_driver1",
            first_name="test_first_name1",
            last_name="test_last_name1",
            password="test_password1",
            license_number="BAC12345",
        )
        self.driver2 = Driver.objects.create(
            username="test_driver2",
            first_name="test_first_name2",
            last_name="test_last_name2",
            password="test_password2",
            license_number="BBC12345",
        )
        self.driver3 = Driver.objects.create(
            username="test_DRIVER1",
            first_name="test_first_name3",
            last_name="test_last_name3",
            password="test_password3",
            license_number="BBB12345",
        )

    def test_search_driver_by_username(self):
        form_data = {"username": "driver1"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        queryset = get_user_model().objects.filter(
            username__icontains=form.cleaned_data["username"]
        )

        self.assertIn(self.driver1, queryset)
        self.assertNotIn(self.driver2, queryset)
        self.assertIn(self.driver3, queryset)


class PublicManufacturerTest(TestCase):
    def test_list_manufacturers(self):
        res = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(res.status_code, 200)


class PublicDriverTest(TestCase):
    def test_list_drivers(self):
        res = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(res.status_code, 200)

    def test_driver_detail(self):
        res = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": 1})
        )
        self.assertNotEqual(res.status_code, 200)


class PublicCarTest(TestCase):
    def test_list_cars(self):
        res = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(res.status_code, 200)

    def test_car_detail(self):
        res = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": 1})
        )
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_driver",
            password="test_password1",
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country"
        )

    def test_retrieve_manufacturers(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(
            response, "taxi/manufacturer_list.html"
        )


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_driver",
            password="test_password1",
            license_number="BAC12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_detail(self):
        response = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_driver",
            password="test_password1",
            license_number="BAC12345",
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country"
        )
        Car.objects.create(
            model="test_model",
            manufacturer=Manufacturer.objects.get(name="test_manufacturer")
        )

    def test_retrieve_cars(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_detail(self):
        response = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")
