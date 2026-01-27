from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car, Driver


class BaseViewTest(TestCase):
    """Base class for creating shared data (user, car)"""

    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="test.user",
            password="password123",
            license_number="ABC12345"
        )
        self.client.login(username="test.user",
                          password="password123")
        self.manufacturer = Manufacturer.objects.create(
            name="Tesla", country="USA")
        self.car = Car.objects.create(
            model="Model S", manufacturer=self.manufacturer)


class IndexViewTest(BaseViewTest):
    def test_index_view_status_code(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")
        self.assertIn("num_cars", response.context)


class ManufacturerListViewTest(BaseViewTest):
    def test_manufacturer_list_view(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tesla")
        self.assertIn("manufacturer_list",
                      response.context)

    def test_manufacturer_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Tesla"})
        self.assertContains(response, "Tesla")
        response_empty = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Ford"})
        self.assertNotContains(response_empty, "Tesla")


class CarDetailViewTest(BaseViewTest):
    def test_car_detail_status_code(self):
        url = reverse("taxi:car-detail",
                      kwargs={"pk": self.car.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["car"], self.car)


class DriverDetailViewTest(BaseViewTest):
    def test_driver_detail_status_code(self):
        url = reverse("taxi:driver-detail",
                      kwargs={"pk": self.driver.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ToggleAssignToCarTest(BaseViewTest):
    def test_toggle_assign_to_car(self):
        url = reverse("taxi:toggle-car-assign",
                      kwargs={"pk": self.car.pk})

        response = self.client.post(url)
        self.assertRedirects(response,
                             reverse("taxi:car-detail",
                                     kwargs={"pk": self.car.pk}))
        self.assertIn(self.driver, self.car.drivers.all())

        self.client.post(url)
        self.assertNotIn(self.driver, self.car.drivers.all())


class ManufacturerCRUDTest(BaseViewTest):
    def test_manufacturer_create(self):
        url = reverse("taxi:manufacturer-create")
        data = {"name": "Toyota", "country": "Japan"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Manufacturer.objects.filter(
            name="Toyota").exists())

    def test_manufacturer_delete(self):
        url = reverse("taxi:manufacturer-delete",
                      kwargs={"pk": self.manufacturer.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Manufacturer.objects.filter(
            id=self.manufacturer.pk).exists())
