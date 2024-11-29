from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
MANUFACTURERS_CREATE_URL = reverse("taxi:manufacturer-create")
CARS_URL = reverse("taxi:car-list")
DRIVERS_URL = reverse("taxi:driver-list")
INDEX_URL = reverse("taxi:index")


class ManufacturerListTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        num_of_manufacturers = 9

        for manufacturer_id in range(num_of_manufacturers):
            Manufacturer.objects.create(
                name=f"Manufacturer_{manufacturer_id}",
            )

    def setUp(self):
        user = get_user_model().objects.create_user(
            username="test_user",
        )
        self.client.force_login(user)

    def test_manufacturers_access_by_url(self):
        url = "/manufacturers/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_manufacturers_access_by_name(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertEqual(response.status_code, 200)

    def test_manufacturers_used_correct_template(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturers_pagination_equals_to_five(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(
            len(response.context["manufacturer_list"]),
            5
        )

    def test_manufacturers_list_all_objects(self):
        response = self.client.get(MANUFACTURERS_URL + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 4)


class ManufacturerCreateTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="test_user",
        )
        self.client.force_login(user)
        self.url = reverse("taxi:manufacturer-create")

    def test_manufacturers_access_by_url(self):
        url = "/manufacturers/create/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_manufacturers_access_by_name(self):
        response = self.client.get(MANUFACTURERS_CREATE_URL)
        self.assertEqual(response.status_code, 200)

    def test_manufacturers_used_correct_template(self):
        response = self.client.get(MANUFACTURERS_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")

    def test_new_manufacturer_object_created(self):
        data = {
            "name": "test_manufacturer_name",
            "country": "test_manufacturer_country",
        }
        response = self.client.post(MANUFACTURERS_CREATE_URL, data)
        self.assertEqual(Manufacturer.objects.count(), 1)
        self.assertEqual(
            Manufacturer.objects.get(id=1).name, "test_manufacturer_name"
        )

        self.assertRedirects(
            response,
            reverse("taxi:manufacturer-list")
        )


class ManufacturerUpdateTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="test_user",
        )
        self.client.force_login(user)
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer_name",
            country="test_manufacturer_country",
        )

    def test_manufacturers_access_by_url(self):
        url = "/manufacturers/1/update/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_manufacturers_access_by_name(self):
        url = reverse("taxi:manufacturer-update", args=[self.manufacturer.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_manufacturers_used_correct_template(self):
        url = reverse("taxi:manufacturer-update", args=[self.manufacturer.id])
        response = self.client.get(url)
        self.assertTemplateUsed(
            response, "taxi/manufacturer_form.html"
        )

    def test_update_manufacturer(self):
        data = {
            "name": "test_manufacturer_name_changed",
            "country": "test_manufacturer_country_changed",
        }
        manufacturer_update_url = reverse(
            "taxi:manufacturer-update", args=[self.manufacturer.id]
        )
        response = self.client.post(manufacturer_update_url, data)
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, data["name"])
        self.assertEqual(self.manufacturer.country, data["country"])
        self.assertRedirects(
            response,
            reverse("taxi:manufacturer-list")
        )


class ManufacturerDeleteTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="test_user",
        )
        self.client.force_login(user)
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer_name",
            country="test_manufacturer_country",
        )

    def test_manufacturers_access_by_url(self):
        url = "/manufacturers/1/delete/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_manufacturers_access_by_name(self):
        url = reverse(
            "taxi:manufacturer-delete", kwargs={"pk": self.manufacturer.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_manufacturers_used_correct_template(self):
        url = reverse(
            "taxi:manufacturer-delete", kwargs={"pk": self.manufacturer.id}
        )
        response = self.client.get(url)
        self.assertTemplateUsed(
            response, "taxi/manufacturer_confirm_delete.html"
        )

    def test_delete_manufacturer(self):
        url = reverse(
            "taxi:manufacturer-delete", kwargs={"pk": self.manufacturer.id}
        )
        self.assertEqual(Manufacturer.objects.count(), 1)
        response = self.client.post(url)
        self.assertEqual(Manufacturer.objects.count(), 0)
        self.assertRedirects(
            response,
            reverse("taxi:manufacturer-list")
        )


class CarListTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="test_manufacturer"
        )
        num_of_cars = 11

        for car_id in range(num_of_cars):
            Car.objects.create(
                model=f"test_model_{car_id}",
                manufacturer=manufacturer,
            )

    def setUp(self):
        user = get_user_model().objects.create_user(
            username="test_user",
        )
        self.client.force_login(user)

    def test_car_list_access_by_url(self):
        url = "/cars/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_car_list_access_by_name(self):
        response = self.client.get(CARS_URL)
        self.assertEqual(response.status_code, 200)

    def test_car_list_used_correct_template(self):
        response = self.client.get(CARS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_list_pagination_equals_to_five(self):
        response = self.client.get(CARS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(
            len(response.context["car_list"]),
            5
        )

    def test_car_list_all_objects(self):
        response = self.client.get(CARS_URL + "?page=3")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 1)


class CarCreateTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user"
        )
        self.client.force_login(user=self.user)

    def test_access_by_url(self):
        url = "/cars/create/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_access_by_name(self):
        url = reverse("taxi:car-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_use_correct_template(self):
        url = reverse("taxi:car-create")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_car_was_created(self):
        manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_manufacturer_country",
        )
        data = {
            "model": "test_model",
            "manufacturer": manufacturer.id,
        }
        self.client.post(
            reverse("taxi:car-create"),
            data=data,
        )
        self.assertEqual(Car.objects.count(), 1)


class CarUpdateTests(TestCase):

    def setUp(self):
        user = get_user_model().objects.create_user(
            username="test_user"
        )
        self.client.force_login(user)
        for i in range(3):
            Manufacturer.objects.create(
                name=f"test_manufacturer_{i}",
                country=f"test_country_{i}",
            )
        Car.objects.create(
            model="test_model",
            manufacturer=Manufacturer.objects.get(id=1)
        )

    def test_access_by_url(self):
        url = "/cars/1/update/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_access_by_name(self):
        url = reverse("taxi:car-update", kwargs={"pk": "1"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_use_correct_template(self):
        url = reverse("taxi:car-update", kwargs={"pk": "1"})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_car_was_updated(self):
        manufacturer_2 = Manufacturer.objects.get(id=2)
        url = reverse("taxi:car-update", kwargs={"pk": "1"})
        data = {
            "model": "test_model_updated",
            "manufacturer": manufacturer_2.id,
        }
        self.client.post(url, data=data)
        car = Car.objects.get(pk=1)
        car.refresh_from_db()
        self.assertEqual(car.model, data["model"])
        self.assertEqual(car.manufacturer, Manufacturer.objects.get(id=2))


class CarDeleteTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="test_user"
        )
        self.client.force_login(user)
        Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_manufacturer_country",
        )
        Car.objects.create(
            model="test_model",
            manufacturer=Manufacturer.objects.get(id=1)
        )

    def test_access_by_url(self):
        url = "/cars/1/delete/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_access_by_name(self):
        url = reverse("taxi:car-delete", kwargs={"pk": "1"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_use_correct_template(self):
        url = reverse("taxi:car-delete", kwargs={"pk": "1"})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "taxi/car_confirm_delete.html")

    def test_car_was_deleted(self):
        url = reverse("taxi:car-delete", kwargs={"pk": "1"})
        self.assertEqual(Car.objects.count(), 1)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("taxi:car-list"))
        self.assertEqual(Car.objects.count(), 0)


class DriverListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_drivers = 7

        for drivers_id in range(number_of_drivers):
            get_user_model().objects.create_user(
                f"first_name {drivers_id}",
                f"last_name {drivers_id}",
            )

    def setUp(self):
        user = get_user_model().objects.get(pk=1)
        self.client.force_login(user)

    def test_drivers_list_access_by_url(self):
        url = "/drivers/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_drivers_list_access_by_name(self):
        response = self.client.get(DRIVERS_URL)
        self.assertEqual(response.status_code, 200)

    def test_drivers_list_used_correct_template(self):
        response = self.client.get(DRIVERS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_drivers_list_is_paginated(self):
        response = self.client.get(DRIVERS_URL)
        self.assertTrue("is_paginated" in response.context)

    def test_driver_list_pagination_equal_to_five(self):
        response = self.client.get(DRIVERS_URL)
        self.assertTrue("is_paginated" in response.context)
        paginated_by = len(response.context["driver_list"])
        self.assertEqual(paginated_by, 5)

    def test_driver_list_number_of_objects_on_the_last_page(self):
        response = self.client.get(DRIVERS_URL + "?page=2")
        self.assertTrue(response.status_code == 200)
        self.assertTrue("is_paginated" in response.context)
        num_of_objects = len(response.context["driver_list"])
        self.assertEqual(num_of_objects, 2)


class DriverCreateViewTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="test_user"
        )
        self.client.force_login(user)

    def test_access_by_url(self):
        url = "/drivers/create/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_access_by_name(self):
        url = reverse("taxi:driver-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_use_correct_template(self):
        url = reverse("taxi:driver-create")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_driver_created(self):
        url = reverse("taxi:driver-create")
        data = {
            "username": "test_driver",
            "license_number": "ABC12345",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "password1": "test_password",
            "password2": "test_password",
        }
        self.client.post(url, data)
        self.assertTrue(
            Driver.objects.filter(username=data["username"]).exists()
        )


class DriverUpdateViewTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="test_user",
        )
        self.client.force_login(user)
        Driver.objects.create(
            username="test_driver",
        )

    def test_access_by_url(self):
        url = "/drivers/2/update/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_access_by_name(self):
        url = reverse("taxi:driver-update", kwargs={"pk": "2"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_use_correct_template(self):
        url = reverse("taxi:driver-update", kwargs={"pk": "2"})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_driver_was_updated(self):
        url = reverse("taxi:driver-update", kwargs={"pk": "2"})
        data = {
            "username": "test_driver_updated",
            "license_number": "ABC12345",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "password1": "test_password",
            "password2": "test_password",
        }
        self.client.post(url, data)
        driver = Driver.objects.get(id=2)
        driver.refresh_from_db()
        self.assertEqual(
            driver.username,
            data["username"],
        )


class DriverDeleteViewTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="test_user",
        )
        self.client.force_login(user)
        Driver.objects.create(
            username="test_driver",
        )

    def test_access_by_url(self):
        url = "/drivers/2/delete/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_access_by_name(self):
        url = reverse("taxi:driver-delete", kwargs={"pk": "2"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_use_correct_template(self):
        url = reverse("taxi:driver-delete", kwargs={"pk": "2"})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "taxi/driver_confirm_delete.html")

    def test_driver_deleted(self):
        url = reverse("taxi:driver-delete", kwargs={"pk": "2"})
        self.assertEqual(Driver.objects.count(), 2)
        response = self.client.post(url, {"pk": "2"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("taxi:driver-list"))
        self.assertTrue(Driver.objects.count(), 1)


class PublicAccessTest(TestCase):
    def test_login_required_manufacturers(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_cars(self):
        response = self.client.get(CARS_URL)
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_drivers(self):
        response = self.client.get(DRIVERS_URL)
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_home_page(self):
        response = self.client.get(INDEX_URL)
        self.assertNotEquals(response.status_code, 200)


class PrivateAccessTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="test",
            password="password",
            license_number="ABC12345",
        )
        self.client.force_login(user)

    def test_private_login_required_manufacturers(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertEquals(response.status_code, 200)

    def test_private_login_required_cars(self):
        response = self.client.get(CARS_URL)
        self.assertEquals(response.status_code, 200)

    def test_private_login_required_drivers(self):
        response = self.client.get(DRIVERS_URL)
        self.assertEquals(response.status_code, 200)

    def test_private_login_required_home_page(self):
        response = self.client.get(INDEX_URL)
        self.assertEquals(response.status_code, 200)
