from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Driver, Car

INDEX_URL = reverse("taxi:index")


class TestIndexView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_driver",
            password="driver1234"
        )
        self.client.force_login(self.user)

    def test_public_permission(self):
        self.client.logout()
        resp = self.client.get(INDEX_URL)

        self.assertNotEqual(resp.status_code, 200)
        self.assertRedirects(resp, "/accounts/login/?next=/")

    def test_private_permission_used_template(self):
        resp = self.client.get(INDEX_URL)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "taxi/index.html")

    def test_driver_cars_manufacturer_count_listed(self):
        manuf = Manufacturer.objects.create(name="Test_manufacturer")
        driver = get_user_model().objects.get(id=1)
        car = Car.objects.create(model="test_model",
                                 manufacturer=manuf)
        car.drivers.add(driver)
        resp = self.client.get(INDEX_URL)

        self.assertEqual(resp.context["num_drivers"], len(get_user_model().objects.all()))
        self.assertEqual(resp.context["num_cars"], len(Car.objects.all()))
        self.assertEqual(resp.context["num_manufacturers"], len(Manufacturer.objects.all()))

    def test_num_visit_count(self):
        num_visit = 10
        for visit in range(num_visit):
            resp = self.client.get(INDEX_URL)

        self.assertEqual(resp.context["num_visits"], num_visit)
