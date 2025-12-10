from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

MANUFACTURER_FORMAT_URL = reverse("taxi:manufacturer-list")
CAR_FORMAT_URL = reverse("taxi:car-list")
DRIVER_FORMAT_URL = reverse("taxi:driver-list")
User = get_user_model()


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_FORMAT_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="Test123!",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="BMW", country="Poland")
        Manufacturer.objects.create(name="Audi", country="Germany")
        response = self.client.get(MANUFACTURER_FORMAT_URL)
        self.assertEqual(response.status_code, 200)
        manufacturer = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="Test123!",
        )
        self.client.force_login(self.user)

    def test_create_user(self):
        form_data = {
            "username": "new_user",
            "password1": "Testuser123!",
            "password2": "Testuser123!",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ADM56984",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])


class BaseSearchTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="test",
            password="Test123!",
        )
        self.client.force_login(self.user)


class ManufacturerSearchTest(BaseSearchTestCase):
    def setUp(self):
        super().setUp()
        self.m1 = Manufacturer.objects.create(name="BMW")
        self.m2 = Manufacturer.objects.create(name="Audi")
        self.m3 = Manufacturer.objects.create(name="Mercedes")

    def test_manufacturer_search_filters_by_name(self):
        response = self.client.get(MANUFACTURER_FORMAT_URL, {"name": "bm"})

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.m1, response.context["manufacturer_list"])
        self.assertNotIn(self.m2, response.context["manufacturer_list"])
        self.assertNotIn(self.m3, response.context["manufacturer_list"])

        search = response.context["search_form"]
        self.assertEqual(search.initial["name"], "bm")

    def test_manufacturer_search_without_query_returns_all(self):
        response = self.client.get(MANUFACTURER_FORMAT_URL)
        self.assertEqual(response.status_code, 200)
        queryset = response.context["manufacturer_list"]
        self.assertCountEqual(queryset, [self.m1, self.m2, self.m3])


class CarSearchTest(BaseSearchTestCase):
    def setUp(self):
        super().setUp()
        manufacturer = Manufacturer.objects.create(name="TestBrand")
        self.c1 = Car.objects.create(model="X5", manufacturer=manufacturer)
        self.c2 = Car.objects.create(model="X3", manufacturer=manufacturer)
        self.c3 = Car.objects.create(model="Civic", manufacturer=manufacturer)

    def test_car_search_filters_by_model(self):
        response = self.client.get(CAR_FORMAT_URL, {"model": "x"})
        self.assertEqual(response.status_code, 200)
        queryset = response.context["car_list"]

        self.assertIn(self.c1, queryset)
        self.assertIn(self.c2, queryset)
        self.assertNotIn(self.c3, queryset)

        search = response.context["search_form"]
        self.assertEqual(search.initial["model"], "x")

    def test_car_search_without_query_returns_all(self):
        response = self.client.get(CAR_FORMAT_URL)
        self.assertEqual(response.status_code, 200)
        queryset = response.context["car_list"]
        self.assertCountEqual(queryset, [self.c1, self.c2, self.c3])


class DriverSearchTests(TestCase):
    def setUp(self):
        super().setUp()
        self.d1 = User.objects.create_user(
            username="bob_blue",
            password="Test123!",
            license_number="AAA11111",
        )
        self.d2 = User.objects.create_user(
            username="jane_volk",
            password="Test123!",
            license_number="AAA22222",
        )
        self.d3 = User.objects.create_user(
            username="alex",
            password="Test123!",
            license_number="AAA33333",
        )
        self.client.force_login(self.d1)

    def test_driver_search_filters_by_username(self):
        response = self.client.get(DRIVER_FORMAT_URL, {"username": "jan"})
        self.assertEqual(response.status_code, 200)
        queryset = response.context["driver_list"]
        self.assertNotIn(self.d1, queryset)
        self.assertIn(self.d2, queryset)
        self.assertNotIn(self.d3, queryset)

        search = response.context["search_form"]
        self.assertEqual(search.initial["username"], "jan")

    def test_driver_search_query_returns_all(self):
        response = self.client.get(DRIVER_FORMAT_URL)
        self.assertEqual(response.status_code, 200)
        queryset = response.context["driver_list"]
        self.assertCountEqual(queryset, [self.d1, self.d2, self.d3])
