from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

"""
testing code for the IndexView
"""


class PrivateHomePageTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="test",
            password="12234"
        )
        self.client.force_login(user)
        self.res = self.client.get(reverse("taxi:index"))

    def test_private_hom_pclearage_test(self):
        self.assertEquals(self.res.status_code, 200)


class PublicHomePageTest(TestCase):
    def setUp(self):
        self.res = self.client.get(reverse("taxi:index"))

    def test_public_home_page(self):
        self.assertNotEquals(self.res.status_code, 200)


class IndexViewTest(TestCase):
    def setUp(self):
        driver_test = get_user_model().objects.create_user(
            username="Anton", password="tiguti26", license_number="NO55555"
        )

        manufacturer_test = Manufacturer.objects.create(
            name="test_Manufacturer", country="test_Country"
        )
        self.car = Car.objects.create(
            model="test_Model",
            manufacturer=manufacturer_test,
        )
        self.car.drivers.add(driver_test)
        self.client.force_login(driver_test)
        self.response = self.client.get(
            reverse("taxi:index")
        )

    def test_home_page_count(self):
        num_test = [
            "num_drivers",
            "num_cars",
            "num_manufacturers",
            "num_visits"
        ]
        for data in num_test:
            self.assertTemplateUsed(self.response, "taxi/index.html")
            self.assertIn(data, self.response.context,
                          f"key must be equal to {data}")
            self.assertGreaterEqual(
                self.response.context[data],
                1,
                "count must be greater or equal 1"
            )


"""
     testing code for Manufacturer view
"""
MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerPageTest(TestCase):
    def setUp(self):
        self.res = self.client.get(MANUFACTURER_URL)

    def test_retrieve_login_manufacturer(self):
        self.assertNotEquals(self.res.status_code, 200)


class PrivateManufacturerPageTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test", password="12234"
        )
        Manufacturer.objects.create(
            name="test_Manufacturer",
            country="test_Country"
        )
        Manufacturer.objects.create(
            name="test_Manufacturer1",
            country="test_Country1"
        )

    def test_retrieve_login_manufacturer(self):
        self.client.force_login(self.user)
        self.res = self.client.get(MANUFACTURER_URL)
        self.assertEqual(self.res.status_code, 200)


class ManufacturerListTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="test",
            password="12234"
        )
        Manufacturer.objects.create(
            name="test_Manufacturer",
            country="test_Country"
        )
        Manufacturer.objects.create(
            name="test_Manufacturer1",
            country="test_Country1"
        )
        self.client.force_login(user)
        self.res = self.client.get(MANUFACTURER_URL)

    def test_retrieve_manufacturers(self):
        self.assertEquals(self.client.get(MANUFACTURER_URL).status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEquals(
            list(self.client.get(MANUFACTURER_URL).
                 context["manufacturer_list"]),
            list(manufacturers),
        )


class ManufacturerCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.post_data = {"name": "TestName", "country": "test_Country1"}
        self.client.force_login(self.user)
        self.response = self.client.get(reverse("taxi:manufacturer-create"))

    def test_create_manufacturer(self):
        self.client.post(reverse("taxi:manufacturer-create"),
                         data=self.post_data)
        self.new_manufacturer = Manufacturer.objects.get(
            name=self.post_data["name"]
        )
        self.assertEqual(self.new_manufacturer.name, self.post_data["name"])
        self.assertEqual(self.new_manufacturer.country,
                         self.post_data["country"])


class ManufacturerUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword"
        )

        self.manufacturer = (Manufacturer.objects.create
                             (name="test1", country="test_Country1"))

        self.post_data = {"name": "TestName", "country": "test_Country2"}
        self.client.force_login(self.user)

    def test_manufacturer_update(self):
        url = reverse("taxi:manufacturer-update",
                      kwargs={"pk": self.manufacturer.pk}
                      )
        self.client.post(url,
                         data=self.post_data
                         )
        updated_manufacturer = (Manufacturer.objects.
                                get(name=self.post_data["name"]))
        self.assertEqual(updated_manufacturer.name,
                         self.post_data["name"])
        self.assertEqual(updated_manufacturer.country,
                         self.post_data["country"])


class ManufacturerDeleteView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test1",
            country="test_Country1"
        )
        Manufacturer.objects.create(name="test2",
                                    country="test_Country2")
        self.post_data = {"name": "TestName",
                          "country": "test_Country2"}
        self.client.force_login(self.user)
        self.url_delete = reverse(
            "taxi:manufacturer-delete",
            kwargs={"pk": self.manufacturer.id}
        )

    def test_delete_manufacturer(self):
        self.client.post(self.url_delete)
        updated_manufacturer = Manufacturer.objects.all()
        self.assertEqual(len(updated_manufacturer), 1)


class ManufacturerSearchContextTest(TestCase):
    def setUp(self):
        driver1 = Driver.objects.create_user(username="nop",
                                             password="re")
        self.manufacturer = Manufacturer.objects.create(
            name="test_Manufacturer",
            country="test_Country"
        )
        self.manufacturer1 = Manufacturer.objects.create(
            name="test_Manufacturer1",
            country="test_Country1"
        )
        self.client.force_login(driver1)

    def test_search_field_manufacturer_by_name(self):
        Manufacturer.objects.create(name="TestName",
                                    country="TestCountry")
        expected_query_set = (
            Manufacturer.objects.filter(name__icontains="TestName")
        )

        response = self.client.get(MANUFACTURER_URL + "?name=TestName")
        result_query_set = response.context_data["manufacturer_list"]

        self.assertEqual(list(expected_query_set), list(result_query_set))


"""
     testing code for Car view
"""

CAR_URL = reverse("taxi:car-list")


class PublicCarPageTest(TestCase):
    def setUp(self):
        self.res = self.client.get(CAR_URL)

    def test_retrieve_login_manufacturer(self):
        self.assertNotEquals(self.res.status_code, 200)


class PrivateCarPageTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test", password="12234"
        )
        self.manufacturer_test_data = Manufacturer.objects.create(
            name="test_Manufacturer",
            country="test_Country"
        )
        self.car_test_data = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer_test_data,
        )

        self.driver_test_data = get_user_model().objects.create_user(
            username="driver",
            password="testdriver",
            license_number="OO55555"
        )
        self.car_test_data.drivers.add(self.driver_test_data)
        self.client.force_login(self.driver_test_data)

        Manufacturer.objects.create(name="test_Manufacturer1",
                                    country="test_Country1")
        self.client.force_login(self.user)
        self.res = self.client.get(CAR_URL)

    def test_retrieve_login_manufacturer(self):
        self.client.force_login(self.user)
        self.res = self.client.get(CAR_URL)
        self.assertEqual(self.res.status_code, 200)


class CarListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="12234"
        )
        self.manufacturer_test_data = Manufacturer.objects.create(
            name="test_Manufacturer",
            country="test_Country"
        )
        self.car_test_data = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer_test_data,
        )

        self.driver_test_data = get_user_model().objects.create_user(
            username="driver",
            password="testdriver",
            license_number="OO55555"
        )
        self.car_test_data.drivers.add(self.driver_test_data)
        self.client.force_login(self.driver_test_data)
        self.res = self.client.get(CAR_URL)

    def test_retrieve_car(self):
        self.assertEquals(self.client.get(CAR_URL).status_code, 200)
        cars_list = Car.objects.all()
        self.assertEquals(
            list(self.client.get(CAR_URL).context["car_list"]), list(cars_list)
        )


class CarCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.manufacturer_test_data = Manufacturer.objects.create(
            name="test_Manufacturer",
            country="test_Country"
        )
        self.car_test_data = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer_test_data,
        )

        self.driver_test_data = get_user_model().objects.create_user(
            username="driver",
            password="testdriver",
            license_number="OO55555"
        )
        self.new_driver_test_data = get_user_model().objects.create_user(
            username="driver1",
            password="testdriver1",
            license_number="OO55554"
        )
        self.car_test_data.drivers.add(self.driver_test_data)
        self.client.force_login(self.driver_test_data)

        self.post_data = {
            "model": "testmodel1",
            "manufacturer": self.manufacturer_test_data.pk,
            "drivers": [self.car_test_data.pk, self.new_driver_test_data.pk],
        }

    def test_create_car(self):
        self.client.post(reverse("taxi:car-create"), data=self.post_data)
        self.new_car = Car.objects.get(model=self.post_data["model"])
        self.assertEqual(self.new_car.model, self.post_data["model"])
        self.assertEqual(self.new_car.manufacturer.pk,
                         self.post_data["manufacturer"])
        self.assertCountEqual(
            self.new_car.drivers.values_list("pk", flat=True),
            self.post_data["drivers"]
        )


class CarUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.manufacturer_test_data = Manufacturer.objects.create(
            name="test_Manufacturer",
            country="test_Country"
        )

        Manufacturer.objects.create(name="test_Manufacturer1",
                                    country="test_Country2")

        self.car_test_data = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer_test_data,
        )

        self.driver_test_data = get_user_model().objects.create_user(
            username="driver",
            password="testdriver",
            license_number="OO55555"
        )
        self.new_driver_test_data = get_user_model().objects.create_user(
            username="driver1",
            password="testdriver1",
            license_number="OO55554"
        )
        self.car_test_data.drivers.add(self.driver_test_data)
        self.post_data = {
            "model": "tester_model1",
            "manufacturer": self.manufacturer_test_data.pk,
            "drivers": [self.car_test_data.pk, self.new_driver_test_data.pk],
        }

        self.client.force_login(self.driver_test_data)

    def test_car_update(self):
        url = reverse("taxi:car-update",
                      kwargs={"pk": self.car_test_data.pk})
        self.client.post(url, data=self.post_data)
        updated_car = Car.objects.get(model=self.post_data["model"])
        self.assertEqual(updated_car.manufacturer.pk,
                         self.post_data["manufacturer"])
        self.assertCountEqual(
            self.car_test_data.drivers.values_list("pk", flat=True),
            self.post_data["drivers"],
        )


class DeleteCarViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.manufacturer_test_data = Manufacturer.objects.create(
            name="test_Manufacturer",
            country="test_Country"
        )

        Manufacturer.objects.create(name="test_Manufacturer1",
                                    country="test_Country2")

        self.car_test_data = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer_test_data,
        )

        self.driver_test_data = get_user_model().objects.create_user(
            username="driver",
            password="testdriver",
            license_number="OO55555"
        )
        self.new_driver_test_data = get_user_model().objects.create_user(
            username="driver1",
            password="testdriver1",
            license_number="OO55554"
        )
        self.car_test_data.drivers.add(self.driver_test_data)
        self.post_data = {
            "model": "tester_model1",
            "manufacturer": self.manufacturer_test_data.pk,
            "drivers": [self.car_test_data.pk, self.new_driver_test_data.pk],
        }

        self.client.force_login(self.driver_test_data)

    def test_car_delete(self):
        url = reverse("taxi:car-update",
                      kwargs={"pk": self.car_test_data.pk})
        self.client.post(url)
        updated_car = Car.objects.all()
        self.assertEqual(len(updated_car), 1)


class CarSearchContextTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="12234"
        )
        self.manufacturer_test_data = Manufacturer.objects.create(
            name="test_Manufacturer",
            country="test_Country"
        )
        self.car_test_data = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer_test_data,
        )

        self.driver_test_data = get_user_model().objects.create_user(
            username="driver",
            password="testdriver",
            license_number="OO55555"
        )
        self.car_test_data.drivers.add(self.driver_test_data)
        self.client.force_login(self.driver_test_data)
        self.res = self.client.get(CAR_URL)

    def test_search_field_car_by_model(self):
        expected_query_set = Car.objects.filter(model__icontains="test_model")
        response = self.client.get(CAR_URL + "?name=test_model")
        result_query_set = response.context_data["car_list"]

        self.assertEqual(list(expected_query_set), list(result_query_set))


"""
     testing code for Driver view
"""

DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverPageTest(TestCase):
    def setUp(self):
        self.res = self.client.get(DRIVER_URL)

    def test_retrieve_login_manufacturer(self):
        self.assertNotEquals(self.res.status_code, 200)


class DriverViewTest(TestCase):
    def setUp(self):
        self.driver_test_data = get_user_model().objects.create_user(
            username="driver",
            password="testdriver",
            license_number="OO55555",
            first_name="test_first_name",
            last_name="test_last_name",
            email="user@gmail.com",
        )
        self.client.force_login(self.driver_test_data)
        self.res = self.client.get(DRIVER_URL)

    def test_retrieve_driver(self):
        self.assertEquals(self.client.get(DRIVER_URL).status_code, 200)
        drivers_list = Driver.objects.all()
        self.assertEquals(
            list(self.client.get(DRIVER_URL).context["driver_list"]),
            list(drivers_list)
        )


class DriverCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.driver_test_data = get_user_model().objects.create_user(
            username="driver",
            password="testdriver",
            license_number="OO55555",
            first_name="test_first_name",
            last_name="test_last_name",
            email="user@gmail.com",
        )
        self.res = self.client.get(DRIVER_URL)
        self.post_data = {
            "username": "driver1",
            "password1": "tiguti26",
            "password2": "tiguti26",
            "license_number": "NON55545",
            "first_name": "test_first_name1",
            "last_name": "test_last_name1",
            "email": "test@gmail.com",
        }

        self.client.force_login(self.driver_test_data)
        self.response = self.client.get(reverse("taxi:driver-create"))

    def test_create_driver(self):
        self.client.post(reverse("taxi:driver-create"), data=self.post_data)

        self.new_driver = Driver.objects.get(
            username=self.post_data["username"]
        )
        self.assertEqual(self.new_driver.username,
                         self.post_data["username"])
        self.assertTrue(
            self.new_driver.check_password(self.post_data["password1"])
        )
        self.assertTrue(self.new_driver.check_password(
            self.post_data["password2"])
        )
        self.assertEqual(
            self.new_driver.license_number,
            self.post_data["license_number"]
        )
        self.assertEqual(self.new_driver.first_name,
                         self.post_data["first_name"])
        self.assertEqual(self.new_driver.last_name,
                         self.post_data["last_name"])


class DriverSearchContextTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="12234"
        )
        self.manufacturer_test_data = Manufacturer.objects.create(
            name="test_Manufacturer",
            country="test_Country"
        )
        self.car_test_data = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer_test_data,
        )

        self.driver_test_data = get_user_model().objects.create_user(
            username="driver",
            password="testdriver",
            license_number="OO55555"
        )
        self.car_test_data.drivers.add(self.driver_test_data)
        self.client.force_login(self.driver_test_data)
        self.res = self.client.get(DRIVER_URL)

    def test_search_field_driver_by_username(self):
        expected_query_set = Driver.objects.filter(
            username__icontains="driver"
        )
        response = self.client.get(DRIVER_URL + "?username=driver")
        result_query_set = response.context_data["driver_list"]

        self.assertEqual(list(expected_query_set), list(result_query_set))


class ToggleAssignToCarTestCase(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="testdriver",
            license_number="OO55555",
            first_name="test_first_name",
            last_name="test_last_name",
        )

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )

        self.car = Car.objects.create(
            model="Toyota Camry", manufacturer=self.manufacturer
        )
        self.client.login(username="driver",
                          password="testdriver")

    def test_toggle_assign_to_car(self):
        self.new_car = Car.objects.get(pk=self.car.pk)
        self.assertNotIn(self.new_car, self.driver.cars.all())
        response = self.client.post(
            reverse("taxi:toggle-car-assign", args=[self.new_car.pk])
        )
        print(vars(response))
        print(self.driver.cars.all())
        self.client.post(reverse(
            "taxi:toggle-car-assign",
            args=[self.new_car.pk])
        )
        self.assertNotIn(self.new_car, self.driver.cars.all())
