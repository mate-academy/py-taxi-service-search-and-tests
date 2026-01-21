from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

INDEX_URL = reverse("taxi:index")

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")

CARS_URL = reverse("taxi:car-list")

DRIVERS_URL = reverse("taxi:driver-list")


class PublicViewTest(TestCase):
    def test_login_required(self):
        res_index = self.client.get(INDEX_URL)
        res_manufacturers = self.client.get(MANUFACTURERS_URL)
        res_cars = self.client.get(CARS_URL)
        res_drivers = self.client.get(DRIVERS_URL)

        self.assertRedirects(
            res_index,
            "/accounts/login/?next=/"
        )
        self.assertRedirects(
            res_manufacturers,
            "/accounts/login/?next=/manufacturers/"
        )
        self.assertRedirects(
            res_cars,
            "/accounts/login/?next=/cars/"
        )
        self.assertRedirects(
            res_drivers,
            "/accounts/login/?next=/drivers/"
        )


class PrivateHomePageViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="<TEST_USER>"
        )
        self.client.force_login(self.user)

    def test_retrieve_homepage(self):
        res = self.client.get(INDEX_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "taxi/index.html")
        self.assertEqual(self.client.session.get("num_visits"), 1)

    def test_homepage_visit_counter_increasing(self):
        self.client.get(INDEX_URL)
        res = self.client.get(INDEX_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.client.session.get("num_visits"), 2)

    def test_homepage_context_counter(self):
        get_user_model().objects.create_user(
            username="test_driver",
            password="<TEST_USER>",
            license_number="ABC12345"
        )
        manufacturer_one = Manufacturer.objects.create(
            name="test_manufacturer_one"
        )
        Car.objects.create(
            model="test_car_one",
            manufacturer=manufacturer_one
        )
        Car.objects.create(
            model="test_car_two",
            manufacturer=manufacturer_one
        )

        num_manufacturers = Manufacturer.objects.count()
        num_cars = Car.objects.count()
        num_drivers = Driver.objects.count()

        res = self.client.get(INDEX_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            self.client.session.get("num_visits"),
            1
        )
        self.assertEqual(
            res.context["num_manufacturers"],
            num_manufacturers
        )
        self.assertEqual(
            res.context["num_cars"],
            num_cars
        )
        self.assertEqual(
            res.context["num_drivers"],
            num_drivers
        )


class PrivateManufacturerViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="<TEST_USER>"
        )
        self.client.force_login(self.user)
        self.manufacturer_one = Manufacturer.objects.create(
            name="test_manufacturer_one",
            country="test_country_one"
        )
        self.manufacturer_two = Manufacturer.objects.create(
            name="test_manufacturer_two",
            country="test_country_two"
        )

    def test_retrieve_manufacturers(self):
        res = self.client.get(MANUFACTURERS_URL)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.manufacturer_one.name)
        self.assertContains(res, self.manufacturer_two.name)
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_manufacturer_search(self):
        res = self.client.get(
            MANUFACTURERS_URL + "?name=test_manufacturer_one"
        )

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.manufacturer_one.name)
        self.assertNotContains(res, self.manufacturer_two.name)
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_manufacturer_create(self):
        form_data = {
            "name": "new_test_manufacturer",
            "country": "new_test_country"
        }
        res = self.client.get(reverse("taxi:manufacturer-create"))
        res_created = self.client.post(
            reverse("taxi:manufacturer-create"),
            form_data
        )
        new_manufacturer = Manufacturer.objects.get(
            name="new_test_manufacturer"
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_created.status_code, 302)
        self.assertEqual(
            new_manufacturer.name,
            form_data["name"]
        )
        self.assertEqual(
            new_manufacturer.country,
            form_data["country"]
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_form.html")
        self.assertRedirects(res_created, MANUFACTURERS_URL)

    def test_manufacturer_update(self):
        form_data = {
            "name": "updated_test_manufacturer",
            "country": "updated_test_country"
        }
        res = self.client.post(
            reverse(
                "taxi:manufacturer-update",
                args=[self.manufacturer_one.id]
            ),
            data=form_data
        )
        updated_manufacturer = Manufacturer.objects.get(
            id=self.manufacturer_one.id
        )

        self.assertEqual(res.status_code, 302)
        self.assertEqual(updated_manufacturer.name, form_data["name"])
        self.assertEqual(updated_manufacturer.country, form_data["country"])
        self.assertRedirects(res, MANUFACTURERS_URL)

    def test_manufacturer_delete(self):
        res = self.client.get(
            reverse(
                "taxi:manufacturer-delete",
                args=[self.manufacturer_one.id]
            )
        )
        res_deleted = self.client.post(
            reverse(
                "taxi:manufacturer-delete",
                args=[self.manufacturer_one.id]
            )
        )
        manufacturers = Manufacturer.objects.filter(
            id=self.manufacturer_one.id
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_deleted.status_code, 302)
        self.assertEqual(len(manufacturers), 0)
        self.assertTemplateUsed(
            res,
            "taxi/manufacturer_confirm_delete.html"
        )


class PrivateCarViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="<TEST_USER>",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)
        self.manufacturer_one = Manufacturer.objects.create(
            name="test_manufacturer_one"
        )
        self.car_one = Car.objects.create(
            model="test_car_one",
            manufacturer=self.manufacturer_one
        )
        self.car_two = Car.objects.create(
            model="test_car_two",
            manufacturer=self.manufacturer_one
        )

    def test_retrieve_cars(self):
        res = self.client.get(CARS_URL)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.car_one.model)
        self.assertContains(res, self.car_two.model)
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_car_detail(self):
        url = reverse(
            "taxi:car-detail",
            args=[self.car_one.id]
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.car_one.model)
        self.assertContains(res, self.car_one.manufacturer.name)
        self.assertTemplateUsed(res, "taxi/car_detail.html")

    def test_car_search(self):
        res = self.client.get(CARS_URL + "?model=test_car_one")

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.car_one.model)
        self.assertContains(res, self.car_one.manufacturer.name)
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_create_car(self):
        url = reverse("taxi:car-create")
        form_data = {
            "model": "new_test_car",
            "manufacturer": self.manufacturer_one.id,
            "drivers": self.user.id
        }
        res = self.client.post(url, data=form_data)
        new_car = Car.objects.get(model=form_data["model"])
        expected_url = reverse("taxi:car-list")

        self.assertEqual(res.status_code, 302)
        self.assertTrue(Car.objects.filter(model=form_data["model"]).exists())
        self.assertEqual(new_car.manufacturer, self.manufacturer_one)
        self.assertIn(self.user, new_car.drivers.all())
        self.assertRedirects(res, expected_url)

    def test_update_car(self):
        url = reverse("taxi:car-update", args=[self.car_one.id])
        form_data = {
            "model": "updated_test_car",
            "manufacturer": self.manufacturer_one.id,
            "drivers": [self.user.id]
        }
        res = self.client.post(url, data=form_data)
        updated_car = Car.objects.get(pk=self.car_one.id)
        expected_url = reverse("taxi:car-list")

        self.assertEqual(res.status_code, 302)
        self.assertEqual(updated_car.model, form_data["model"])
        self.assertRedirects(res, expected_url)

    def test_delete_car(self):
        url = reverse("taxi:car-delete", args=[self.car_one.id])
        res = self.client.post(url)
        expected_url = reverse("taxi:car-list")

        self.assertEqual(res.status_code, 302)
        self.assertFalse(Car.objects.filter(id=self.car_one.id).exists())
        self.assertRedirects(res, expected_url)


class PrivateDriverViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_driver",
            password="password123",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)

        self.driver_one = get_user_model().objects.create_user(
            username="driver_one",
            password="password123",
            license_number="XYZ12345"
        )
        self.driver_two = get_user_model().objects.create_user(
            username="driver_two",
            password="password123",
            license_number="XYZ67890"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer"
        )
        self.car = Car.objects.create(
            model="test_car",
            manufacturer=self.manufacturer
        )
        self.car.drivers.set([self.driver_one])

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVERS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver_one.username)
        self.assertContains(response, self.driver_two.username)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_detail(self):
        url = reverse("taxi:driver-detail", args=[self.driver_one.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver_one.username)
        self.assertContains(response, self.driver_one.license_number)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_driver_search(self):
        response = self.client.get(DRIVERS_URL + "?username=driver_one")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver_one.username)
        self.assertNotContains(response, self.driver_two.username)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_create_driver(self):
        url = reverse("taxi:driver-create")
        form_data = {
            "username": "new_driver",
            "password1": "new_password123",
            "password2": "new_password123",
            "license_number": "NEW12345"
        }
        response = self.client.post(url, data=form_data)
        new_driver = get_user_model().objects.get(username="new_driver")
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            get_user_model().objects
            .filter(username="new_driver")
            .exists()
        )
        self.assertEqual(
            new_driver.license_number,
            "NEW12345"
        )
        self.assertRedirects(
            response,
            reverse("taxi:driver-detail", kwargs={"pk": 4})
        )

    def test_update_driver(self):
        url = reverse("taxi:driver-update", args=[self.driver_one.id])
        form_data = {
            "license_number": "UPD12345"
        }
        response = self.client.post(url, data=form_data)
        updated_driver = get_user_model().objects.get(pk=self.driver_one.id)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(updated_driver.license_number, "UPD12345")
        self.assertRedirects(response, DRIVERS_URL)

    def test_delete_driver(self):
        url = reverse("taxi:driver-delete", args=[self.driver_one.id])
        response = self.client.get(url)
        response_deleted = self.client.post(url)
        drivers = get_user_model().objects.filter(id=self.driver_one.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_deleted.status_code, 302)
        self.assertFalse(drivers.exists())
        self.assertTemplateUsed(response, "taxi/driver_confirm_delete.html")

    def test_toggle_assign_to_car(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.driver_one, self.car.drivers.all())
