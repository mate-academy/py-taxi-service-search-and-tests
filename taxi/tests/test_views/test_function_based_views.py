from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


INDEX_URL = reverse("taxi:index")
TOGGLE_ASSIGN_URL = reverse("taxi:toggle-car-assign", args=[2])


class PublicViewsTest(TestCase):
    def test_login_required_protection_index(self):
        url = INDEX_URL
        res = self.client.get(url)
        self.assertNotEquals(res.status_code, 200)

    def test_login_required_protection_toggle_assign_to_car(self):
        url = TOGGLE_ASSIGN_URL
        res = self.client.get(url)
        self.assertNotEquals(res.status_code, 200)


class PrivateViewsTest(TestCase):
    fixtures = ["taxi_service_db_data.json"]

    def setUp(self):
        self.user = get_user_model().objects.get(id=2)
        self.client.force_login(self.user)

    def test_home_page_info(self):
        url = INDEX_URL
        res = self.client.get(url)
        self.assertEquals(res.context["num_cars"], Car.objects.all().count())
        self.assertEquals(
            res.context["num_drivers"], Driver.objects.all().count()
        )
        self.assertEquals(
            res.context["num_manufacturers"],
            Manufacturer.objects.all().count(),
        )
        self.assertEquals(res.context["num_visits"], 1)
        self.assertTemplateUsed(res, "taxi/index.html")

    def test_toggle_assign_works_correctly(self):
        car = Car.objects.create(
            model="test_car", manufacturer=Manufacturer.objects.first()
        )
        self.client.get(reverse("taxi:toggle-car-assign", args=[car.id]))
        self.assertTrue(self.user in car.drivers.all())

        self.client.get(reverse("taxi:toggle-car-assign", args=[car.id]))
        self.assertFalse(self.user in car.drivers.all())
