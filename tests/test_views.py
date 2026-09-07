from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car

INDEX_URL = reverse("taxi:index")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")
MANUFACTURER_UPDATE_URL = reverse("taxi:manufacturer-update", args=[1])
MANUFACTURER_DELETE_URL = reverse("taxi:manufacturer-delete", args=[1])
CAR_LIST_URL = reverse("taxi:car-list")
CAR_DETAILS_URL = reverse("taxi:car-detail", args=[1])
CAR_CREATE_URL = reverse("taxi:car-create")
CAR_UPDATE_URL = reverse("taxi:car-update", args=[1])
CAR_DELETE_URL = reverse("taxi:car-delete", args=[1])
DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_DETAILS_URL = reverse("taxi:driver-detail", args=[1])
DRIVER_CREATE_URL = reverse("taxi:driver-create")
DRIVER_UPDATE_URL = reverse("taxi:driver-update", args=[1])
DRIVER_DELETE_URL = reverse("taxi:driver-delete", args=[1])


class PublicIndexTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_index_login_required(self):
        res = self.client.get(INDEX_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateIndexTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="testtest123"
        )
        self.client.force_login(self.user)

    def test_index_counts(self):
        Manufacturer.objects.create(name="A", country="B")
        Car.objects.create(
            model="X",
            manufacturer=Manufacturer.objects.first()
        )

        self.client.force_login(self.user)
        response = self.client.get(INDEX_URL)

        self.assertEqual(response.context["num_manufacturers"], 1)
        self.assertEqual(response.context["num_cars"], 1)
        self.assertEqual(response.context["num_drivers"], 1)


class PublicManufacturerTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_manufacturer_login_required(self):
        Manufacturer.objects.create(name="test", country="test_country")
        urls = [
            MANUFACTURER_LIST_URL,
            MANUFACTURER_CREATE_URL,
            MANUFACTURER_UPDATE_URL,
            MANUFACTURER_DELETE_URL,
        ]

        for url in urls:
            res = self.client.get(url)
            self.assertNotEqual(res.status_code, 200, msg=f"Failed at {url}")


class PrivateManufacturerTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="testtest123"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )

    def test_login_manufacturers(self):
        Manufacturer.objects.create(
            name="test_name1",
            country="test_county1"
        )
        Manufacturer.objects.create(
            name="test_name2",
            country="test_county2"
        )
        urls = [
            MANUFACTURER_LIST_URL,
            MANUFACTURER_CREATE_URL,
            MANUFACTURER_UPDATE_URL,
            MANUFACTURER_DELETE_URL,
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, msg=f"Failed at {url}")

    def test_create_manufacturer(self):
        url = reverse("taxi:manufacturer-create")

        data = {
            "name": "BMW",
            "country": "Germany"
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Manufacturer.objects.filter(name="BMW", country="Germany").exists()
        )

    def test_update_manufacturer(self):
        url = reverse("taxi:manufacturer-update", args=[self.manufacturer.id])
        data = {
            "name": "Audi Updated",
            "country": "Germany"
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)

        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, "Audi Updated")

    def test_delete_manufacturer(self):
        url = reverse("taxi:manufacturer-delete", args=[self.manufacturer.id])

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Manufacturer.objects.filter(id=self.manufacturer.id).exists()
        )

    def test_manufacturer_search(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Audi", country="Germany")

        response = self.client.get(MANUFACTURER_LIST_URL, {"data": "bm"})
        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Audi")

    def test_search_form_in_context(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertIn("search_form", response.context)

    def test_pagination_is_five(self):
        for i in range(10):
            Manufacturer.objects.create(name=f"m{i}", country="c")

        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(len(response.context["manufacturer_list"]), 5)


class PublicCarTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        Car.objects.create(
            model="test_model",
            manufacturer=manufacturer
        )
        urls = [CAR_CREATE_URL, CAR_DELETE_URL,
                CAR_UPDATE_URL, CAR_DETAILS_URL]
        for url in urls:
            res = self.client.get(url)
            self.assertNotEqual(
                res.status_code,
                200, msg=f"Failed at {url}"
            )


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_name",
            password="test_password"
        )
        self.client.force_login(self.user)

    def test_login_car(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        Car.objects.create(
            model="test_car1",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="test_car2",
            manufacturer=manufacturer
        )
        urls = [CAR_CREATE_URL, CAR_DELETE_URL,
                CAR_UPDATE_URL, CAR_DETAILS_URL]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(
                response.status_code,
                200, msg=f"Failed at {url}"
            )

    def test_car_search(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        Car.objects.create(model="Tank", manufacturer=manufacturer)
        Car.objects.create(model="Bicycle", manufacturer=manufacturer)
        response = self.client.get(CAR_LIST_URL, {"data": "ta"})
        self.assertContains(response, "Tank")
        self.assertNotContains(response, "Bicycle")

    def test_search_form_in_context(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertIn("search_form", response.context)

    def test_pagination_is_five(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        for i in range(10):
            Car.objects.create(model=f"test_car{i}", manufacturer=manufacturer)

        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(len(response.context["car_list"]), 5)

    def test_create_car(self):
        url = reverse("taxi:car-create")
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        data = {
            "model": "test_car",
            "manufacturer": manufacturer.id,
            "drivers": [self.user.id]
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)

        car = Car.objects.get(model="test_car")
        self.assertEqual(car.manufacturer, manufacturer)

    def test_update_car(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country",
        )
        car = Car.objects.create(
            model="test_change_name",
            manufacturer=manufacturer
        )
        url = reverse("taxi:car-update", args=[car.id])
        data = {
            "model": "test_car",
            "manufacturer": manufacturer.id,
            "drivers": [self.user.id]
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)

        car.refresh_from_db()
        self.assertEqual(car.model, "test_car")

    def test_delete_car(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        car = Car.objects.create(model="test_model", manufacturer=manufacturer)
        url = reverse("taxi:car-delete", args=[car.id])

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Car.objects.filter(id=car.id).exists()
        )


class PublicDriverTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        urls = [DRIVER_CREATE_URL, DRIVER_DELETE_URL,
                DRIVER_DETAILS_URL, DRIVER_UPDATE_URL]
        for url in urls:
            response = self.client.get(url)
            self.assertNotEqual(
                response.status_code,
                200, msg=f"Failed at {url}"
            )


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="testtest123"
        )
        self.client.force_login(self.user)

    def test_login_drivers(self):
        urls = [DRIVER_CREATE_URL, DRIVER_DELETE_URL,
                DRIVER_DETAILS_URL, DRIVER_UPDATE_URL]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, msg=f"Failed at {url}")

    def test_driver_search(self):
        get_user_model().objects.create_user(
            username="cooldriver",
            password="coolpassword67",
            license_number="GGG55555")
        get_user_model().objects.create_user(
            username="guy",
            password="password42",
            license_number="GGG55556"
        )

        response = self.client.get(DRIVER_LIST_URL, {"data": "cool"})
        self.assertContains(response, "cooldriver")
        self.assertNotContains(response, "guy")

    def test_driver_search_form_in_context(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertIn("search_form", response.context)

    def test_driver_list_pagination_is_five(self):
        for i in range(10):
            get_user_model().objects.create_user(username=f"test_user{i}",
                                                 password="test123123",
                                                 license_number=f"GGG5555{i}"
                                                 )
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(len(response.context["driver_list"]), 5)

    def test_create_driver(self):
        url = reverse("taxi:driver-create")
        data = {
            "username": "test_user",
            "password1": "test_password123",
            "password2": "test_password123",
            "license_number": "GGG77777",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            get_user_model().objects.filter(username="test_user").exists()
        )

    def test_update_driver(self):
        driver = get_user_model().objects.create_user(
            username="change_name_test",
            password="test_password",
            license_number="GGG88888",
        )
        url = reverse("taxi:driver-update", args=[driver.id])
        data = {
            "license_number": "GGG77777",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)

        driver.refresh_from_db()

        self.assertEqual(driver.license_number, "GGG77777")

    def test_delete_driver(self):
        driver = get_user_model().objects.create_user(
            username="change_name_test",
            password="test_password",
            license_number="GGG88888",
        )
        url = reverse("taxi:driver-delete", args=[driver.id])

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            get_user_model().objects.filter(id=driver.id).exists()
        )


class ToggleAssignTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password123",
            license_number="TTT33333",
        )
        self.client.force_login(self.user)

    def test_toggle_assign_adds_driver_to_car(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer
        )

        url = reverse("taxi:toggle-car-assign", args=[car.id])

        self.assertNotIn(car, self.user.cars.all())

        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)

        self.assertIn(car, self.user.cars.all())

    def test_toggle_assign_removes_driver_from_car(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer
        )

        self.user.cars.add(car)
        self.assertIn(car, self.user.cars.all())

        url = reverse("taxi:toggle-car-assign", args=[car.id])

        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)

        self.assertNotIn(car, self.user.cars.all())
