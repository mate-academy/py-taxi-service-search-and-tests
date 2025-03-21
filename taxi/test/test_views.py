from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Manufacturer, Car


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            license_number="XYZ12345"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan")
        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer)

    def test_index_view(self):
        url = reverse("taxi:index")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "taxi/index.html")

        self.assertIn("num_drivers", res.context)
        self.assertIn("num_cars", res.context)
        self.assertIn("num_manufacturers", res.context)
        self.assertIn("num_visits", res.context)

        self.assertContains(res, str(res.context["num_drivers"]))
        self.assertContains(res, str(res.context["num_cars"]))
        self.assertContains(res, str(res.context["num_manufacturers"]))
        self.assertContains(res, str(res.context["num_visits"]))

    def test_manufacturer_list_view(self):
        url = reverse("taxi:manufacturer-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")
        self.assertContains(res, self.manufacturer.name)

    def test_car_list_view(self):
        url = reverse("taxi:car-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.car.model)

    def test_car_detail_view(self):
        url = reverse("taxi:car-detail", args=[self.car.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.car.model)

    def test_manufacturer_create_view(self):
        url = reverse("taxi:manufacturer-create")
        res = self.client.post(url, {"name": "Honda", "country": "Japan"})
        self.assertEqual(res.status_code, 302)
        self.assertTrue(Manufacturer.objects.filter(name="Honda").exists())

    def test_car_delete_view(self):
        url = reverse("taxi:car-delete", args=[self.car.id])
        res = self.client.post(url)
        self.assertEqual(res.status_code, 302)
        self.assertFalse(Car.objects.filter(id=self.car.id).exists())

    def test_toggle_assign_to_car(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car.id])
        res = self.client.post(url)
        self.assertEqual(res.status_code, 302)
        self.assertTrue(self.car.drivers.filter(id=self.user.id).exists())
