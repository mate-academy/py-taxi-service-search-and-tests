from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car

INDEX_URL = reverse("taxi:index")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_DETAIL_URL = reverse("taxi:car-detail", args=[1])


class PublicIndexTest(TestCase):
    def test_loggin_required(self):
        res = self.client.get(INDEX_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateIndexTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="12345",
            license_number="TTT12345"
        )
        self.client.force_login(self.user)

    def test_retrive_index(self):
        res = self.client.get(INDEX_URL)
        self.assertTrue(res.status_code, 200)
        self.assertContains(res, "Taxi Service Home")


class PublicManufacturerTest(TestCase):
    def test_loggin_required_manufacturer_list(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="12345",
            license_number="TTT12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="1_test_manufacturer")
        Manufacturer.objects.create(name="2_test_manufacturer")
        res = self.client.get(MANUFACTURER_URL)
        self.assertEqual(res.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_create_manufacturer(self):
        data = {"name": "test manufacturer", "country": "Test country"}
        res = self.client.post(reverse("taxi:manufacturer-create"), data=data)
        manufacturer = Manufacturer.objects.get(name="test manufacturer")
        self.assertEqual(manufacturer.name, data["name"])
        self.assertEqual(manufacturer.country, data["country"])
        self.assertRedirects(res, reverse("taxi:manufacturer-list"))

    def test_update_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="test name",
            country="test country"
        )
        update_data = {"name": "new test", "country": "test country"}
        url = reverse("taxi:manufacturer-update", args=[manufacturer.id])
        res = self.client.post(url, data=update_data)
        manufacturer.refresh_from_db()
        self.assertEqual(manufacturer.name, update_data["name"])
        self.assertRedirects(res, reverse("taxi:manufacturer-list"))

    def test_delete_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="test name",
            country="test country"
        )
        url = reverse("taxi:manufacturer-delete", args=[manufacturer.id])
        res = self.client.post(url)
        self.assertRedirects(res, reverse("taxi:manufacturer-list"))

        with self.assertRaises(Manufacturer.DoesNotExist):
            Manufacturer.objects.get(id=manufacturer.id)

    def test_search_manufacturer(self):
        Manufacturer.objects.create(name="1_test_manufacturer")
        Manufacturer.objects.create(name="2_test_manufacturer")
        res = self.client.get(
            MANUFACTURER_URL, {"name": "1_test_manufacturer"}
        )
        self.assertEqual(res.status_code, 200)
        manufacturers = Manufacturer.objects.filter(
            name__icontains="1_test_manufacturer"
        )
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers),
        )


class PublicCarTest(TestCase):
    def test_loggin_required_car_list(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_loggin_required_car_detail(self):
        res = self.client.get(CAR_DETAIL_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="12345",
            license_number="TTT12345"
        )
        self.client.force_login(self.user)

    def test_login_required_car_list(self):
        manufacturer = Manufacturer.objects.create(
            name="test name",
            country="test country"
        )
        Car.objects.create(model="test model 1", manufacturer=manufacturer)
        Car.objects.create(model="test model 2", manufacturer=manufacturer)
        res = self.client.get(CAR_URL)
        self.assertEqual(res.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(res.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_create_car(self):
        manufacturer = Manufacturer.objects.create(
            name="test name",
            country="test country"
        )
        data = {
            "model": "test_model",
            "manufacturer": manufacturer.id,
            "drivers": [self.user.id]
        }
        self.client.post(reverse("taxi:car-create"), data=data)

        car = Car.objects.get(model="test_model")
        self.assertEqual(car.model, data["model"])
        self.assertEqual(car.manufacturer, manufacturer)


class PublicDriverTest(TestCase):
    def test_login_required_driver_list(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.root_user = get_user_model().objects.create_user(
            username="test_user",
            password="test123",
            license_number="TTT12345"
        )
        self.client.force_login(self.root_user)

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "WWee123456",
            "password2": "WWee123456",
            "first_name": "test_firstname",
            "last_name": "test_lastname",
            "license_number": "WWW12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)

        user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(user.license_number, form_data["license_number"])
        self.assertEqual(user.username, form_data["username"])
        self.assertEqual(user.first_name, form_data["first_name"])
        self.assertEqual(user.last_name, form_data["last_name"])

    def test_retrieve_driver_detail(self):
        driver = get_user_model().objects.create_user(
            username="test user",
            password="12345",
            first_name="test_firstname",
            last_name="test_lastname",
            license_number="WWW12345",
        )
        url = reverse("taxi:driver-detail", args=[driver.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, driver.first_name)
        self.assertContains(response, driver.last_name)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_delete_driver(self):
        driver = get_user_model().objects.create_user(
            username="test user",
            password="12345",
            license_number="WWW12345",
        )
        url = reverse("taxi:driver-delete", args=[driver.id])
        self.client.post(url)
        with self.assertRaises(get_user_model().DoesNotExist):
            get_user_model().objects.get(id=driver.id)
