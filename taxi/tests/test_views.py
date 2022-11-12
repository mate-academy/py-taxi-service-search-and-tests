from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.test import TestCase

from django.urls import reverse

from taxi.forms import SearchForm
from taxi.models import Manufacturer, Driver, Car


class TestAccessViews(TestCase):
    def test_login_required(self):
        urls = [
            reverse("taxi:driver-list"),
            reverse("taxi:car-list"),
            reverse("taxi:manufacturer-list"),
            reverse("taxi:index")
        ]
        for url in urls:
            with self.subTest(url=url):
                resp = self.client.get(url)
                self.assertNotEqual(resp.status_code, 200)


class TestSearchViews(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="random",
            password="random",
            license_number="AAA12345"
        )
        self.client.force_login(self.user)


    def create_manufacturers(self):
        manufacturer1 = Manufacturer.objects.create(name="manufacturer1", country="country1")
        manufacturer2 = Manufacturer.objects.create(name="manufacturer2", country="country2")
        return manufacturer1, manufacturer2
    def test_manufacturer_search(self):
        self.create_manufacturers()
        resp = self.client.get("/manufacturers/?title=manufacturer2")
        print(resp.context["manufacturer_list"])
        self.assertQuerysetEqual(
            resp.context["manufacturer_list"],
            Manufacturer.objects.filter(name__icontains="manufacturer2")
        )

    def test_driver_search(self):
        get_user_model().objects.create_user(
            username="username1",
            password="random",
            license_number="AAA11111"
        )
        get_user_model().objects.create_user(
            username="username2",
            password="random",
            license_number="AAA22222"
        )
        resp = self.client.get("/drivers/?title=username2")
        self.assertEqual(
            list(resp.context["driver_list"]),
            list(Driver.objects.filter(username__icontains="username2"))
        )

    def test_car_search(self):
        manufacturer1, manufacturer2 = self.create_manufacturers()
        Car.objects.create(model="car1", manufacturer=manufacturer1)
        Car.objects.create(model="car2", manufacturer=manufacturer2)
        resp = self.client.get("/cars/?title=car1")
        self.assertQuerysetEqual(
            resp.context["car_list"],
            Car.objects.filter(model__icontains="car1")
        )
