from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver

DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_DETAIL_URL = reverse("taxi:driver-detail", kwargs={"pk": 1})
DRIVER_CREATE_URL = reverse("taxi:driver-create")
DRIVER_UPDATE_URL = reverse("taxi:driver-update", kwargs={"pk": 1})
DRIVER_DELETE_URL = reverse("taxi:driver-delete", kwargs={"pk": 1})

CAR_LIST_URL = reverse("taxi:car-list")
CAR_DETAIL_URL = reverse("taxi:car-detail", kwargs={"pk": 1})
CAR_CREATE_URL = reverse("taxi:car-create")
CAR_UPDATE_URL = reverse("taxi:car-update", kwargs={"pk": 1})
CAR_DELETE_URL = reverse("taxi:car-delete", kwargs={"pk": 1})

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")
MANUFACTURER_UPDATE_URL = reverse("taxi:manufacturer-update", kwargs={"pk": 1})
MANUFACTURER_DELETE_URL = reverse("taxi:manufacturer-delete", kwargs={"pk": 1})


class PublicViewsTest(TestCase):
    def test_login_required_manufacturer_lit(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_manufacturer_create(self):
        res = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_manufacturer_update(self):
        res = self.client.get(MANUFACTURER_UPDATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_manufacturer_delete(self):
        res = self.client.get(MANUFACTURER_DELETE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car_lit(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car_detail(self):
        res = self.client.get(CAR_DETAIL_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car_create(self):
        res = self.client.get(CAR_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car_update(self):
        res = self.client.get(CAR_UPDATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car_delete(self):
        res = self.client.get(CAR_DELETE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_drivers_lit(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver_detail(self):
        res = self.client.get(DRIVER_DETAIL_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver_create(self):
        res = self.client.get(DRIVER_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver_update(self):
        res = self.client.get(DRIVER_UPDATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver_delete(self):
        res = self.client.get(DRIVER_DELETE_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateViewsTest(TestCase):
    def setUp(self) -> None:
        self.driver = Driver.objects.create_user(
            username="Test username",
            license_number="TES45678",
            first_name="Test name",
            last_name="Test surname",
            password="Test parol"
        )
        self.client.force_login(self.driver)

        self.manufacturer_1 = Manufacturer.objects.create(
            name="Test manufacturer name 1",
            country="Test manufacturer country 1"
        )
        self.manufacturer_2 = Manufacturer.objects.create(
            name="Test manufacturer name 2",
            country="Test manufacturer country 2"
        )

        self.car_1 = Car.objects.create(
            manufacturer=self.manufacturer_1,
            model="Test car model 1"
        )
        self.car_1.drivers.add(self.driver)

        self.car_2 = Car.objects.create(
            manufacturer=self.manufacturer_2,
            model="Test car model 2"
        )
        self.car_2.drivers.add(self.driver)

    # Tests for manufacturers views
    def test_retrieve_manufacturer_list_view(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)

        manufacturer_list = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer_list)
        )

    def test_retrieve_manufacturer_create_view(self):
        response = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_manufacturer_update_view(self):
        response = self.client.get(MANUFACTURER_UPDATE_URL)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_manufacturer_delete_view(self):
        response = self.client.get(MANUFACTURER_DELETE_URL)
        self.assertEqual(response.status_code, 200)

    # Tests for car's views
    def test_retrieve_car_list_view(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)

        manufacturer_list = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(manufacturer_list)
        )

    def test_retrieve_car_create_view(self):
        response = self.client.get(CAR_CREATE_URL)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_car_update_view(self):
        response = self.client.get(CAR_UPDATE_URL)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_car_delete_view(self):
        response = self.client.get(CAR_DELETE_URL)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_car_detail_view(self):
        response = self.client.get(CAR_DETAIL_URL)
        self.assertEqual(response.status_code, 200)

    # Tests for driver's views
    def test_retrieve_driver_list_view(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)

        driver_list = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(driver_list)
        )

    def test_retrieve_driver_create_view(self):
        response = self.client.get(DRIVER_CREATE_URL)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_driver_update_view(self):
        response = self.client.get(DRIVER_UPDATE_URL)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_driver_delete_view(self):
        response = self.client.get(DRIVER_DELETE_URL)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_driver_detail_view(self):
        response = self.client.get(DRIVER_DETAIL_URL)
        self.assertEqual(response.status_code, 200)

    # Tests for searching features
    def test_searching_manufacturer_list_view(self):
        queryset_filtered = Manufacturer.objects.filter(name__icontains="2")
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": "2"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(queryset_filtered)
        )

    def test_searching_car_list_view(self):
        queryset_filtered = Car.objects.filter(model__icontains="2")
        response = self.client.get(CAR_LIST_URL, {"model": "2"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(queryset_filtered)
        )

    def test_searching_driver_list_view(self):
        self.driver_2 = Driver.objects.create_user(
            username="2 Test username",
            license_number="TES22222",
            first_name="Test name 2",
            last_name="Test surname 2",
            password="Test parol 2"
        )
        self.driver_3 = Driver.objects.create_user(
            username="3 Test user",
            license_number="TES33333",
            first_name="Test name 3",
            last_name="Test surname 3",
            password="Test parol 3"
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
