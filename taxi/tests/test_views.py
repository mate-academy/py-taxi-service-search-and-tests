from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver

INDEX_URL = reverse("taxi:index")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")
CAR_LIST_URL = reverse("taxi:car-list")
CAR_CREATE_URL = reverse("taxi:car-create")
DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")


def assert_login_required(test_case_obj, url: str):
    response = test_case_obj.client.get(url)
    test_case_obj.assertNotEquals(response.status_code, 200)


class PublicIndexTests(TestCase):
    def test_index_login_required(self):
        assert_login_required(self, INDEX_URL)


class PublicManufacturerTests(TestCase):
    def test_manufacturer_list_login_required(self):
        assert_login_required(self, MANUFACTURER_LIST_URL)

    def test_manufacturer_create_login_required(self):
        assert_login_required(self, MANUFACTURER_CREATE_URL)

    def assert_manufacturer_related_view_login_required(self, url_name):
        manufacturer = Manufacturer.objects.create(name="test_manufacturer")
        url = reverse(f"taxi:{url_name}", kwargs={"pk": manufacturer.pk})
        assert_login_required(self, url)

    def test_manufacturer_update_login_required(self):
        self.assert_manufacturer_related_view_login_required(
            "manufacturer-update"
        )

    def test_manufacturer_delete_login_required(self):
        self.assert_manufacturer_related_view_login_required(
            "manufacturer-delete"
        )


class PublicCarTests(TestCase):
    def test_car_list_login_required(self):
        assert_login_required(self, CAR_LIST_URL)

    def test_car_create_login_required(self):
        assert_login_required(self, CAR_CREATE_URL)

    def assert_car_related_view_login_required(self, url_name: str):
        manufacturer = Manufacturer.objects.create(name="test_manufacturer")
        car = Car.objects.create(manufacturer=manufacturer)
        url = reverse(f"taxi:{url_name}", kwargs={"pk": car.pk})
        assert_login_required(self, url)

    def test_car_detail_login_required(self):
        self.assert_car_related_view_login_required("car-detail")

    def test_car_update_login_required(self):
        self.assert_car_related_view_login_required("car-update")

    def test_car_delete_login_required(self):
        self.assert_car_related_view_login_required("car-delete")

    def test_car_toggle_assign_login_required(self):
        self.assert_car_related_view_login_required("toggle-car-assign")


class PublicDriverTests(TestCase):
    def test_driver_list_login_required(self):
        assert_login_required(self, DRIVER_LIST_URL)

    def test_driver_create_login_required(self):
        assert_login_required(self, DRIVER_CREATE_URL)

    def assert_driver_related_view_login_required(self, url_name: str):
        driver = Driver.objects.create(license_number="TST12345")
        url = reverse(f"taxi:{url_name}", kwargs={"pk": driver.pk})
        assert_login_required(self, url)

    def test_driver_detail_login_required(self):
        self.assert_driver_related_view_login_required("driver-detail")

    def test_driver_update_login_required(self):
        self.assert_driver_related_view_login_required("driver-update")

    def test_driver_delete_login_required(self):
        self.assert_driver_related_view_login_required("driver-delete")


class PrivateIndexTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test.user",
            password="test_password",
            license_number="TST12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_index_page(self):
        response = self.client.get(INDEX_URL)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test.user",
            password="test_password",
            license_number="TST12345"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer"
        )

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(name="test_manufacturer_1")
        Manufacturer.objects.create(name="test_manufacturer_2")
        manufacturers = Manufacturer.objects.order_by("id")
        manufacturers = Paginator(manufacturers, 5).get_page(0)
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_manufacturer_create_page(self):
        response = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertEquals(response.status_code, 200)

    def assert_retrieve_manufacturer_related_view(self, url_name: str):
        response = self.client.get(
            reverse(f"taxi:{url_name}", kwargs={"pk": self.manufacturer.pk})
        )
        self.assertEquals(response.status_code, 200)

    def test_retrieve_manufacturer_update_page(self):
        self.assert_retrieve_manufacturer_related_view("manufacturer-update")

    def test_retrieve_manufacturer_delete_page(self):
        self.assert_retrieve_manufacturer_related_view("manufacturer-delete")


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test.user",
            password="test_password",
            license_number="TST12345"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer"
        )
        self.car = Car.objects.create(manufacturer=self.manufacturer)

    def test_retrieve_car_list(self):
        Car.objects.create(manufacturer=self.manufacturer)
        Car.objects.create(manufacturer=self.manufacturer)
        cars = Car.objects.order_by("id")
        cars = Paginator(cars, 5).get_page(0)
        response = self.client.get(CAR_LIST_URL)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(response.context["car_list"]),
            list(cars)
        )

    def test_retrieve_car_create_page(self):
        response = self.client.get(CAR_CREATE_URL)
        self.assertEquals(response.status_code, 200)

    def assert_retrieve_car_related_view(self, url_name: str):
        response = self.client.get(
            reverse(f"taxi:{url_name}", kwargs={"pk": self.car.pk})
        )
        self.assertEquals(response.status_code, 200)

    def test_retrieve_car_detail_page(self):
        self.assert_retrieve_car_related_view("car-detail")

    def test_retrieve_car_update_page(self):
        self.assert_retrieve_car_related_view("car-update")

    def test_retrieve_car_delete_page(self):
        self.assert_retrieve_car_related_view("car-delete")

    def test_car_assign_driver(self):
        self.client.get(
            reverse("taxi:toggle-car-assign", kwargs={"pk": self.car.pk})
        )
        self.assertTrue(self.user in self.car.drivers.all())

    def test_car_remove_driver(self):
        self.car.drivers.add(self.user)
        self.client.get(
            reverse("taxi:toggle-car-assign", kwargs={"pk": self.car.pk})
        )
        self.assertFalse(self.user in self.car.drivers.all())


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test.user",
            password="test_password",
            license_number="TST12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver_list(self):
        Driver.objects.create()
        drivers = Driver.objects.order_by("id")
        drivers = Paginator(drivers, 5).get_page(0)
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(response.context["driver_list"]),
            list(drivers)
        )

    def test_retrieve_driver_create_page(self):
        response = self.client.get(DRIVER_CREATE_URL)
        self.assertEquals(response.status_code, 200)

    def test_driver_create(self):
        form_data = {
            "username": "test.driver",
            "license_number": "ADC12345",
            "first_name": "test_first",
            "last_name": "test_last",
            "password1": "test_password",
            "password2": "test_password",
        }
        self.client.post(DRIVER_CREATE_URL, data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )
        self.assertEquals(new_driver.first_name, form_data["first_name"])
        self.assertEquals(new_driver.last_name, form_data["last_name"])
        self.assertEquals(
            new_driver.license_number,
            form_data["license_number"]
        )

    def assert_retrieve_driver_related_view(self, url_name):
        driver = self.user
        response = self.client.get(
            reverse(f"taxi:{url_name}", kwargs={"pk": driver.pk})
        )
        self.assertEquals(response.status_code, 200)

    def test_retrieve_driver_detail_page(self):
        self.assert_retrieve_driver_related_view("driver-detail")

    def test_retrieve_driver_update_page(self):
        self.assert_retrieve_driver_related_view("driver-update")

    def test_retrieve_driver_delete_page(self):
        self.assert_retrieve_driver_related_view("driver-delete")
