from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

INDEX_URL = reverse("taxi:index")

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")


def get_manufacturer_update_url(manufacturer):
    return reverse(
        "taxi:manufacturer-update",
        kwargs={"pk": manufacturer.pk}
    )


def get_manufacturer_delete_url(manufacturer):
    return reverse(
        "taxi:manufacturer-delete",
        kwargs={"pk": manufacturer.pk}
    )


CAR_LIST_URL = reverse("taxi:car-list")
CAR_CREATE_URL = reverse("taxi:car-create")


def get_car_detail_url(car):
    return reverse(
        "taxi:car-detail",
        kwargs={"pk": car.pk}
    )


def get_car_update_url(car):
    return reverse(
        "taxi:car-update",
        kwargs={"pk": car.pk}
    )


def get_car_delete_url(car):
    return reverse(
        "taxi:car-delete",
        kwargs={"pk": car.pk}
    )


DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")


def get_driver_detail_url(driver):
    return reverse(
        "taxi:driver-detail",
        kwargs={"pk": driver.pk}
    )


def get_driver_update_url(driver):
    return reverse(
        "taxi:driver-update",
        kwargs={"pk": driver.pk}
    )


def get_driver_delete_url(driver):
    return reverse(
        "taxi:driver-delete",
        kwargs={"pk": driver.pk}
    )


def get_all_urls(
        manufacturer,
        car,
        driver
):
    return [
        ("index", INDEX_URL),

        ("manufacturer_list", MANUFACTURER_LIST_URL),
        ("manufacturer_create", MANUFACTURER_CREATE_URL),
        ("manufacturer_update", get_manufacturer_update_url(manufacturer)),
        ("manufacturer_delete", get_manufacturer_delete_url(manufacturer)),

        ("car_list", CAR_LIST_URL),
        ("car_create", CAR_CREATE_URL),
        ("car_detail", get_car_detail_url(car)),
        ("car_update", get_car_update_url(car)),
        ("car_update", get_car_delete_url(car)),

        ("driver_list", DRIVER_LIST_URL),
        ("driver_create", DRIVER_CREATE_URL),
        ("driver_detail", get_driver_detail_url(driver)),
        ("driver_update", get_driver_update_url(driver)),
        ("driver_delete", get_driver_delete_url(driver)),
    ]


class LoginRequiredTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer"
        )
        self.car = Car.objects.create(
            model="test model",
            manufacturer=self.manufacturer
        )
        self.user = get_user_model().objects.create_user(
            username="test username",
            password="test_password"
        )

    def test_public_access(self):
        for name, url in get_all_urls(self.manufacturer, self.car, self.user):
            with self.subTest(view=name):
                self.assertNotEqual(
                    self.client.get(url).status_code,
                    200
                )

    def test_private_access(self):
        self.client.force_login(self.user)
        for name, url in get_all_urls(self.manufacturer, self.car, self.user):
            with self.subTest(view=name):
                self.assertEqual(
                    self.client.get(url).status_code,
                    200
                )


class IndexTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Index Test Username",
            password="index_test_username",
            license_number="ABC12345"
        )
        manufacturer = Manufacturer.objects.create(
            name="test manufacturer",
            country="Test Country"
        )
        Car.objects.create(
            model="test model",
            manufacturer=manufacturer
        )
        self.client.force_login(self.user)

    def test_contex_data(self):
        response = self.client.get(INDEX_URL)
        for context_obj_name in (
            "num_drivers",
            "num_cars",
            "num_manufacturers",
            "num_visits"
        ):
            self.assertEqual(
                response.context[context_obj_name],
                1
            )


class SearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test username",
            password="test_password",
            license_number="ABC54321"
        )
        self.another_user = get_user_model().objects.create_user(
            username="test username 2",
            password="test_password123",
            license_number="ABC98765"
        )
        self.client.force_login(self.user)

        manufacturer_1 = Manufacturer.objects.create(
            name="test manufacturer 1",
            country="Test Country 1"
        )
        manufacturer_2 = Manufacturer.objects.create(
            name="test manufacturer 2",
            country="Test Country 2"
        )

        self.car_1 = Car.objects.create(
            model="test model1",
            manufacturer=manufacturer_1
        )
        self.car_2 = Car.objects.create(
            model="test model2",
            manufacturer=manufacturer_2
        )

    def test_manufacturers_cars_drivers_search(self):
        param_1, param_2 = "1", "2"

        for (
            search_attribute,
            url,
            queryset_1,
            queryset_2,
            context_name
        ) in (
                (
                    "name",
                    MANUFACTURER_LIST_URL,
                    Manufacturer.objects.filter(name__icontains=param_1),
                    Manufacturer.objects.filter(name__icontains=param_2),
                    "manufacturer_list"
                ),
                (
                    "model",
                    CAR_LIST_URL,
                    Car.objects.filter(model__icontains=param_1),
                    Car.objects.filter(model__icontains=param_2),
                    "car_list"
                ),
                (
                    "username",
                    DRIVER_LIST_URL,
                    get_user_model().objects.filter(
                        username__icontains=param_1
                    ),
                    get_user_model().objects.filter(
                        username__icontains=param_2
                    ),
                    "driver_list"
                )
        ):
            response_1 = self.client.get(
                url,
                {search_attribute: param_1}
            )
            response_2 = self.client.get(
                url,
                {search_attribute: param_2}
            )

            with self.subTest(view=context_name):
                self.assertEqual(response_1.status_code, 200)
                self.assertEqual(response_2.status_code, 200)

                self.assertEqual(
                    list(queryset_1),
                    list(response_1.context[context_name])
                )
                self.assertEqual(
                    list(queryset_2),
                    list(response_2.context[context_name])
                )

                self.assertTrue(
                    "search_form" in response_1.context
                )
                self.assertTrue(
                    "search_form" in response_2.context
                )


class ToggleCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="AssignCar Test Username",
            password="assign_car_test_username",
            license_number="ABC12345"
        )

        manufacturer = Manufacturer.objects.create(
            name="test manufacturer",
            country="Test Country"
        )
        self.car = Car.objects.create(
            model="test model",
            manufacturer=manufacturer
        )
        self.client.force_login(self.user)

    def test_toggle_assign_car_to_user(self):
        self.client.get(reverse(
            "taxi:toggle-car-assign",
            kwargs={"pk": self.car.pk}
        ))

        self.assertTrue(
            self.car in self.user.cars.all()
        )

    def test_toggle_remove_car_from_user(self):
        self.user.cars.add(self.car)
        self.client.get(reverse(
            "taxi:toggle-car-assign",
            kwargs={"pk": self.car.pk}
        ))

        self.assertTrue(
            self.car not in self.user.cars.all()
        )
