from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

INDEX_URL = reverse("taxi:index")


class PublicIndexViewTests(TestCase):
    def test_login_required(self):
        res = self.client.get(INDEX_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateIndexViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="LIC123"
        )
        self.client.force_login(self.user)

    def test_index_retrieve(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Car.objects.create(
            model="X5",
            manufacturer=Manufacturer.objects.first()
        )

        res = self.client.get(INDEX_URL)

        self.assertEqual(res.status_code, 200)
        self.assertIn("num_drivers", res.context)
        self.assertIn("num_cars", res.context)
        self.assertIn("num_manufacturers", res.context)
        self.assertTemplateUsed(res, "taxi/index.html")


MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerListTests(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerListTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="LIC123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Audi", country="Germany")

        res = self.client.get(MANUFACTURER_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(Manufacturer.objects.all()),
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")


CAR_LIST_URL = reverse("taxi:car-list")


class PublicCarListTests(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarListTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="LIC123"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        Car.objects.create(model="X5", manufacturer=manufacturer)
        Car.objects.create(model="X3", manufacturer=manufacturer)

        res = self.client.get(CAR_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["car_list"]),
            list(Car.objects.all()),
        )


DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicDriverListTests(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverListTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="LIC123"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        driver1 = get_user_model().objects.create_user(
            username="driver1",
            password="pass123",
            license_number="AAA111"
        )
        driver2 = get_user_model().objects.create_user(
            username="driver2",
            password="pass123",
            license_number="BBB222"
        )

        res = self.client.get(DRIVER_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["driver_list"]),
            [self.user, driver1, driver2]
        )


class PrivateDriverDetailTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="LIC123"
        )
        self.client.force_login(self.user)

    def test_driver_detail_view(self):
        url = reverse("taxi:driver-detail", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["driver"], self.user)


class PrivateManufacturerListSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="LIC123"
        )
        self.client.force_login(self.user)

    def test_manufacturer_list_filtered_by_name(self):
        bmw = Manufacturer.objects.create(name="BMW", country="Germany")
        audi = Manufacturer.objects.create(name="Audi", country="Germany")

        response = self.client.get(
            MANUFACTURER_LIST_URL,
            {"name": "BM"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            [bmw]
        )

        response = self.client.get(
            MANUFACTURER_LIST_URL,
            {"name": "Au"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            [audi]
        )


class PrivateCarListSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="LIC123"
        )
        self.client.force_login(self.user)

    def test_car_list_filtered_by_model(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        car_x5 = Car.objects.create(
            model="X5",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="A4",
            manufacturer=manufacturer
        )

        response = self.client.get(
            CAR_LIST_URL,
            {"model": "X5"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            [car_x5]
        )


class PrivateDriverListSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="LIC123"
        )
        self.client.force_login(self.user)

    def test_driver_list_filtered_by_username(self):
        driver1 = get_user_model().objects.create_user(
            username="john_doe",
            password="pass123",
            license_number="AAA111"
        )
        get_user_model().objects.create_user(
            username="alice",
            password="pass123",
            license_number="BBB222"
        )

        response = self.client.get(
            DRIVER_LIST_URL,
            {"username": "john"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            [driver1]
        )
