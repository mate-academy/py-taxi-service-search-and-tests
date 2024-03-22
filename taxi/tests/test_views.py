from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver

DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_DETAIL_URL = reverse("taxi:driver-detail", kwargs={"pk": 1})

CAR_CREATE_URL = reverse("taxi:car-create")
CAR_UPDATE_URL = reverse("taxi:car-update", kwargs={"pk": 1})

MANUFACTURER_DELETE_URL = reverse("taxi:manufacturer-delete", kwargs={"pk": 1})


class PublicViewsTest(TestCase):
    def test_login_required_to_delete_manufacturer(self):
        res = self.client.get(MANUFACTURER_DELETE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_to_create_car(self):
        res = self.client.get(CAR_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_to_update_car(self):
        res = self.client.get(CAR_UPDATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_to_see_drivers_list(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_to_see_driver_details(self):
        res = self.client.get(DRIVER_DETAIL_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateViewsTest(TestCase):
    def setUp(self) -> None:
        self.driver = Driver.objects.create_user(
            username="Test",
            license_number="ABV12345",
            first_name="Test",
            last_name="Test",
            password="Test"
        )
        self.client.force_login(self.driver)

        self.manufacturer_1 = Manufacturer.objects.create(
            name="Test  1",
            country="Test  1"
        )
        self.manufacturer_2 = Manufacturer.objects.create(
            name="Test  2",
            country="Test  2"
        )

        self.car_1 = Car.objects.create(
            manufacturer=self.manufacturer_1,
            model="Test  1"
        )
        self.car_1.drivers.add(self.driver)

        self.car_2 = Car.objects.create(
            manufacturer=self.manufacturer_2,
            model="Test  2"
        )
        self.car_2.drivers.add(self.driver)

    def test_manufacturer_deletion(self):
        response = self.client.get(MANUFACTURER_DELETE_URL)
        self.assertEqual(response.status_code, 200)

    # Tests for car's views
    def test_car_creation(self):
        response = self.client.get(CAR_CREATE_URL)
        self.assertEqual(response.status_code, 200)

    def test_car_updating(self):
        response = self.client.get(CAR_UPDATE_URL)
        self.assertEqual(response.status_code, 200)

    # Tests for driver's views
    def test_driver_list_view(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)

        driver_list = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(driver_list)
        )

    def test_driver_detail_view(self):
        response = self.client.get(DRIVER_DETAIL_URL)
        self.assertEqual(response.status_code, 200)

    # Tests for searching features

    def test_of_searching_feature_in_driver_list(self):
        self.driver_2 = Driver.objects.create_user(
            username="2 Test",
            license_number="ABV22222",
            first_name="Test 2",
            last_name="Test  2",
            password="Test  2"
        )
        self.driver_3 = Driver.objects.create_user(
            username="3 Test ",
            license_number="ABV33333",
            first_name="Test 3",
            last_name="Test 3",
            password="Test 3"
        )
        queryset_filtered = Driver.objects.all().filter(
            username__icontains="username"
        )
        response = self.client.get(DRIVER_LIST_URL, {"username": "username"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(queryset_filtered)
        )
