from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicViewsTests(TestCase):
    def test_manufacturer_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_driver_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_car_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_name1",
            password="password1",
            license_number="ABC11111",
        )
        self.client.force_login(self.user)

        Manufacturer.objects.create(name="test_name1", country="test_country1")
        Manufacturer.objects.create(name="test_name2", country="test_country2")
        Manufacturer.objects.create(name="test_name3", country="test_country3")
        Manufacturer.objects.create(name="test_name4", country="test_country4")
        Manufacturer.objects.create(name="test_name5", country="test_country5")

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_is_case_insensitive(self):
        response = self.client.get(MANUFACTURER_URL, {"name": "TEST_NAME1"}, )

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            [Manufacturer.objects.get(name="test_name1")]
        )

    def test_search_with_no_matches_returns_empty_list(self):
        response = self.client.get(MANUFACTURER_URL, {"name": "wrong_name"}, )

        self.assertEqual(
            len(response.context["manufacturer_list"]),
            0
        )

    def test_search_form_preserves_search_value(self):
        response = self.client.get(MANUFACTURER_URL, {"name": "TEST"}, )

        self.assertEqual(
            response.context["search_form"].initial["name"],
            "TEST"
        )

    def test_second_page_contains_remaining_manufacturers(self):
        Manufacturer.objects.create(name="test_name6", country="test_country6")
        Manufacturer.objects.create(name="test_name7", country="test_country7")
        response = self.client.get(MANUFACTURER_URL, {"page": 2}, )

        self.assertEqual(
            len(response.context["manufacturer_list"]),
            2,
        )


class PrivateDriverViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_name1",
            password="password1",
            license_number="ABC11111",
        )
        self.client.force_login(self.user)

        get_user_model().objects.create(
            username="test_name2",
            password="password2",
            license_number="ABC11112"
        )
        get_user_model().objects.create(
            username="test_name3",
            password="password3",
            license_number="ABC11113"
        )
        get_user_model().objects.create(
            username="test_name4",
            password="password4",
            license_number="ABC11114"
        )
        get_user_model().objects.create(
            username="test_name5",
            password="password5",
            license_number="ABC11115"
        )

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_URL)

        self.assertEqual(response.status_code, 200)
        drivers = get_user_model().objects.all()

        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_is_case_insensitive(self):
        response = self.client.get(DRIVER_URL, {"username": "TEST_NAME1"}, )

        self.assertEqual(
            list(response.context["driver_list"]),
            [get_user_model().objects.get(username="test_name1")]
        )

    def test_search_with_no_matches_returns_empty_list(self):
        response = self.client.get(DRIVER_URL, {"username": "wrong_name"}, )

        self.assertEqual(
            len(response.context["driver_list"]),
            0
        )

    def test_search_form_preserves_search_value(self):
        response = self.client.get(DRIVER_URL, {"username": "TEST"}, )

        self.assertEqual(
            response.context["search_form"].initial["username"],
            "TEST"
        )

    def test_second_page_contains_remaining_manufacturers(self):
        get_user_model().objects.create(
            username="test_name6",
            password="password6",
            license_number="ABC11116"
        )
        get_user_model().objects.create(
            username="test_name7",
            password="password7",
            license_number="ABC11117"
        )
        response = self.client.get(DRIVER_URL, {"page": 2}, )

        self.assertEqual(
            len(response.context["driver_list"]),
            2,
        )


class PrivateCarViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_name1",
            password="password1",
            license_number="ABC11111",
        )
        self.client.force_login(self.user)

        manufacturers = [
            Manufacturer.objects.create(
                name="test_name1",
                country="test_country1"
            ),
            Manufacturer.objects.create(
                name="test_name2",
                country="test_country2"
            ),
            Manufacturer.objects.create(
                name="test_name3",
                country="test_country3"
            ),
            Manufacturer.objects.create(
                name="test_name4",
                country="test_country4"
            ),
            Manufacturer.objects.create(
                name="test_name5",
                country="test_country5"
            )
        ]

        drivers = [
            self.user,
            get_user_model().objects.create(
                username="test_name2",
                password="password2",
                license_number="ABC11112"
            ),
            get_user_model().objects.create(
                username="test_name3",
                password="password3",
                license_number="ABC11113"
            ),
            get_user_model().objects.create(
                username="test_name4",
                password="password4",
                license_number="ABC11114"
            ),
            get_user_model().objects.create(
                username="test_name5",
                password="password5",
                license_number="ABC11115"
            )

        ]

        Car.objects.create(
            model="test_model1",
            manufacturer=manufacturers[0]
        ).drivers.add(drivers[0])
        Car.objects.create(
            model="test_model2",
            manufacturer=manufacturers[1]
        ).drivers.add(*drivers[:1])
        Car.objects.create(
            model="test_model3",
            manufacturer=manufacturers[2]
        ).drivers.add(*drivers[:2])
        Car.objects.create(
            model="test_model4",
            manufacturer=manufacturers[3]
        ).drivers.add(*drivers[:3])
        Car.objects.create(
            model="test_model5",
            manufacturer=manufacturers[4]
        ).drivers.add(*drivers[:4])

    def test_retrieve_cars(self):
        response = self.client.get(CAR_URL)

        self.assertEqual(response.status_code, 200)
        drivers = Car.objects.all()

        self.assertEqual(
            list(response.context["car_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_is_case_insensitive(self):
        response = self.client.get(CAR_URL, {"model": "TEST_MODEL1"}, )

        self.assertEqual(
            list(response.context["car_list"]),
            [Car.objects.get(model="test_model1")]
        )

    def test_search_with_no_matches_returns_empty_list(self):
        response = self.client.get(CAR_URL, {"model": "wrong_model"}, )

        self.assertEqual(
            len(response.context["car_list"]),
            0
        )

    def test_search_form_preserves_search_value(self):
        response = self.client.get(CAR_URL, {"model": "TEST"}, )

        self.assertEqual(
            response.context["search_form"].initial["model"],
            "TEST"
        )
