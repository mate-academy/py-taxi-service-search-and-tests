from django.test import TestCase, Client
from django.urls import reverse

from django.db.utils import IntegrityError

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.assertEqual(str(manufacturer), "Toyota Japan")

    def test_manufacturer_ordering(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Audi", country="Germany")
        manufacturers = list(Manufacturer.objects.all())
        self.assertEqual(manufacturers[0].name, "Audi")
        self.assertEqual(manufacturers[1].name, "BMW")

    def test_driver_str(self):
        driver = Driver.objects.create_user(
            username="driver1",
            password="test1234",
            license_number="ABC12345",
            first_name="John",
            last_name="Doe",
        )
        self.assertEqual(str(driver), "driver1 (John Doe)")

    def test_driver_license_number_unique(self):
        Driver.objects.create_user(
            username="driver1",
            password="test1234",
            license_number="ABC12345",
        )
        with self.assertRaises(IntegrityError):
            Driver.objects.create_user(
                username="driver2",
                password="test1234",
                license_number="ABC12345",
            )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        car = Car.objects.create(model="Camry", manufacturer=manufacturer)
        self.assertEqual(str(car), "Camry")

    def test_car_drivers_many_to_many(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        car = Car.objects.create(model="Camry", manufacturer=manufacturer)
        driver1 = Driver.objects.create_user(
            username="driver1",
            password="test1234",
            license_number="ABC12345",
        )
        driver2 = Driver.objects.create_user(
            username="driver2",
            password="test1234",
            license_number="DEF67890",
        )
        car.drivers.add(driver1, driver2)
        self.assertEqual(car.drivers.count(), 2)
        self.assertIn(driver1, car.drivers.all())
        self.assertIn(driver2, car.drivers.all())


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Driver.objects.create_user(
            username="testdriver",
            password="test1234",
            license_number="ABC12345",
            first_name="Test",
            last_name="User",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.user)

    def test_index_view(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")
        self.assertContains(response, "testdriver")
        self.assertContains(response, "Drivers:")
        self.assertContains(response, "Cars:")
        self.assertContains(response, "Manufacturers:")

    def test_index_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    # Manufacturer view tests
    def test_manufacturer_list_view(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Japan")

    def test_manufacturer_list_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 302)

    def test_manufacturer_create_view_get(self):
        response = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")

    def test_manufacturer_create_view_post(self):
        response = self.client.post(
            reverse("taxi:manufacturer-create"),
            {"name": "Honda", "country": "Japan"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Manufacturer.objects.filter(name="Honda").exists())

    def test_manufacturer_update_view(self):
        response = self.client.post(
            reverse(
                "taxi:manufacturer-update",
                kwargs={"pk": self.manufacturer.pk}
            ),
            {"name": "Toyota Updated", "country": "Japan"},
        )
        self.assertEqual(response.status_code, 302)
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, "Toyota Updated")

    def test_manufacturer_delete_view(self):
        response = self.client.post(
            reverse(
                "taxi:manufacturer-delete",
                kwargs={"pk": self.manufacturer.pk},
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Manufacturer.objects.filter(pk=self.manufacturer.pk).exists()
        )

    # Car view tests
    def test_car_list_view(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertContains(response, "Camry")
        self.assertContains(response, "Toyota")

    def test_car_detail_view(self):
        response = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": self.car.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")
        self.assertContains(response, "Camry")
        self.assertContains(response, "Toyota")

    def test_car_create_view_get(self):
        response = self.client.get(reverse("taxi:car-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_car_create_view_post(self):
        response = self.client.post(
            reverse("taxi:car-create"),
            {"model": "Corolla", "manufacturer": self.manufacturer.pk},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Car.objects.filter(model="Corolla").exists())

    def test_car_update_view(self):
        response = self.client.post(
            reverse("taxi:car-update", kwargs={"pk": self.car.pk}),
            {"model": "Camry Updated", "manufacturer": self.manufacturer.pk},
        )
        self.assertEqual(response.status_code, 302)
        self.car.refresh_from_db()
        self.assertEqual(self.car.model, "Camry Updated")

    def test_car_delete_view(self):
        response = self.client.post(
            reverse("taxi:car-delete", kwargs={"pk": self.car.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Car.objects.filter(pk=self.car.pk).exists())

    # Driver view tests
    def test_driver_list_view(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertContains(response, "testdriver")

    def test_driver_detail_view(self):
        response = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": self.user.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")
        self.assertContains(response, "testdriver")
        self.assertContains(response, "ABC12345")

    def test_driver_create_view_get(self):
        response = self.client.get(reverse("taxi:driver-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_driver_create_view_post(self):
        response = self.client.post(
            reverse("taxi:driver-create"),
            {
                "username": "newdriver",
                "password1": "complexpass123",
                "password2": "complexpass123",
                "license_number": "XYZ98765",
                "first_name": "New",
                "last_name": "Driver",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Driver.objects.filter(username="newdriver").exists())

    def test_driver_license_update_view(self):
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.pk}),
            {"license_number": "NEW12345"},
        )
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.license_number, "NEW12345")

    def test_driver_delete_view(self):
        other_driver = Driver.objects.create_user(
            username="otherdriver",
            password="test1234",
            license_number="OTH12345",
        )
        response = self.client.post(
            reverse("taxi:driver-delete", kwargs={"pk": other_driver.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Driver.objects.filter(pk=other_driver.pk).exists())

    def test_toggle_assign_to_car(self):
        new_car = Car.objects.create(
            model="Prius", manufacturer=self.manufacturer
        )
        self.assertNotIn(self.user, new_car.drivers.all())

        response = self.client.post(
            reverse("taxi:toggle-car-assign", kwargs={"pk": new_car.pk})
        )
        self.assertEqual(response.status_code, 302)
        new_car.refresh_from_db()
        self.assertIn(self.user, new_car.drivers.all())

        response = self.client.post(
            reverse("taxi:toggle-car-assign", kwargs={"pk": new_car.pk})
        )
        self.assertEqual(response.status_code, 302)
        new_car.refresh_from_db()
        self.assertNotIn(self.user, new_car.drivers.all())


class SearchTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Driver.objects.create_user(
            username="testdriver",
            password="test1234",
            license_number="ABC12345",
            first_name="Test",
            last_name="User",
        )
        self.client.force_login(self.user)
        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Honda", country="Japan"
        )
        self.manufacturer3 = Manufacturer.objects.create(
            name="BMW", country="Germany"
        )
        self.car1 = Car.objects.create(
            model="Camry", manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Corolla", manufacturer=self.manufacturer1
        )
        self.car3 = Car.objects.create(
            model="Civic", manufacturer=self.manufacturer2
        )
        self.car4 = Car.objects.create(
            model="X5", manufacturer=self.manufacturer3
        )
        self.driver1 = Driver.objects.create_user(
            username="alex_driver",
            password="test1234",
            license_number="DRV12345",
            first_name="Alex",
            last_name="Smith",
        )
        self.driver2 = Driver.objects.create_user(
            username="bob_driver",
            password="test1234",
            license_number="DRV67890",
            first_name="Bob",
            last_name="Jones",
        )
        self.driver3 = Driver.objects.create_user(
            username="charlie",
            password="test1234",
            license_number="DRV11111",
            first_name="Charlie",
            last_name="Brown",
        )

    # Manufacturer search tests
    def test_manufacturer_search_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Toy"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Honda")
        self.assertNotContains(response, "BMW")

    def test_manufacturer_search_case_insensitive(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "toy"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")

    def test_manufacturer_search_partial_match(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "ond"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Honda")
        self.assertNotContains(response, "Toyota")

    def test_manufacturer_search_empty_query_returns_all(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Honda")
        self.assertContains(response, "BMW")

    def test_manufacturer_search_no_results(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Ford"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Toyota")
        self.assertNotContains(response, "Honda")
        self.assertNotContains(response, "BMW")
        self.assertContains(
            response, "There are no manufacturers in the service."
        )

    # Car search tests
    def test_car_search_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Cam"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camry")
        self.assertNotContains(response, "Corolla")
        self.assertNotContains(response, "Civic")
        self.assertNotContains(response, "X5")

    def test_car_search_case_insensitive(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "cam"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camry")

    def test_car_search_partial_match(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "rol"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Camry")

    def test_car_search_empty_query_returns_all(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camry")
        self.assertContains(response, "Corolla")
        self.assertContains(response, "Civic")
        self.assertContains(response, "X5")

    def test_car_search_no_results(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Mustang"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Camry")
        self.assertNotContains(response, "Corolla")
        self.assertNotContains(response, "Civic")
        self.assertNotContains(response, "X5")
        self.assertContains(response, "There are no cars in taxi")

    # Driver search tests
    def test_driver_search_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "alex"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "alex_driver")
        self.assertNotContains(response, "bob_driver")
        self.assertNotContains(response, "charlie")

    def test_driver_search_case_insensitive(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "ALEx"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "alex_driver")

    def test_driver_search_partial_match(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "bob"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "bob_driver")
        self.assertNotContains(response, "alex_driver")

    def test_driver_search_empty_query_returns_all(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "alex_driver")
        self.assertContains(response, "bob_driver")
        self.assertContains(response, "charlie")
        self.assertContains(response, "testdriver")

    def test_driver_search_no_results(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "xyz"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "alex_driver")
        self.assertNotContains(response, "bob_driver")
        self.assertNotContains(response, "charlie")
        self.assertContains(response, "There are no drivers in the service.")


class FormTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )

    def test_driver_creation_form_valid(self):
        from taxi.forms import DriverCreationForm
        form_data = {
            "username": "newdriver",
            "password1": "complexpass123",
            "password2": "complexpass123",
            "license_number": "ABC12345",
            "first_name": "New",
            "last_name": "Driver",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_license_number(self):
        from taxi.forms import DriverCreationForm
        form_data = {
            "username": "newdriver",
            "password1": "complexpass123",
            "password2": "complexpass123",
            "license_number": "invalid",
            "first_name": "New",
            "last_name": "Driver",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_creation_form_password_mismatch(self):
        from taxi.forms import DriverCreationForm
        form_data = {
            "username": "newdriver",
            "password1": "complexpass123",
            "password2": "differentpass123",
            "license_number": "ABC12345",
            "first_name": "New",
            "last_name": "Driver",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_license_update_form_valid(self):
        from taxi.forms import DriverLicenseUpdateForm
        form_data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid(self):
        from taxi.forms import DriverLicenseUpdateForm
        form_data = {"license_number": "short"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_car_form_valid(self):
        from taxi.forms import CarForm
        form_data = {
            "model": "Camry",
            "manufacturer": self.manufacturer.pk,
            "drivers": [],
        }
        form = CarForm(data=form_data)
        if not form.is_valid():
            print("Form errors:", form.errors)
        self.assertTrue(form.is_valid())

    def test_car_form_invalid_missing_model(self):
        from taxi.forms import CarForm
        form_data = {"manufacturer": self.manufacturer.pk}
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_car_form_invalid_missing_manufacturer(self):
        from taxi.forms import CarForm
        form_data = {"model": "Camry"}
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())


class URLTests(TestCase):
    def test_index_url_resolves(self):
        self.assertEqual(reverse("taxi:index"), "/")

    def test_manufacturer_list_url(self):
        self.assertEqual(reverse("taxi:manufacturer-list"), "/manufacturers/")

    def test_manufacturer_create_url(self):
        self.assertEqual(
            reverse("taxi:manufacturer-create"), "/manufacturers/create/"
        )

    def test_manufacturer_update_url(self):
        self.assertEqual(
            reverse("taxi:manufacturer-update", kwargs={"pk": 1}),
            "/manufacturers/1/update/",
        )

    def test_manufacturer_delete_url(self):
        self.assertEqual(
            reverse("taxi:manufacturer-delete", kwargs={"pk": 1}),
            "/manufacturers/1/delete/",
        )

    def test_car_list_url(self):
        self.assertEqual(reverse("taxi:car-list"), "/cars/")

    def test_car_detail_url(self):
        self.assertEqual(
            reverse("taxi:car-detail", kwargs={"pk": 1}), "/cars/1/"
        )

    def test_car_create_url(self):
        self.assertEqual(reverse("taxi:car-create"), "/cars/create/")

    def test_car_update_url(self):
        self.assertEqual(
            reverse("taxi:car-update", kwargs={"pk": 1}), "/cars/1/update/"
        )

    def test_car_delete_url(self):
        self.assertEqual(
            reverse("taxi:car-delete", kwargs={"pk": 1}), "/cars/1/delete/"
        )

    def test_car_toggle_assign_url(self):
        self.assertEqual(
            reverse("taxi:toggle-car-assign", kwargs={"pk": 1}),
            "/cars/1/toggle-assign/",
        )

    def test_driver_list_url(self):
        self.assertEqual(reverse("taxi:driver-list"), "/drivers/")

    def test_driver_detail_url(self):
        self.assertEqual(
            reverse("taxi:driver-detail", kwargs={"pk": 1}), "/drivers/1/"
        )

    def test_driver_create_url(self):
        self.assertEqual(reverse("taxi:driver-create"), "/drivers/create/")

    def test_driver_update_url(self):
        self.assertEqual(
            reverse("taxi:driver-update", kwargs={"pk": 1}),
            "/drivers/1/update/",
        )

    def test_driver_delete_url(self):
        self.assertEqual(
            reverse("taxi:driver-delete", kwargs={"pk": 1}),
            "/drivers/1/delete/",
        )
