from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test1234",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(name="test1", country="test")
        Manufacturer.objects.create(name="test2", country="test")
        res = self.client.get(MANUFACTURER_LIST_URL)
        manufacturer_list = Manufacturer.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]), list(manufacturer_list)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_retrieve_filtered_manufacturer_list(self):
        search_word = "2"
        Manufacturer.objects.create(name="test1", country="test")
        Manufacturer.objects.create(name="test2", country="test")

        response = self.client.get(
            MANUFACTURER_LIST_URL + f"?name={search_word}"
        )
        manufacturer_list = Manufacturer.objects.filter(
            name__icontains=search_word
        )
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer_list)
        )

    def test_manufacturer_create(self):
        form_data = {
            "name": "test",
            "country": "test",
        }

        response = self.client.post(
            reverse("taxi:manufacturer-create"),
            form_data
        )
        new_manufacturer = Manufacturer.objects.get(name=form_data["name"])

        self.assertEqual(new_manufacturer.name, form_data["name"])
        self.assertEqual(new_manufacturer.country, form_data["country"])

        self.assertRedirects(response, reverse("taxi:manufacturer-list"))

    def test_manufacturer_update(self):
        manufacturer = Manufacturer.objects.create(
            name="test1",
            country="test"
        )
        change_data = {
            "name": "test2",
            "country": "test2",
        }
        response = self.client.post(
            reverse(
                "taxi:manufacturer-update",
                kwargs={"pk": manufacturer.id}
            ),
            change_data,
        )
        self.assertTrue(len(Manufacturer.objects.filter(name="test1")) == 0)
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))

    def test_manufacturer_delete(self):

        manufacturer = Manufacturer.objects.create(name="test", country="test")
        response = self.client.post(
            reverse(
                "taxi:manufacturer-delete",
                kwargs={"pk": manufacturer.id}
            )
        )

        self.assertTrue(len(Manufacturer.objects.filter(name="test")) == 0)
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test1234",
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "test",
            "password1": "2wsxvfr4",
            "password2": "2wsxvfr4",
            "first_name": "Test",
            "last_name": "Test",
            "license_number": "TST12345",
        }

        response = self.client.post(reverse("taxi:driver-create"), form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.username, form_data["username"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

        self.assertRedirects(
            response, reverse(
                "taxi:driver-detail",
                kwargs={"pk": new_user.id}
            )
        )

    def test_license_update_driver(self):
        driver = get_user_model().objects.create_user(
            username="test", password="12345678", license_number="TST00000"
        )
        change_data = {
            "license_number": "QWE12345",
        }
        response = self.client.post(
            reverse(
                "taxi:driver-update",
                kwargs={"pk": driver.id}
            ),
            change_data
        )
        self.assertTrue(
            len(
                get_user_model().objects.filter(license_number="TST00000")
            ) == 0
        )
        self.assertRedirects(response, reverse("taxi:driver-list"))

    def test_delete_driver(self):
        driver = get_user_model().objects.create_user(
            username="test", password="12345678", license_number="TST00000"
        )
        response = self.client.post(
            reverse("taxi:driver-delete", kwargs={"pk": driver.id})
        )

        self.assertTrue(
            len(get_user_model().objects.filter(username="test")) == 0
        )
        self.assertRedirects(response, reverse("taxi:driver-list"))

    def test_retrieve_filtered_driver_list(self):
        search_word = "bor"
        get_user_model().objects.create(
            username="test1", password="test", license_number="TST00000"
        )
        get_user_model().objects.create(
            username="bora", password="test", license_number="TST00001"
        )

        response = self.client.get(
            reverse("taxi:driver-list") + f"?username={search_word}"
        )
        driver_list = get_user_model().objects.filter(
            username__icontains=search_word
        )
        self.assertEqual(
            list(response.context["driver_list"]),
            list(driver_list)
        )


class PrivateCarTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test1234",
        )
        self.client.force_login(self.user)

    def test_create_car(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test"
        )
        driver = get_user_model().objects.create_user(
            username="test",
            password="12345678",
            license_number="TST00000"
        )
        form_data = {
            "model": "e60",
            "manufacturer": manufacturer.id,
            "drivers": driver.id,
        }

        response = self.client.post(reverse("taxi:car-create"), form_data)
        new_car = Car.objects.get(model=form_data["model"])

        self.assertEqual(new_car.model, form_data["model"])
        self.assertEqual(new_car.manufacturer.id, form_data["manufacturer"])
        self.assertEqual(new_car.drivers.get(username="test"), driver)

        self.assertRedirects(response, reverse("taxi:car-list"))

    def test_update_car(self):

        manufacturer = Manufacturer.objects.create(name="test", country="test")
        driver = get_user_model().objects.create_user(
            username="test", password="12345678", license_number="TST00000"
        )
        car = Car.objects.create(model="test_model", manufacturer=manufacturer)
        car.drivers.add(driver)

        new_manufacturer = Manufacturer.objects.create(
            name="test2",
            country="test2"
        )
        new_driver = get_user_model().objects.create_user(
            username="test2", password="12345678", license_number="TST00001"
        )

        change_data = {
            "model": "notest_model",
            "manufacturer": new_manufacturer.id,
            "drivers": new_driver.id,
        }

        response = self.client.post(
            reverse("taxi:car-update", kwargs={"pk": car.id}), change_data
        )

        car.refresh_from_db()

        self.assertEqual(car.model, change_data["model"])
        self.assertRedirects(response, reverse("taxi:car-list"))

    def test_delete_car(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test")
        driver = get_user_model().objects.create_user(
            username="test", password="12345678", license_number="TST00000"
        )
        car = Car.objects.create(model="test_model", manufacturer=manufacturer)
        car.drivers.add(driver)

        response = self.client.post(reverse(
            "taxi:car-delete",
            kwargs={"pk": car.id})
        )

        self.assertTrue(len(Car.objects.filter(model="test_model")) == 0)
        self.assertRedirects(response, reverse("taxi:car-list"))

    def test_retrieve_filtered_car_list(self):
        search_word = "bor"
        manufacturer_first = Manufacturer.objects.create(
            name="test1",
            country="test"
        )
        driver_first = get_user_model().objects.create_user(
            username="test1",
            password="12345678",
            license_number="TST00000"
        )

        manufacturer_second = Manufacturer.objects.create(
            name="test2",
            country="test"
        )
        driver_second = get_user_model().objects.create_user(
            username="test2", password="12345678", license_number="TST00001"
        )

        car_first = Car.objects.create(
            model="bora",
            manufacturer=manufacturer_first
        )
        car_first.drivers.add(driver_first)
        car_second = Car.objects.create(
            model="test_model", manufacturer=manufacturer_second
        )
        car_second.drivers.add(driver_second)

        response = self.client.get(
            reverse("taxi:car-list") + f"?model={search_word}"
        )
        car_list = Car.objects.filter(model__icontains=search_word)

        self.assertEqual(list(response.context["car_list"]), list(car_list))

    def test_retrieve_car_list(self):
        manufacturer_first = Manufacturer.objects.create(
            name="test1",
            country="test"
        )
        driver_first = get_user_model().objects.create_user(
            username="test1",
            password="12345678",
            license_number="TST00000"
        )

        manufacturer_second = Manufacturer.objects.create(
            name="test2",
            country="test"
        )
        driver_second = get_user_model().objects.create_user(
            username="test2",
            password="12345678",
            license_number="TST00001"
        )

        car_first = Car.objects.create(
            model="bora",
            manufacturer=manufacturer_first
        )
        car_first.drivers.add(driver_first)
        car_second = Car.objects.create(
            model="test_model", manufacturer=manufacturer_second
        )
        car_second.drivers.add(driver_second)

        response = self.client.get(reverse("taxi:car-list"))

        car_list = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]), list(car_list))
