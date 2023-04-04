from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver

CARS_LIST_URL = reverse("taxi:car-list")
DRIVERS_LIST_URL = reverse("taxi:driver-list")


class PublicCarTests(TestCase):
    def test_car_list_login_required(self):
        response = self.client.get(CARS_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_car_detail_login_required(self):
        car_detail_url = reverse("taxi:car-detail", args=[1])
        response = self.client.get(car_detail_url)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user("test", "password123")
        self.client.force_login(self.user)

    def test_retrieve_car_list(self):
        manufacturer = Manufacturer.objects.create(
            name="Volkswagen", country="Germany"
        )
        Car.objects.create(model="test", manufacturer=manufacturer)
        Car.objects.create(model="TEST", manufacturer=manufacturer)

        response = self.client.get(CARS_LIST_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_car_detail(self):
        manufacturer = Manufacturer.objects.create(
            name="Volkswagen", country="Germany"
        )
        car = Car.objects.create(model="test", manufacturer=manufacturer)

        car_detail_url = reverse("taxi:car-detail", args=[1])
        response = self.client.get(car_detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], car)
        self.assertTemplateUsed(response, "taxi/car_detail.html")


class PublicDriverTests(TestCase):
    def test_driver_list_login_required(self):
        response = self.client.get(DRIVERS_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_driver_detail_login_required(self):
        driver_detail_url = reverse("taxi:driver-detail", args=[1])
        response = self.client.get(driver_detail_url)

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user("test", "password123")
        self.client.force_login(self.user)

    def test_retrieve_driver_list(self):
        get_user_model().objects.create_user(
            username="driver1",
            password="password123",
            first_name="Driver1",
            last_name="Lastname1",
            license_number="1111",
        )
        get_user_model().objects.create_user(
            username="driver2",
            password="password123",
            first_name="Driver2",
            last_name="Lastname2",
            license_number="2222",
        )

        response = self.client.get(DRIVERS_LIST_URL)
        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_retrieve_driver_detail(self):
        driver = get_user_model().objects.create_user(
            username="driver1",
            password="user12345",
            first_name="Driver1",
            last_name="Lastname1",
            license_number="ASD87654",
        )

        driver_detail_url = reverse("taxi:driver-detail", args=[driver.pk])

        response = self.client.get(driver_detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], driver)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_delete_driver(self):
        driver = get_user_model().objects.create(
            username="not_admin.user",
            license_number="NOT12345",
            first_name="Not Admin",
            last_name="User",
            password="1qazcde3",
        )
        response = self.client.post(
            reverse("taxi:driver-delete", kwargs={"pk": driver.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            get_user_model().objects.filter(id=driver.id).exists()
        )


class ManufacturerListViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("taxi:manufacturer-list")

        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )

    def test_manufacturer_list_view(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_list_context(self):
        self.client.force_login(self.user)

        Manufacturer.objects.create(name="Volkswagen", country="Germany")
        Manufacturer.objects.create(name="Toyota", country="Japan")
        response = self.client.get(self.url)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 2)
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )


class UpdateDriverLicenseTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass", license_number="ABC12345"
        )
        self.client.force_login(self.user)

    def test_update_driver_license_number_with_valid_data(self):
        test_license_number = "CVB98765"
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.id}),
            data={"license_number": test_license_number},
        )
        self.assertEqual(response.status_code, 302)

    def test_update_driver_license_number_with_not_valid_data(self):
        test_license_number = "A111"
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.id}),
            data={"license_number": test_license_number},
        )
        self.assertEqual(response.status_code, 200)


class ToggleAssignToCarTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.manufacturer = Manufacturer.objects.create(
            name='Test Manufacturer'
        )
        self.car = Car.objects.create(
            model='Test Model',
            manufacturer=self.manufacturer
        )
        self.driver = Driver.objects.create(
            username='testuser',
            password='testpass',
            license_number='1234'
        )

    def test_toggle_assign_to_car(self):
        self.client.force_login(self.driver)
        url = reverse('taxi:toggle-car-assign', args=[self.car.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.assertIn(self.driver, self.car.drivers.all())

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.assertNotIn(self.driver, self.car.drivers.all())
