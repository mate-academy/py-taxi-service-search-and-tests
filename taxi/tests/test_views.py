from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Car, Manufacturer


MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")
MANUFACTURER_UPDATE_URL_STR = "taxi:manufacturer-update"
MANUFACTURER_DELETE_URL_STR = "taxi:manufacturer-delete"

CAR_LIST_URL = reverse("taxi:car-list")
CAR_CREATE_URL = reverse("taxi:car-create")
CAR_DETAIL_URL_STR = "taxi:car-detail"
CAR_UPDATE_URL_STR = "taxi:car-update"
CAR_DELETE_URL_STR = "taxi:car-delete"
CAR_TOGGLE_CAR_ASSIGN_URL_STR = "taxi:toggle-car-assign"

DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")
DRIVER_DETAIL_URL_STR = "taxi:driver-detail"
DRIVER_UPDATE_URL_STR = "taxi:driver-update"
DRIVER_DELETE_URL_STR = "taxi:driver-delete"


class PublicManufacturerViewTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country",
        )

    def test_manufacturer_list_login_required(self) -> None:
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_create_login_required(self) -> None:
        response = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_update_login_required(self) -> None:
        url = reverse(
            MANUFACTURER_UPDATE_URL_STR,
            args=(self.manufacturer.id,)
        )
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_delete_login_required(self) -> None:
        url = reverse(
            MANUFACTURER_DELETE_URL_STR,
            args=(self.manufacturer.id,)
        )
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerViewTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.manufacturer_names_search = [
            "",
            "Toyota",
            "bmw",
            "da",
            "a",
        ]

    def setUp(self) -> None:
        self.admin = get_user_model().objects.create_superuser(
            username="admin.user",
            password="1qazcde3",
        )
        self.client = Client()
        self.login = self.client.force_login(self.admin)

    def creating_manufacturers(self) -> None:
        manufacturers = [
            ("Toyota", "Japan"),
            ("BMW", "German"),
            ("Honda", "Japan"),
            ("Skoda", "Czech Republic"),
        ]
        for name, country in manufacturers:
            Manufacturer.objects.create(
                name=name,
                country=country,
            )

    def test_retrieving_manufacturers_list(self) -> None:
        self.creating_manufacturers()
        response = self.client.get(MANUFACTURER_LIST_URL)
        manufacturer_list = Manufacturer.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer_list)
        )
        self.assertTemplateUsed(
            response, "taxi/manufacturer_list.html"
        )

    def test_manufacturer_search_result(self) -> None:
        self.creating_manufacturers()
        for manufacturer_name in self.manufacturer_names_search:
            with self.subTest(manufacturer_name):
                response = self.client.get(
                    MANUFACTURER_LIST_URL,
                    {"name": manufacturer_name}
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    list(response.context["manufacturer_list"]),
                    list(
                        Manufacturer.objects.filter(
                            name__icontains=manufacturer_name
                        )
                    )
                )

    def test_manufacturer_create(self) -> None:
        test_name = "Alfa Romeo"
        test_country = "Italy"
        response = self.client.post(
            MANUFACTURER_CREATE_URL,
            {
                "name": test_name,
                "country": test_country,
            }
        )
        self.assertRedirects(response, MANUFACTURER_LIST_URL)
        manufacturer = Manufacturer.objects.get(name=test_name)
        self.assertEqual(manufacturer.name, test_name)

    def test_manufacturer_update(self) -> None:
        updated_name = "New name"
        updated_country = "New country"
        self.manufacturer = Manufacturer.objects.create(
            name="Wrong name",
            country="Wrong country",
        )
        url = reverse(
            MANUFACTURER_UPDATE_URL_STR,
            args=[self.manufacturer.id, ]
        )
        response = self.client.post(
            url,
            {
                "name": updated_name,
                "country": updated_country,
            }
        )
        self.manufacturer.refresh_from_db()
        self.assertRedirects(response, MANUFACTURER_LIST_URL)
        self.assertEqual(self.manufacturer.name, updated_name)

    def test_manufacturer_delete(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country",
        )
        url = reverse(
            MANUFACTURER_DELETE_URL_STR,
            args=[self.manufacturer.id, ]
        )
        response = self.client.post(url)
        self.assertRedirects(response, MANUFACTURER_LIST_URL)
        self.assertFalse(list(Manufacturer.objects.all()))


class PublicCarViewTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country",
        )
        self.car = Car.objects.create(
            model="Test model",
            manufacturer=self.manufacturer,
        )

    def test_car_list_login_required(self) -> None:
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_car_create_login_required(self) -> None:
        response = self.client.get(CAR_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_car_detail_login_required(self) -> None:
        url = reverse(CAR_DETAIL_URL_STR, args=(self.car.id,))
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_car_update_login_required(self) -> None:
        url = reverse(CAR_UPDATE_URL_STR, args=(self.car.id,))
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_car_delete_login_required(self) -> None:
        url = reverse(CAR_DELETE_URL_STR, args=(self.car.id,))
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_toggle_car_assign_login_required(self) -> None:
        url = reverse(CAR_TOGGLE_CAR_ASSIGN_URL_STR, args=(self.car.id,))
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarViewTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.car_models_search = [
            "",
            "Camry",
            "70",
            "FAB",
            "ia",
        ]

    def setUp(self) -> None:
        self.admin = get_user_model().objects.create_superuser(
            username="admin.user",
            password="1qazcde3",
        )
        self.client = Client()
        self.login = self.client.force_login(self.admin)

    def creating_manufacturers_and_cars(self) -> None:
        self.toyota = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.skoda = Manufacturer.objects.create(
            name="Skoda",
            country="Czech Republic",
        )
        cars = [
            ("Camry 40", self.toyota),
            ("Camry 70", self.toyota),
            ("Octavia", self.skoda),
            ("Fabia", self.skoda),
        ]
        for model, manufacturer in cars:
            Car.objects.create(
                model=model,
                manufacturer=manufacturer,
            )

    def test_retrieving_car_list(self) -> None:
        self.creating_manufacturers_and_cars()
        response = self.client.get(CAR_LIST_URL)
        car_list = Car.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(car_list)
        )
        self.assertTemplateUsed(
            response, "taxi/car_list.html"
        )

    def test_car_search_result(self) -> None:
        self.creating_manufacturers_and_cars()
        for car_model in self.car_models_search:
            with self.subTest(car_model):
                response = self.client.get(
                    CAR_LIST_URL,
                    {"model": car_model}
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    list(response.context["car_list"]),
                    list(
                        Car.objects.filter(
                            model__icontains=car_model
                        )
                    )
                )

    def test_car_create(self) -> None:
        test_model_name = "Test model"
        self.manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country",
        )
        self.user = get_user_model().objects.create_user(
            username="test.driver",
            password="1qazcde3",
            first_name="Test_first",
            last_name="Test_last",
            license_number="TST12345",
        )
        response = self.client.post(
            CAR_CREATE_URL,
            {
                "model": test_model_name,
                "manufacturer": self.manufacturer.id,
                "drivers": [self.user.id, ],
            }
        )
        self.car = Car.objects.get(model=test_model_name)
        self.assertRedirects(response, CAR_LIST_URL)
        self.assertEqual(self.car.model, test_model_name)
        self.assertEqual(self.car.manufacturer, self.manufacturer)
        self.assertEqual(
            list(self.car.drivers.all()),
            [self.user]
        )

    def test_car_update(self) -> None:
        test_model_name = "Test_model"
        new_model_name = "New model"
        self.manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country",
        )
        self.user = get_user_model().objects.create_user(
            username="test.driver",
            password="1qazcde3",
            first_name="Test_first",
            last_name="Test_last",
            license_number="TST12345"
        )
        self.car = Car.objects.create(
            model=test_model_name,
            manufacturer=self.manufacturer,
        )
        self.car.drivers.set([self.user, ])
        url = reverse(CAR_UPDATE_URL_STR, args=[self.car.id, ])
        response = self.client.post(
            url,
            {
                "model": new_model_name,
                "manufacturer": self.manufacturer.id,
                "drivers": [self.user.id, ],
            }
        )
        self.car.refresh_from_db()
        self.assertRedirects(response, CAR_LIST_URL)
        self.assertEqual(self.car.model, new_model_name)

    def test_car_delete(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country",
        )
        self.user = get_user_model().objects.create_user(
            username="test.driver",
            password="1qazcde3",
            first_name="Test_first",
            last_name="Test_last",
            license_number="TST12345",
        )
        self.car = Car.objects.create(
            model="Test model",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.set([self.user, ])
        url = reverse(CAR_DELETE_URL_STR, args=[self.car.id, ])
        response = self.client.post(url)
        self.assertRedirects(response, CAR_LIST_URL)
        self.assertFalse(list(Car.objects.all()))

    def test_retrieving_car_detail(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test.driver",
            password="1qazcde3",
            first_name="Test_first",
            last_name="Test_last",
            license_number="TST12345",
        )
        self.creating_manufacturers_and_cars()
        self.cars = Car.objects.all()
        for car in self.cars:
            with self.subTest(car):
                url = reverse(CAR_DETAIL_URL_STR, args=[car.id, ])
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, car.model)
                self.assertContains(response, car.manufacturer.name)
                self.assertContains(response, car.manufacturer.country)

    def test_toggle_car_assign(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country",
        )
        self.user = get_user_model().objects.create_user(
            username="test.driver",
            password="1qazcde3",
            first_name="Test_first",
            last_name="Test_last",
            license_number="TST12345",
        )
        self.car = Car.objects.create(
            model="Test model",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.set([self.user, ])
        self.drivers_before = self.car.drivers.all()
        url = reverse(CAR_TOGGLE_CAR_ASSIGN_URL_STR, args=[self.car.id, ])
        self.client.post(url)
        self.assertEqual(
            list(self.drivers_before),
            list(self.car.drivers.all())
        )
        self.client.post(url)
        self.assertNotEqual(
            list(self.drivers_before),
            list(self.car.drivers.all())
        )


class PublicDriverViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test.driver",
            password="1qazcde3",
            first_name="Test_first",
            last_name="Test_last",
            license_number="TST12345",
        )

    def test_driver_list_login_required(self) -> None:
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_create_login_required(self) -> None:
        response = self.client.get(DRIVER_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_detail_login_required(self) -> None:
        url = reverse(DRIVER_DETAIL_URL_STR, args=(self.user.id,))
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_update_login_required(self) -> None:
        url = reverse(DRIVER_UPDATE_URL_STR, args=(self.user.id,))
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_delete_login_required(self) -> None:
        url = reverse(DRIVER_DELETE_URL_STR, args=(self.user.id,))
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverViewTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.usernames_search = [
            "",
            "admin",
            "bob",
            "b",
            "driv",
        ]

    def setUp(self) -> None:
        self.admin = get_user_model().objects.create_superuser(
            username="admin.user",
            password="1qazcde3",
        )
        self.client = Client()
        self.login = self.client.force_login(self.admin)

    def creating_users(self) -> None:
        users = [
            ("Bob", "1qazcde3", "Bob", "Cage", "TST12345"),
            ("bruce.drive", "1qazcde3", "Bruce", "Dove", "TST54321"),
            ("super.driver", "1qazcde3", "Super", "Driver", "TST13524"),
            ("fake.admin", "1qazcde3", "Admin", "NotReal", "TST24135"),
        ]
        for username, password, first_name, last_name, license_number in users:
            get_user_model().objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                license_number=license_number,
            )

    def test_retrieving_driver_list(self) -> None:
        self.creating_users()
        response = self.client.get(DRIVER_LIST_URL)
        driver_list = get_user_model().objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(driver_list)
        )
        self.assertTemplateUsed(
            response, "taxi/driver_list.html"
        )

    def test_driver_search_result(self) -> None:
        self.creating_users()
        for username in self.usernames_search:
            with self.subTest(username):
                response = self.client.get(
                    DRIVER_LIST_URL,
                    {"username": username}
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    list(response.context["driver_list"]),
                    list(
                        get_user_model().objects.filter(
                            username__icontains=username
                        )
                    )
                )

    def test_driver_create(self) -> None:
        username = "test.user"
        password = "1qazcde3"
        first_name = "Test_first"
        last_name = "Test_last"
        license_number = "TST12345"
        response = self.client.post(
            DRIVER_CREATE_URL,
            {
                "username": username,
                "password1": password,
                "password2": password,
                "first_name": first_name,
                "last_name": last_name,
                "license_number": license_number,
            }
        )
        user = get_user_model().objects.get(username=username)
        url = reverse(DRIVER_DETAIL_URL_STR, args=[user.id, ])
        self.assertRedirects(response, url)
        self.assertEqual(user.username, username)

    def test_driver_delete(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test.driver",
            password="1qazcde3",
            first_name="Test_first",
            last_name="Test_last",
            license_number="TST12345",
        )
        self.user.save()
        url = reverse("taxi:driver-delete", args=[self.user.id, ])
        response = self.client.post(url)
        self.assertRedirects(response, DRIVER_LIST_URL)
        self.assertFalse(len(list(get_user_model().objects.all())) >= 2)
