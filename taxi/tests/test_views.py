from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car


class PublicUrlTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        url_names = [
            "taxi:index",
            "taxi:manufacturer-list",
            "taxi:car-list",
            "taxi:driver-list",
        ]

        for name in url_names:
            url = reverse(name)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith("/accounts/login/"))


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123"
        )
        self.client.force_login(self.user)

        Manufacturer.objects.create(name="Audi", country="Germany")
        Manufacturer.objects.create(name="BMW", country="Germany")

    def test_manufacturer_list_view(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertEqual(len(response.context["manufacturer_list"]), 2)

    def test_manufacturer_search(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, data={"name": "Audi"})

        manufacturer_list = response.context["manufacturer_list"]
        self.assertEqual(len(manufacturer_list), 1)
        self.assertEqual(manufacturer_list[0].name, "Audi")

    def test_create_manufacturer(self):
        form_data = {
            "name": "Toyota",
            "country": "Japan"
        }
        url = reverse("taxi:manufacturer-create")
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Manufacturer.objects.filter(name="Toyota").exists())

    def test_update_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="ZAZ",
            country="Ukraine"
        )
        url = reverse(
            "taxi:manufacturer-update",
            kwargs={"pk": manufacturer.pk}
        )

        new_data = {"name": "Daewoo", "country": "Korea"}
        response = self.client.post(url, data=new_data)

        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        manufacturer.refresh_from_db()
        self.assertEqual(manufacturer.name, "Daewoo")
        self.assertEqual(manufacturer.country, "Korea")

    def test_delete_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="Volvo",
            country="Sweden"
        )
        url = reverse(
            "taxi:manufacturer-delete",
            kwargs={"pk": manufacturer.pk}
        )

        response = self.client.post(url)

        self.assertRedirects(response, reverse("taxi:manufacturer-list"))

        self.assertFalse(
            Manufacturer.objects.filter(
                pk=manufacturer.pk).exists()
        )


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password123"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="ZAZ",
            country="Ukraine"
        )
        self.car = Car.objects.create(
            model="Lanos",
            manufacturer=self.manufacturer
        )

    def test_car_list_view_queryset(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lanos")

        with self.assertNumQueries(4):
            self.client.get(reverse("taxi:car-list"))

    def test_car_search(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, data={"model": "Lanos"})

        car_list = response.context["car_list"]
        self.assertEqual(len(car_list), 1)
        self.assertEqual(car_list[0].model, "Lanos")

    def test_toggle_assign_to_car(self):
        url = reverse("taxi:toggle-car-assign", kwargs={"pk": self.car.pk})

        self.assertNotIn(self.user, self.car.drivers.all())

        response = self.client.post(url)
        self.assertRedirects(
            response, reverse("taxi:car-detail", kwargs={"pk": self.car.pk})
        )

        self.car.refresh_from_db()
        self.assertIn(self.user, self.car.drivers.all())

        self.client.post(url)
        self.car.refresh_from_db()
        self.assertNotIn(self.user, self.car.drivers.all())

    def test_create_car(self):
        url = reverse("taxi:car-create")
        form_data = {
            "model": "Camry",
            "manufacturer": self.manufacturer.pk,
            "drivers": [self.user.pk]
        }

        response = self.client.post(url, data=form_data)

        self.assertRedirects(response, reverse("taxi:car-list"))
        self.assertTrue(Car.objects.filter(model="Camry").exists())

    def test_update_car(self):
        url = reverse("taxi:car-update", kwargs={"pk": self.car.pk})
        new_data = {
            "model": "Sens",
            "manufacturer": self.manufacturer.pk,
            "drivers": [self.user.pk]
        }

        response = self.client.post(url, data=new_data)

        self.assertRedirects(response, reverse("taxi:car-list"))

        self.car.refresh_from_db()
        self.assertEqual(self.car.model, "Sens")

    def test_delete_car(self):
        url = reverse("taxi:car-delete", kwargs={"pk": self.car.pk})

        response = self.client.post(url)

        self.assertRedirects(response, reverse("taxi:car-list"))
        self.assertFalse(Car.objects.filter(pk=self.car.pk).exists())


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin_tester",
            password="password123",
            license_number="ADM12345"
        )
        self.client.force_login(self.user)

    def test_driver_list_view(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertEqual(len(response.context["driver_list"]), 1)

    def test_driver_detail_view(self):
        url = reverse("taxi:driver-detail", kwargs={"pk": self.user.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")
        self.assertEqual(response.context["driver"], self.user)

    def test_create_driver(self):
        url = reverse("taxi:driver-create")
        form_data = {
            "username": "new_driver",
            "password1": "SecurePass123!",
            "password2": "SecurePass123!",
            "first_name": "Admin",
            "last_name": "Adminovich",
            "license_number": "NEW88888"
        }

        response = self.client.post(url, data=form_data)

        new_driver = get_user_model().objects.get(username="new_driver")
        self.assertRedirects(response, new_driver.get_absolute_url())

        self.assertTrue(
            get_user_model().objects.filter(license_number="NEW88888").exists()
        )

    def test_update_driver_license(self):
        driver_to_update = get_user_model().objects.create_user(
            username="driver_upt",
            password="p",
            license_number="OLD00000"
        )

        url = reverse("taxi:driver-update", kwargs={"pk": driver_to_update.pk})

        new_data = {
            "license_number": "UPD11111"
        }

        response = self.client.post(url, data=new_data)

        self.assertRedirects(response, reverse("taxi:driver-list"))

        driver_to_update.refresh_from_db()
        self.assertEqual(driver_to_update.license_number, "UPD11111")
        self.assertEqual(driver_to_update.username, "driver_upt")

    def test_delete_driver(self):
        driver_to_delete = get_user_model().objects.create_user(
            username="driver_del",
            password="p",
            license_number="DEL99999"
        )

        url = reverse("taxi:driver-delete", kwargs={"pk": driver_to_delete.pk})

        response = self.client.post(url)

        self.assertRedirects(response, reverse("taxi:driver-list"))

        self.assertFalse(
            get_user_model().objects.filter(pk=driver_to_delete.pk).exists()
        )

    def test_driver_search(self):
        user1 = get_user_model().objects.create_user(
            username="alice",
            password="p",
            license_number="OLD00001"
        )
        user2 = get_user_model().objects.create_user(
            username="albert",
            password="p",
            license_number="OLD00002"
        )
        user3 = get_user_model().objects.create_user(
            username="bob",
            password="p",
            license_number="OLD00003"
        )

        url = reverse("taxi:driver-list")

        response = self.client.get(url, data={"username": "al"})
        driver_list = response.context["driver_list"]

        self.assertIn(user1, driver_list)
        self.assertIn(user2, driver_list)
        self.assertNotIn(user3, driver_list)

        response = self.client.get(url, data={"username": "bob"})
        driver_list = response.context["driver_list"]

        self.assertIn(user3, driver_list)
        self.assertNotIn(user1, driver_list)
        self.assertEqual(len(driver_list), 1)

        response = self.client.get(url, data={"username": "zorro"})
        driver_list = response.context["driver_list"]
        self.assertEqual(len(driver_list), 0)


class IndexViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password123"
        )
        self.client.force_login(self.user)

    def test_index_view_context(self):
        Manufacturer.objects.create(name="A", country="B")
        Car.objects.create(model="C", manufacturer_id=1)

        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_manufacturers"], 1)
        self.assertEqual(response.context["num_cars"], 1)
        self.assertEqual(response.context["num_drivers"], 1)

        self.assertEqual(response.context["num_visits"], 1)

        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.context["num_visits"], 2)
