from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

INDEX_URL = reverse("taxi:index")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")
CAR_LIST_URL = reverse("taxi:car-list")
CAR_CREATE_URL = reverse("taxi:car-create")
DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")


class PublicViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_login_required(self):
        res = self.client.get(INDEX_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_manufacturer_list_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_car_list_login_required(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_driver_list_login_required(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.driver = get_user_model().objects.create_user(
            username="testdriver",
            password="testpassword123",
            license_number="DRV12345",
        )
        self.client.force_login(self.driver)
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.car = Car.objects.create(
            model="Prius",
            manufacturer=self.manufacturer,
        )

    def test_index_view(self):
        res = self.client.get(INDEX_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "taxi/index.html")
        self.assertEqual(res.context["num_drivers"], 1)
        self.assertEqual(res.context["num_cars"], 1)
        self.assertEqual(res.context["num_manufacturers"], 1)
        self.assertEqual(res.context["num_visits"], 1)

    def test_manufacturer_list_view(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")
        self.assertIn("manufacturer_list", res.context)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            [self.manufacturer],
        )

    def test_manufacturer_create_view(self):
        res = self.client.post(
            MANUFACTURER_CREATE_URL,
            {"name": "Ford", "country": "USA"},
        )
        self.assertEqual(res.status_code, 302)
        self.assertTrue(Manufacturer.objects.filter(name="Ford").exists())

    def test_manufacturer_update_view(self):
        update_url = reverse(
            "taxi:manufacturer-update",
            kwargs={"pk": self.manufacturer.pk},
        )
        res = self.client.post(
            update_url,
            {"name": "Toyota Updated", "country": "Japan"},
        )
        self.assertEqual(res.status_code, 302)
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, "Toyota Updated")

    def test_manufacturer_delete_view(self):
        delete_url = reverse(
            "taxi:manufacturer-delete",
            kwargs={"pk": self.manufacturer.pk},
        )
        res = self.client.post(delete_url)
        self.assertEqual(res.status_code, 302)
        self.assertFalse(
            Manufacturer.objects.filter(pk=self.manufacturer.pk).exists()
        )

    def test_car_list_view(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "taxi/car_list.html")
        self.assertIn("car_list", res.context)
        self.assertEqual(list(res.context["car_list"]), [self.car])

    def test_car_detail_view(self):
        detail_url = reverse("taxi:car-detail", kwargs={"pk": self.car.pk})
        res = self.client.get(detail_url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "taxi/car_detail.html")
        self.assertEqual(res.context["car"], self.car)

    def test_car_create_view(self):
        res = self.client.post(
            CAR_CREATE_URL,
            {
                "model": "Camry",
                "manufacturer": self.manufacturer.pk,
                "drivers": [self.driver.pk],
            },
        )
        self.assertEqual(res.status_code, 302)
        self.assertTrue(Car.objects.filter(model="Camry").exists())

    def test_car_update_view(self):
        update_url = reverse("taxi:car-update", kwargs={"pk": self.car.pk})
        res = self.client.post(
            update_url,
            {
                "model": "Prius Prime",
                "manufacturer": self.manufacturer.pk,
                "drivers": [self.driver.pk],
            },
        )
        self.assertEqual(res.status_code, 302)
        self.car.refresh_from_db()
        self.assertEqual(self.car.model, "Prius Prime")

    def test_car_delete_view(self):
        delete_url = reverse("taxi:car-delete", kwargs={"pk": self.car.pk})
        res = self.client.post(delete_url)
        self.assertEqual(res.status_code, 302)
        self.assertFalse(Car.objects.filter(pk=self.car.pk).exists())

    def test_toggle_assign_to_car(self):
        toggle_url = reverse(
            "taxi:toggle-car-assign",
            kwargs={"pk": self.car.pk},
        )
        # Assign driver
        res = self.client.get(toggle_url)
        self.assertEqual(res.status_code, 302)
        self.assertIn(self.driver, self.car.drivers.all())

        # Unassign driver
        res = self.client.get(toggle_url)
        self.assertEqual(res.status_code, 302)
        self.assertNotIn(self.driver, self.car.drivers.all())

    def test_driver_list_view(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "taxi/driver_list.html")
        self.assertIn("driver_list", res.context)
        self.assertEqual(list(res.context["driver_list"]), [self.driver])

    def test_driver_detail_view(self):
        detail_url = reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.driver.pk},
        )
        res = self.client.get(detail_url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "taxi/driver_detail.html")
        self.assertEqual(res.context["driver"], self.driver)

    def test_driver_license_update_view(self):
        update_url = reverse(
            "taxi:driver-update",
            kwargs={"pk": self.driver.pk},
        )
        res = self.client.post(
            update_url,
            {"license_number": "NEW12345"},
        )
        self.assertEqual(res.status_code, 302)
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.license_number, "NEW12345")

    def test_driver_delete_view(self):
        delete_url = reverse(
            "taxi:driver-delete",
            kwargs={"pk": self.driver.pk},
        )
        res = self.client.post(delete_url)
        self.assertEqual(res.status_code, 302)
        self.assertFalse(
            get_user_model().objects.filter(pk=self.driver.pk).exists()
        )
