from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm
from taxi.models import Manufacturer, Car, Driver


class ModelTestClass(TestCase):

    def test_manufacturer_model(self):
        manufacturer = Manufacturer.objects.create(
            name="Ivan",
            country="Ukraine"
        )
        manufacturer.refresh_from_db()
        self.assertEqual(str(manufacturer), "Ivan Ukraine")

    def test_driver_model(self):
        driver = get_user_model().objects.create_user(
            username="Testik",
            first_name="Test",
            last_name="Testiuk"
        )
        driver.refresh_from_db()
        self.assertEqual(str(driver), "Testik (Test Testiuk)")

    def test_car_model(self):
        driver1 = get_user_model().objects.create_user(
            username="driver1",
            first_name="Fill1",
            last_name="Norton1",
            license_number="1234",
        )
        driver2 = get_user_model().objects.create_user(
            username="driver2",
            first_name="Fill2",
            last_name="Norton2",
            license_number="12345",
        )
        manufacturer = Manufacturer.objects.create(
            name="Zaz",
            country="Ukraine"
        )
        driver1.refresh_from_db()
        driver2.refresh_from_db()
        manufacturer.refresh_from_db()
        car = Car.objects.create(
            model="Lanos",
            manufacturer_id=manufacturer.id
        )
        car.drivers.set([driver1, driver2])

        self.assertEqual(str(car), "Lanos")


class AdminPanelTestClass(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123"
        )
        self.client.force_login(self.admin_user)

    def test_car_search_field_exists(self):
        url = reverse("admin:taxi_car_changelist")
        res = self.client.get(url)

        self.assertContains(res, 'name="q"')

    def test_license_number_in_driver_list_exists(self):
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, "license_number")

    def test_license_number_in_driver_add_exists(self):
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)

        self.assertContains(res, "license_number")

    def test_additional_info_in_driver_add_exists(self):
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)

        self.assertContains(res, "Additional info")

    def test_first_name_in_driver_add_exists(self):
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)

        self.assertContains(res, "first_name")

    def test_last_name_in_driver_add_exists(self):
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)

        self.assertContains(res, "last_name")

    def test_license_number_in_driver_change(self):
        url = reverse(
            "admin:taxi_driver_change",
            args=[self.admin_user.id]
        )
        res = self.client.get(url)

        self.assertContains(res, "license_number")

    def test_additional_info_in_driver_change(self):
        url = reverse(
            "admin:taxi_driver_change",
            args=[self.admin_user.id]
        )
        res = self.client.get(url)

        self.assertContains(res, "Additional info")


class ManufacturerListViewTest(TestCase):
    def setUp(self) -> None:
        self.url = reverse("taxi:manufacturer-list")
        Manufacturer.objects.create(
            name="Test1",
            country="TestCountry"
        )
        Manufacturer.objects.create(
            name="Test2",
            country="TestCountry"
        )

    def test_login_required(self):
        res = self.client.get(self.url)
        self.assertNotEqual(res.status_code, 200)

    def test_view_accessible_for_logged_in_user(self):
        admin_user = get_user_model().objects.create_superuser(
            "superuser"
        )
        self.client.force_login(admin_user)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)

    def test_manufacturer_list_as_expected(self):
        admin_user = get_user_model().objects.create_superuser(
            "superuser"
        )
        self.client.force_login(admin_user)
        res = self.client.get(self.url)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(res.context["manufacturer_list"]), list(manufacturers)
        )

    def test_manufacturer_list_filtered(self):
        admin_user = get_user_model().objects.create_superuser(
            "superuser"
        )
        self.client.force_login(admin_user)
        res = self.client.get(self.url + "?name=Test1")
        expected_queryset = (Manufacturer.objects.filter(name="Test1")
                             .order_by("name"))
        self.assertQuerySetEqual(
            res.context["manufacturer_list"],
            expected_queryset
        )


class CarListViewTest(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            "superuser"
        )
        self.client.force_login(self.admin_user)
        self.url = reverse("taxi:car-list")
        man1 = Manufacturer.objects.create(
            name="Man1",
            country="TestCountry"
        )
        man2 = Manufacturer.objects.create(
            name="Man2",
            country="TestCountry"
        )

        Car.objects.create(
            manufacturer=man1,
            model="Model1"
        )
        Car.objects.create(
            manufacturer=man2,
            model="Model2"
        )
        Car.objects.create(
            manufacturer=man1,
            model="Model3"
        )

    def test_car_list_filtered(self):
        res = self.client.get(self.url + "?model=Model1")
        expected_queryset = (Car.objects.filter(model="Model1")
                             .order_by("model"))
        self.assertQuerySetEqual(
            res.context["car_list"],
            expected_queryset
        )


class DriverListViewTest(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            "superuser"
        )
        self.client.force_login(self.admin_user)
        self.url = reverse("taxi:driver-list")
        Driver.objects.create(
            username="Driver1",
            license_number="CBA54321"
        )
        Driver.objects.create(
            username="Driver2",
            license_number="ABC12345"
        )

    def test_driver_list_filtered(self):
        res = self.client.get(self.url + "?username=Driver2")
        expected_queryset = (Driver.objects.filter(username="Driver2")
                             .order_by("username"))
        self.assertQuerySetEqual(
            res.context["driver_list"],
            expected_queryset
        )


class FormTest(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "DriverUserName234",
            "password1": "user12test12",
            "password2": "user12test12",
            "license_number": "LSN12345",
            "first_name": "DriverFirstName",
            "last_name": "DriverLastName",
        }

    def test_driver_form_is_valid(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["username"], self.form_data["username"]
        )
        self.assertEqual(
            form.cleaned_data["password1"], self.form_data["password1"]
        )
        self.assertEqual(
            form.cleaned_data["license_number"],
            self.form_data["license_number"]
        )
        self.assertEqual(
            form.cleaned_data["first_name"],
            self.form_data["first_name"]
        )
        self.assertEqual(
            form.cleaned_data["last_name"],
            self.form_data["last_name"]
        )

        def test_driver_form_is_invalid_password_check(self):
            form_data = {
                "username": "DriverUserName234",
                "password1": "user12test13",
                "password2": "user12test12",
                "license_number": "LSN12345",
                "first_name": "DriverFirstName",
                "last_name": "DriverLastName",
            }
            form = DriverCreationForm(data=form_data)
            self.assertFalse(form.is_valid())

        def test_driver_form_is_invalid_license_number(self):
            form_data = {
                "username": "DriverUserName234",
                "password1": "user12test13",
                "password2": "user12test13",
                "license_number": "LSn12345",
                "first_name": "DriverFirstName",
                "last_name": "DriverLastName",
            }
            form = DriverCreationForm(data=form_data)
            self.assertFalse(form.is_valid())

        def test_driver_creation_form(self):
            self.admin_user = get_user_model().objects.create_superuser(
                "superuser"
            )
            self.client.force_login(self.admin_user)
            url = reverse("taxi:driver-create")
            self.client.post(url, data=self.form_data)
            driver = get_user_model().objects.get(
                username=self.form_data["username"]
            )
            self.assertEqual(driver.username, self.form_data["username"])
            self.assertEqual(driver.first_name, self.form_data["first_name"])
            self.assertEqual(driver.last_name, self.form_data["last_name"])
