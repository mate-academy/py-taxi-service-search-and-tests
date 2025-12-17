from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Driver, Car

User = get_user_model()


class ViewsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="driver1",
                                             password="password123",
                                             license_number="ABC12345"
                                             )
        self.client.login(username="driver1", password="password123")

        self.manufacturer = Manufacturer.objects.create(name="Toyota",
                                                        country="Japan"
                                                        )
        self.car = Car.objects.create(model="Corolla",
                                      manufacturer=self.manufacturer
                                      )
        self.driver2 = User.objects.create_user(username="driver2",
                                                password="password123",
                                                license_number="DEF67890"
                                                )
        self.car.drivers.add(self.user)

    def test_manufacturer_list_view(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.manufacturer.name)

    def test_car_list_view(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car.model)

    def test_driver_list_view(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_toggle_assign_to_car_add_remove(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car.id])
        response = self.client.get(url)
        self.assertRedirects(response, reverse("taxi:car-detail",
                                               args=[self.car.id]))
        self.assertNotIn(self.user, self.car.drivers.all())

        response = self.client.get(url)
        self.assertRedirects(response, reverse("taxi:car-detail",
                                               args=[self.car.id]))
        self.assertIn(self.user, self.car.drivers.all())

    def test_manufacturer_create_view(self):
        url = reverse("taxi:manufacturer-create")
        response = self.client.post(url, {"name": "Honda",
                                          "country": "Japan"}
                                    )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Manufacturer.objects.filter(name="Honda").exists())

    def test_car_create_view(self):
        url = reverse("taxi:car-create")
        response = self.client.post(url, {
            "model": "Civic",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.user.id],
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Car.objects.filter(model="Civic").exists())

    def test_car_search_view(self):
        url = reverse("taxi:car-list") + "?model=Corolla"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car.model)
        Car.objects.create(model="Civic",
                           manufacturer=self.manufacturer
                           )
        response = self.client.get(url)
        self.assertNotContains(response, "Civic")

    def test_driver_search_view(self):
        url = reverse("taxi:driver-list") + "?username=driver1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
        self.assertNotContains(response, self.driver2.username)

    def test_car_pagination_with_search(self):
        for i in range(6):
            Car.objects.create(model=f"Car{i}",
                               manufacturer=self.manufacturer
                               )
        url = reverse("taxi:car-list") + "?model=Car"
        response = self.client.get(url)
        self.assertContains(response, "Car0")
        self.assertContains(response, "Car4")
        response = self.client.get(url + "&page=2")
        self.assertContains(response, "Car5")
