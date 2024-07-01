from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

HOME_URL = reverse("taxi:index")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")
CAR_LIST_URL = reverse("taxi:car-list")
CAR_CREATE_URL = reverse("taxi:car-create")
DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")


class PublicTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test",
            country="USA"
        )
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="PASSWORD",
        )
        self.car = Car.objects.create(
            model="test",
            manufacturer=self.manufacturer
        )
        self.car.drivers.set([self.driver])

    def test_login_required_index(self):
        res = self.client.get(HOME_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_manufacturer_list(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_manufacturer_create(self):
        res = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_manufacturer_update(self):
        res = self.client.get(reverse(
            "taxi:manufacturer-update",
            args=[self.manufacturer.id]
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_manufacturer_delete(self):
        res = self.client.get(reverse(
            "taxi:manufacturer-delete",
            args=[self.manufacturer.id]
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car_list(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car_detail(self):
        res = self.client.get(reverse(
            "taxi:car-detail",
            args=[self.car.id]
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car_create(self):
        res = self.client.get(CAR_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car_update(self):
        res = self.client.get(reverse(
            "taxi:car-update",
            args=[self.car.id]
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car_delete(self):
        res = self.client.get(reverse(
            "taxi:car-delete",
            args=[self.car.id]
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver_list(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver_detail(self):
        res = self.client.get(reverse(
            "taxi:driver-detail",
            args=[self.driver.id]
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver_create(self):
        res = self.client.get(DRIVER_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver_update(self):
        res = self.client.get(reverse(
            "taxi:driver-update",
            args=[self.driver.id]
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver_delete(self):
        res = self.client.get(reverse(
            "taxi:driver-delete",
            args=[self.driver.id]
        ))
        self.assertNotEqual(res.status_code, 200)


class IndexViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="PASSWORD"
        )
        self.client.force_login(self.user)

    def test_index(self):
        response = self.client.get(HOME_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")


class ManufacturerListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Test",
            country="USA"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="abc",
            country="USA"
        )

    def test_manufacturer_list_view(self):
        Manufacturer.objects.create(name="Test3", country="USA")
        response = self.client.get(MANUFACTURER_LIST_URL)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_manufacturer_list_view_search(self):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": "Test"})
        self.assertContains(response, self.manufacturer.name)
        self.assertNotContains(response, self.manufacturer2.name)


class ManufacturerCreateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.force_login(self.user)

    def test_manufacturer_create_view(self):
        response = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_form.html"
        )

    def test_manufacturer_create(self):
        test_data = {"name": "test11", "country": "tess"}
        response = self.client.post(MANUFACTURER_CREATE_URL, data=test_data)
        self.assertEqual(response.status_code, 302)
        new_manufacturer = Manufacturer.objects.get(name=test_data["name"])
        self.assertEqual(new_manufacturer.name, test_data["name"])
        self.assertEqual(new_manufacturer.country, test_data["country"])


class ManufacturerUpdateDeleteViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Test",
            country="USA"
        )

    def test_manufacturer_update(self):
        url = reverse("taxi:manufacturer-update", args=[self.manufacturer.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")

    def test_manufacturer_delete(self):
        url = reverse("taxi:manufacturer-delete", args=[self.manufacturer.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_confirm_delete.html"
        )


class CarListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.car = Car.objects.create(
            model="Test Car",
            manufacturer=self.manufacturer
        )
        self.car.drivers.set([self.user])
        self.car1 = Car.objects.create(
            model="abc",
            manufacturer=self.manufacturer
        )
        self.car1.drivers.set([self.user])

    def test_car_list_view(self):
        response = self.client.get(CAR_LIST_URL)
        cars = Car.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_list_view_search(self):
        response = self.client.get(CAR_LIST_URL, {"model": "Test"})
        self.assertContains(response, self.car.model)
        self.assertNotContains(response, self.car1.model)


class CarCreateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test Country"
        )
        self.driver = get_user_model().objects.create_user(
            username="testuser1",
            password="password",
            license_number="ABC12345",
        )

    def test_car_create_view(self):
        response = self.client.get(CAR_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_car_create(self):
        form_data = {
            "model": "Test Car",
            "manufacturer": self.manufacturer.id,
            "drivers": self.driver.id
        }
        response = self.client.post(CAR_CREATE_URL, data=form_data)
        self.assertEqual(response.status_code, 302)
        new_car = Car.objects.get(model=form_data["model"])

        self.assertEqual(new_car.model, form_data["model"])
        self.assertEqual(new_car.manufacturer.id, form_data["manufacturer"])
        self.assertIn(self.driver, new_car.drivers.all())


class CarUpdateDeleteViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.driver = get_user_model().objects.create_user(
            username="testuser1",
            password="password",
            license_number="ABC12345",
        )
        self.car = Car.objects.create(model="test", manufacturer=manufacturer)

    def test_car_update(self):
        test_data = {
            "model": "bmw",
            "manufacturer": self.car.manufacturer.id,
            "drivers": self.driver.id
        }
        url = reverse("taxi:car-update", args=[self.car.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")

        response = self.client.post(url, test_data)
        self.assertEqual(response.status_code, 302)

        self.car.refresh_from_db()
        self.assertEqual(self.car.model, test_data["model"])

    def test_car_delete(self):
        url = reverse("taxi:car-delete", args=[self.car.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_confirm_delete.html")


class DriverListViewTests(TestCase):
    def setUp(self):
        self.driver1 = get_user_model().objects.create_user(
            username="driver1",
            password="testpassword1",
            license_number="ABC12345"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver2",
            password="testpassword2",
            license_number="ABC12346"
        )
        self.client.force_login(self.driver1)

    def test_driver_list_view(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver1.username)
        self.assertContains(response, self.driver2.username)

    def test_driver_list_view_search(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "driver1"})
        self.assertContains(response, self.driver1.username)
        self.assertNotContains(response, self.driver2.username)

    def test_driver_list_view_no_results(self):
        response = self.client.get(DRIVER_LIST_URL, {
            "username": "nonexistent_driver"
        })
        self.assertContains(response, "There are no drivers in the service.")


class DriverDetailViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.force_login(self.user)
        self.driver = get_user_model().objects.create(
            username="driver", password="password", license_number="ABC12345")

    def test_driver_detail_view(self):
        response = self.client.get(reverse(
            "taxi:driver-detail",
            args=[self.driver.id]
        ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")
        self.assertIn("driver", response.context)


class DriverUpdateDeleteTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.force_login(self.user)
        self.driver = get_user_model().objects.create(
            username="driver",
            password="password",
            license_number="ABC12345"
        )

    def test_driver_update(self):
        url = reverse("taxi:driver-update", args=[self.driver.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_driver_delete(self):
        url = reverse("taxi:driver-delete", args=[self.driver.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_confirm_delete.html")


class ToggleAssignToCarViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.car = Car.objects.create(
            model="Test Car",
            manufacturer=self.manufacturer
        )
        self.car.drivers.set([self.user])

    def test_toggle_assign_to_car_add(self):
        self.user.cars.remove(self.car)
        response = self.client.get(reverse(
            "taxi:toggle-car-assign",
            kwargs={"pk": self.car.id}
        ))
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.car, self.user.cars.all())

    def test_toggle_assign_to_car_remove(self):
        response = self.client.get(reverse(
            "taxi:toggle-car-assign",
            kwargs={"pk": self.car.id}
        ))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.car, self.user.cars.all())


class DriverLicenseUpdateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.force_login(self.user)
        self.driver = get_user_model().objects.create(
            username="testdriver",
            password="password",
            license_number="ABC12345"
        )
        self.url = reverse("taxi:driver-update", args=[self.driver.id])

    def test_driver_update_view_accessible(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_valid_license_update(self):
        valid_license_number = "XYZ67890"
        response = self.client.post(self.url, {
            "license_number": valid_license_number
        })
        self.assertEqual(response.status_code, 302)
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.license_number, valid_license_number)

    def test_invalid_license_update_length(self):
        invalid_license_number = "XYZ123"
        response = self.client.post(self.url, {
            "license_number": invalid_license_number
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "license_number",
            "License number should consist of 8 characters"
        )

    def test_invalid_license_update_format_uppercase(self):
        invalid_license_number = "xyz12345"
        response = self.client.post(self.url, {
            "license_number": invalid_license_number
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "license_number",
            "First 3 characters should be uppercase letters"
        )

    def test_invalid_license_update_format_digits(self):
        invalid_license_number = "XYZ12abc"
        response = self.client.post(self.url, {
            "license_number": invalid_license_number
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "license_number",
            "Last 5 characters should be digits"
        )
