from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

URL_MANUFACTURER_LIST = reverse("taxi:manufacturer-list")
URL_CAR_LIST = reverse("taxi:car-list")
URL_CAR_DETAIL = reverse("taxi:car-detail", args=[1])
URL_DRIVER_LIST = reverse("taxi:driver-list")
URL_DRIVER_DETAIL = reverse("taxi:driver-detail", args=[1])


class AdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="superadmin",
            password="P@s$w0rd432"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver_test",
            password="Drivertest123",
            license_number="TTT12365"
        )

    def test_driver_license_number_in_display_list(self):
        """Test, that license number display in display list of admin page"""
        url = reverse("admin:taxi_driver_changelist")
        result = self.client.get(url)

        self.assertContains(result, self.driver.license_number)

    def test_driver_license_number_in_detail_page(self):
        """Test, that license number display in driver admin page"""
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        result = self.client.get(url)

        self.assertContains(result, self.driver.license_number)


class ModelsTests(TestCase):
    name_temp = "nAme"
    country_temp = "coUntry"
    username_temp = "uSerNAME"
    first_name_temp = "First_nmae"
    last_name_temp = "LAST_name"
    model_temp = "MOdel"

    def create_manufacture(self):
        return Manufacturer.objects.create(
            name=self.name_temp,
            country=self.country_temp)

    def test_manufacturer_str(self):
        manufacture = self.create_manufacture()
        self.assertEqual(
            str(manufacture),
            f"{self.name_temp} {self.country_temp}"
        )

    def test_driver_str(self):
        driver = Driver.objects.create(
            username=self.username_temp,
            first_name=self.first_name_temp,
            last_name=self.last_name_temp
        )
        self.assertEqual(
            str(driver),
            f"{self.username_temp} "
            f"({self.first_name_temp} "
            f"{self.last_name_temp})"
        )

    def test_car_str(self):
        manufacturer_ = self.create_manufacture()
        car = Car.objects.create(
            model=self.model_temp,
            manufacturer=manufacturer_
        )
        self.assertEqual(str(car), f"{self.model_temp}")

    def test_driver_with_license_number(self):
        username = "dim_test"
        pwd = "P@s$w0rd135"
        first_name = "dim"
        last_name = "dimdim"
        license_number = "AAA54321"
        driver = get_user_model().objects.create_user(
            username=username,
            password=pwd,
            first_name=first_name,
            last_name=last_name,
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(pwd))


class ViewsLoginRequiredTests(TestCase):

    def test_manufacturer_list_login_required(self):
        result = self.client.get(URL_MANUFACTURER_LIST)

        self.assertNotEqual(result.status_code, 200)

    def test_car_list_login_required(self):
        result = self.client.get(URL_CAR_LIST)

        self.assertNotEqual(result.status_code, 200)

    def test_driver_list_login_required(self):
        result = self.client.get(URL_CAR_LIST)

        self.assertNotEqual(result.status_code, 200)


class ViewsDisplayListTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="TestUser123"
        )
        self.client.force_login(self.user)

    def test_manufacturer_data_list(self):
        Manufacturer.objects.create(name="Mazda")
        Manufacturer.objects.create(name="Toyota")
        need_list = list(Manufacturer.objects.all())
        result = self.client.get(URL_MANUFACTURER_LIST)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(list(result.context["manufacturer_list"]), need_list)

    def test_car_data_list(self):
        mazda = Manufacturer.objects.create(name="Mazda")
        toyota = Manufacturer.objects.create(name="Toyota")
        car = Car.objects.create(manufacturer=mazda, model="CX7")
        car.drivers.add(self.user.id)
        Car.objects.create(manufacturer=toyota, model="Prado")
        car.drivers.add(self.user.id)
        need_list = list(Car.objects.all())
        result = self.client.get(URL_CAR_LIST)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(list(result.context["car_list"]), need_list)

    def test_driver_data_list(self):
        need_list = list(Driver.objects.all())
        result = self.client.get(URL_DRIVER_LIST)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(list(result.context["driver_list"]), need_list)


class ViewsDispDetailTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="TestUser123"
        )
        self.client.force_login(self.user)

    def test_car_detail_view(self):

        mazda = Manufacturer.objects.create(name="Mazda")
        car = Car.objects.create(manufacturer=mazda, model="CX7")
        car.drivers.add(self.user.id)
        result = self.client.get(URL_CAR_DETAIL)
        self.assertEqual(result.status_code, 200)

    def test_driver_detail_view(self):

        mazda = Manufacturer.objects.create(name="Mazda")
        car = Car.objects.create(manufacturer=mazda, model="CX7")
        car.drivers.add(self.user.id)
        result = self.client.get(URL_DRIVER_DETAIL)
        self.assertEqual(result.status_code, 200)
