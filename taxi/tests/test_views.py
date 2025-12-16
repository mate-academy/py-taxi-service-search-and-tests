from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

INDEX_URL = reverse("taxi:index")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicPagesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )

        cls.car = Car.objects.create(
            model="test_model",
            manufacturer=cls.manufacturer
        )

        cls.driver = get_user_model().objects.create_user(
            username="test",
            password="t5st_P@ss",
            first_name="testus",
            last_name="testenko",
            license_number="TES77587"
        )

    def test_login_required_index(self):
        self.assertNotEqual(
            self.client.get(INDEX_URL).status_code, 200
        )

    def test_login_required_manufacturer(self):
        self.assertNotEqual(
            self.client.get(MANUFACTURER_LIST_URL).status_code, 200
        )

    def test_login_required_car(self):
        self.assertNotEqual(
            self.client.get(CAR_LIST_URL).status_code, 200
        )

    def test_login_required_driver(self):
        self.assertNotEqual(
            self.client.get(DRIVER_LIST_URL).status_code, 200
        )

    def test_login_required_car_detail(self):
        car_detail_url = reverse("taxi:car-detail", kwargs={"pk": self.car.pk})
        self.assertNotEqual(
            self.client.get(car_detail_url).status_code, 200
        )

    def test_login_required_driver_detail(self):
        driver_detail_url = reverse(
            "taxi:driver-detail", kwargs={"pk": self.driver.pk}
        )
        self.assertNotEqual(
            self.client.get(driver_detail_url).status_code, 200
        )


class PrivatePagesTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )

        self.car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer
        )
        self.user = get_user_model().objects.create_user(
            username="private_test_user",
            password="t5st_P@ss",
            license_number="TES12345"
        )
        self.client.force_login(self.user)

    def test_index_page_logged_in(self):
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("num_drivers" in response.context)
        self.assertTrue("num_cars" in response.context)
        self.assertTrue("num_manufacturers" in response.context)

    def test_manufacturer_list_view(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.manufacturer.name)

    def test_car_list_view(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car.model)

    def test_driver_list_view(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.user.license_number)

    def test_car_detail_view(self):
        response = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": self.car.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car.model)
        self.assertContains(response, self.car.manufacturer.name)

    def test_driver_detail_view(self):
        response = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": self.user.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.user.license_number)

    def test_toggle_assign_car(self):
        self.assertNotIn(self.car, self.user.cars.all())

        assign_url = reverse(
            "taxi:toggle-car-assign", kwargs={"pk": self.car.pk}
        )
        self.client.get(assign_url)
        self.user.refresh_from_db()
        self.assertIn(self.car, self.user.cars.all())

        self.client.get(assign_url)
        self.user.refresh_from_db()
        self.assertNotIn(self.car, self.user.cars.all())

    def test_manufacturer_create(self):
        initial_count = Manufacturer.objects.count()
        response = self.client.post(
            reverse("taxi:manufacturer-create"),
            data={"name": "NewMan", "country": "NewCo"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, MANUFACTURER_LIST_URL)
        self.assertEqual(Manufacturer.objects.count(), initial_count + 1)
        self.assertTrue(Manufacturer.objects.filter(name="NewMan").exists())

    def test_manufacturer_update(self):
        response = self.client.post(
            reverse(
                "taxi:manufacturer-update", kwargs={"pk": self.manufacturer.pk}
            ),
            data={"name": "UpdatedName", "country": self.manufacturer.country}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, MANUFACTURER_LIST_URL)
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, "UpdatedName")

    def test_manufacturer_delete(self):
        manufacturer_to_delete = Manufacturer.objects.create(
            name="ToDelete", country="Del"
        )
        initial_count = Manufacturer.objects.count()
        response = self.client.post(
            reverse(
                "taxi:manufacturer-delete",
                kwargs={"pk": manufacturer_to_delete.pk}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, MANUFACTURER_LIST_URL)
        self.assertEqual(Manufacturer.objects.count(), initial_count - 1)
        with self.assertRaises(Manufacturer.DoesNotExist):
            Manufacturer.objects.get(pk=manufacturer_to_delete.pk)

    def test_successful_car_search(self):
        car_name = "SearchCarModel"
        manufacturer_for_car = Manufacturer.objects.create(
            name="CarMan", country="USA"
        )
        Car.objects.create(
            model=car_name, manufacturer=manufacturer_for_car
        )

        response = self.client.get(
            CAR_LIST_URL, {"model": car_name}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, car_name)
        self.assertEqual(len(response.context["car_list"]), 1)
        self.assertEqual(response.context["car_list"][0].model, car_name)

    def test_manufacturer_search_found(self):
        manufacturer_name = "SearchManName"
        Manufacturer.objects.create(
            name=manufacturer_name, country="Country"
        )
        response = self.client.get(
            MANUFACTURER_LIST_URL, {"name": manufacturer_name}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, manufacturer_name)
        self.assertEqual(len(response.context["manufacturer_list"]), 1)
        self.assertEqual(
            response.context["manufacturer_list"][0].name,
            manufacturer_name
        )

    def test_manufacturer_search_not_found(self):
        response = self.client.get(
            MANUFACTURER_LIST_URL, {"name": "NonExistentManufacturer"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["manufacturer_list"], []
        )

    def test_driver_search_found(self):
        driver_username = "searchdriver"
        get_user_model().objects.create_user(
            username=driver_username,
            password="pwd",
            license_number="SRCHDRV"
        )

        response = self.client.get(
            DRIVER_LIST_URL, {"username": driver_username}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, driver_username)
        self.assertEqual(len(response.context["driver_list"]), 1)
        self.assertEqual(
            response.context["driver_list"][0].username, driver_username
        )

    def test_driver_search_not_found(self):
        response = self.client.get(
            DRIVER_LIST_URL, {"username": "NonExistentDriver"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["driver_list"], []
        )

    def test_car_create(self):
        initial_count = Car.objects.count()
        driver_pks = [self.user.pk]
        form_data = {
            "model": "NewCar",
            "manufacturer": self.manufacturer.pk,
            "drivers": driver_pks,
        }
        response = self.client.post(reverse("taxi:car-create"), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, CAR_LIST_URL)
        self.assertEqual(Car.objects.count(), initial_count + 1)
        new_car = Car.objects.get(model="NewCar")
        self.assertEqual(
            list(new_car.drivers.values_list("pk", flat=True)), driver_pks
        )

    def test_car_update(self):
        other_driver = get_user_model().objects.create_user(
            username="other", password="pwd", license_number="DRV54321"
        )
        form_data = {
            "model": "UpdatedCar",
            "manufacturer": self.car.manufacturer.pk,
            "drivers": [other_driver.pk],
        }
        response = self.client.post(
            reverse("taxi:car-update", kwargs={"pk": self.car.pk}),
            data=form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, CAR_LIST_URL)
        self.car.refresh_from_db()
        self.assertEqual(self.car.model, "UpdatedCar")
        self.assertIn(other_driver, self.car.drivers.all())

    def test_car_delete(self):
        car_to_delete = Car.objects.create(
            model="ToDelete", manufacturer=self.manufacturer
        )
        initial_count = Car.objects.count()
        response = self.client.post(
            reverse("taxi:car-delete", kwargs={"pk": car_to_delete.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, CAR_LIST_URL)
        self.assertEqual(Car.objects.count(), initial_count - 1)
        with self.assertRaises(Car.DoesNotExist):
            Car.objects.get(pk=car_to_delete.pk)

    def test_driver_create(self):
        initial_count = get_user_model().objects.count()
        form_data = {
            "username": "newdriver",
            "password1": "ValidPassword123",
            "password2": "ValidPassword123",
            "license_number": "NEW12345",
            "first_name": "New",
            "last_name": "Driver",
        }
        response = self.client.post(
            reverse("taxi:driver-create"), data=form_data
        )
        if response.status_code == 200:
            form = response.context["form"]
            self.fail(f"Form validation failed with errors: {form.errors}")
        self.assertEqual(
            response.status_code,
            302,
            f"Expected 302 redirect, got {response.status_code}"
        )
        self.assertEqual(get_user_model().objects.count(), initial_count + 1)
        new_driver = get_user_model().objects.get(username="newdriver")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, new_driver.get_absolute_url())

    def test_driver_license_update(self):
        form_data = {"license_number": "VAL54321"}
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.pk}),
            data=form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, DRIVER_LIST_URL)
        self.user.refresh_from_db()
        self.assertEqual(self.user.license_number, "VAL54321")

    def test_driver_delete(self):
        driver_to_delete = get_user_model().objects.create_user(
            username="deleteme", password="pwd", license_number="DEL12345"
        )
        initial_count = get_user_model().objects.count()
        response = self.client.post(
            reverse("taxi:driver-delete", kwargs={"pk": driver_to_delete.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, DRIVER_LIST_URL)
        self.assertEqual(get_user_model().objects.count(), initial_count - 1)
        with self.assertRaises(get_user_model().DoesNotExist):
            get_user_model().objects.get(pk=driver_to_delete.pk)
