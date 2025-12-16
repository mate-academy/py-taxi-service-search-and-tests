from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")
MANUFACTURER_UPDATE_URL = reverse("taxi:manufacturer-update",
                                  kwargs={"pk": 1})
MANUFACTURER_DELETE_URL = reverse("taxi:manufacturer-delete",
                                  kwargs={"pk": 1})

CAR_LIST_URL = reverse("taxi:car-list")
CAR_DETAIL_URL = reverse("taxi:car-detail", kwargs={"pk": 1})
CAR_CREATE_URL = reverse("taxi:car-create")
CAR_UPDATE_URL = reverse("taxi:car-update", kwargs={"pk": 1})
CAR_DELETE_URL = reverse("taxi:car-delete", kwargs={"pk": 1})

DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_DETAIL_URL = reverse("taxi:driver-detail", kwargs={"pk": 1})
DRIVER_CREATE_URL = reverse("taxi:driver-create")
DRIVER_UPDATE_URL = reverse("taxi:driver-update", kwargs={"pk": 1})
DRIVER_DELETE_URL = reverse("taxi:driver-delete", kwargs={"pk": 1})


class PublicManufacturerTest(TestCase):

    def test_list_page_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_create_page_login_required(self):
        res = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_update_page_login_required(self):
        res = self.client.get(MANUFACTURER_UPDATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_delete_page_login_required(self):
        res = self.client.get(MANUFACTURER_DELETE_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_username",
            first_name="first_name",
            last_name="last_name",
            license_number="DSA12345",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="manu1", country="coun1")
        Manufacturer.objects.create(name="manu2", country="coun2")
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(res.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(list(res.context["manufacturer_list"]),
                         list(manufacturers))
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_create_manufacturer(self):
        before_count = Manufacturer.objects.count()
        data = {"name": "test1", "country": "test"}
        self.client.post(MANUFACTURER_CREATE_URL, data)
        after_count = Manufacturer.objects.count()
        self.assertEqual(after_count, before_count + 1)

    def test_update_manufacturer(self):
        before_update = Manufacturer.objects.create(name="123", country="123")
        data = {"name": "1234", "country": "123"}
        self.client.post(MANUFACTURER_UPDATE_URL, data)
        after_update = Manufacturer.objects.get(id=1)
        self.assertNotEqual(before_update.name, after_update.name)

    def test_delete_manufacturer(self):
        Manufacturer.objects.create(name="123", country="123")
        before_count = Manufacturer.objects.count()
        self.client.post(MANUFACTURER_DELETE_URL)
        after_count = Manufacturer.objects.count()
        self.assertNotEqual(before_count, after_count)

    def test_search_cars(self):
        for i in range(20):
            Manufacturer.objects.create(
                name=f"test_name{i}",
                country="Some country")
        res = self.client.get(MANUFACTURER_LIST_URL, {"name": "1"})
        for manufacturer in res.context["manufacturer_list"]:
            self.assertIn("1", manufacturer.name)


class PublicCarTest(TestCase):

    def test_list_page_login_required(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_detail_page_login_required(self):
        res = self.client.get(CAR_DETAIL_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_create_page_login_required(self):
        res = self.client.get(CAR_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_update_page_login_required(self):
        res = self.client.get(CAR_UPDATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_delete_page_login_required(self):
        res = self.client.get(CAR_DELETE_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_username",
            first_name="first_name",
            last_name="last_name",
            license_number="DSA12345",
            password="test123"
        )
        Manufacturer.objects.create(name="manu1", country="coun1")
        car = Car.objects.create(model="test_model", manufacturer_id=1)
        car.drivers.add(self.user)
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertEqual(res.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(list(res.context["car_list"]),
                         list(cars))
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_retrieve_concrete_car(self):
        car = Car.objects.get(id=1)
        res = self.client.get(CAR_DETAIL_URL)
        self.assertEqual(res.context["car"], car)

    def test_create_car(self):
        before_count = Car.objects.count()
        data = {"model": "test1", "manufacturer": 1, "drivers": 1}
        self.client.post(CAR_CREATE_URL, data)
        after_count = Car.objects.count()
        self.assertEqual(after_count, before_count + 1)

    def test_update_car(self):
        before_update = Car.objects.get(id=1)
        data = {"model": "updated", "manufacturer": 1, "drivers": 1}
        self.client.post(CAR_UPDATE_URL, data)
        after_update = Car.objects.get(id=1)
        self.assertNotEqual(before_update.model, after_update.model)

    def test_delete_car(self):
        before_count = Car.objects.count()
        self.client.post(CAR_DELETE_URL)
        after_count = Car.objects.count()
        self.assertNotEqual(before_count, after_count)

    def test_search_cars(self):
        for i in range(20):
            Car.objects.create(model=f"test_model{i}", manufacturer_id=1)
        res = self.client.get(CAR_LIST_URL, {"model": "1"})
        for car in res.context["car_list"]:
            self.assertIn("1", car.model)


class PublicDriverTest(TestCase):

    def test_list_page_login_required(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_detail_page_login_required(self):
        res = self.client.get(DRIVER_DETAIL_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_create_page_login_required(self):
        res = self.client.get(DRIVER_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_update_page_login_required(self):
        res = self.client.get(DRIVER_UPDATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_delete_page_login_required(self):
        res = self.client.get(DRIVER_DELETE_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_username",
            first_name="first_name",
            last_name="last_name",
            license_number="DSA12345",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(res.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(list(res.context["driver_list"]),
                         list(drivers))
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_search_drivers(self):
        for i in range(20):
            get_user_model().objects.create_user(
                username=f"test_username{i}",
                first_name="first_name",
                last_name="last_name",
                license_number=f"DSA1{i}3{i}5",
                password="test123"
            )
        res = self.client.get(DRIVER_LIST_URL, {"username": "1"})
        for driver in res.context["driver_list"]:
            self.assertIn("1", driver.username)

    def test_retrieve_concrete_driver(self):
        driver = Driver.objects.get(id=1)
        res = self.client.get(DRIVER_DETAIL_URL)
        self.assertEqual(res.context["driver"], driver)

    def test_create_driver(self):
        before_count = Driver.objects.count()
        data = {"username": "test1",
                "license_number": "DSS12345",
                "first_name": "213",
                "last_name": "213",
                "password1": "wdaszwdas1234",
                "password2": "wdaszwdas1234"}
        self.client.post(DRIVER_CREATE_URL, data)
        after_count = Driver.objects.count()
        self.assertEqual(after_count, before_count + 1)

    def test_update_driver(self):
        before_update = Driver.objects.get(id=1)
        data = {"license_number": "DQS12345"}
        self.client.post(DRIVER_UPDATE_URL, data)
        after_update = Driver.objects.get(id=1)
        self.assertNotEqual(before_update.license_number,
                            after_update.license_number)

    def test_delete_driver(self):
        before_count = Driver.objects.count()
        self.client.post(DRIVER_DELETE_URL)
        after_count = Driver.objects.count()
        self.assertNotEqual(before_count, after_count)
