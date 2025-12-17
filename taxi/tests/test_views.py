from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car

User = get_user_model()


class ViewsTestCase(TestCase):

    def setUp(self):
        self.driver1 = User.objects.create_user(
            username="driver1",
            password="password123",
            license_number="ABC12345"
        )
        self.driver2 = User.objects.create_user(
            username="driver2",
            password="password123",
            license_number="DEF67890"
        )
        self.client.login(username="driver1", password="password123")

        self.toyota = Manufacturer.objects.create(name="Toyota",
                                                  country="Japan"
                                                  )
        self.honda = Manufacturer.objects.create(name="Honda",
                                                 country="Japan"
                                                 )

        self.corolla = Car.objects.create(model="Corolla",
                                          manufacturer=self.toyota
                                          )
        self.civic = Car.objects.create(model="Civic",
                                        manufacturer=self.honda
                                        )
        self.corolla.drivers.add(self.driver1)
        self.civic.drivers.add(self.driver2)

    def test_manufacturer_list_view(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.toyota.name)

    def test_car_list_view(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.corolla.model)

    def test_driver_list_view(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver1.username)

    def test_toggle_assign_to_car(self):
        url = reverse("taxi:toggle-car-assign",
                      args=[self.corolla.id])
        response = self.client.get(url)
        self.assertRedirects(response, reverse(
            "taxi:car-detail",
            args=[self.corolla.id]))
        self.assertNotIn(self.driver1, self.corolla.drivers.all())

        response = self.client.get(url)
        self.assertRedirects(response, reverse(
            "taxi:car-detail",
            args=[self.corolla.id]))
        self.assertIn(self.driver1, self.corolla.drivers.all())

    def test_car_create_view(self):
        url = reverse("taxi:car-create")
        response = self.client.post(url, {
            "model": "Accord",
            "manufacturer": self.honda.id,
            "drivers": [self.driver1.id],
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Car.objects.filter(model="Accord").exists())

    def test_car_search_view(self):
        url = reverse("taxi:car-list") + "?model=Corolla"
        response = self.client.get(url)
        self.assertContains(response, self.corolla.model)
        self.assertNotContains(response, self.civic.model)

    def test_driver_search_view(self):
        url = reverse("taxi:driver-list") + "?username=driver1"
        response = self.client.get(url)
        self.assertContains(response, self.driver1.username)
        self.assertNotContains(response, self.driver2.username)

    def test_car_pagination_with_search(self):
        for i in range(6):
            Car.objects.create(model=f"Car{i}", manufacturer=self.honda)
        url = reverse("taxi:car-list") + "?model=Car"
        response = self.client.get(url)
        self.assertContains(response, "Car0")
        self.assertContains(response, "Car4")
        response = self.client.get(url + "&page=2")
        self.assertContains(response, "Car5")

    def test_manufacturer_search_view(self):
        url = reverse("taxi:manufacturer-list") + "?name=Toy"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Honda")
