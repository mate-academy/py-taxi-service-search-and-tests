from http.client import responses
from urllib.parse import urlencode

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerListViewTest(TestCase):
    def test_public_access_to_manufacturer_list(self):
        Manufacturer.objects.create(name="test1", country="test1")
        Manufacturer.objects.create(name="test2", country="test2")

        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEquals(response.status_code, 200)


class PrivateManufacturerListViewTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create(
            username="test_name",
            password="password_test12345"
        )
        self.client.force_login(user)

    def test_private_access_to_manufacturer_list(self):
        Manufacturer.objects.create(name="test1", country="test1")
        Manufacturer.objects.create(name="test2", country="test2")

        manufacturers = Manufacturer.objects.all()
        response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class SearchTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create(
            username="test_name",
            password="test_password12345"
        )
        self.client.force_login(user)

    def test_filter_for_manufacturer_list(self):
        Manufacturer.objects.create(name="name1", country="test1")
        Manufacturer.objects.create(name="name2", country="test2")
        Manufacturer.objects.create(name="name3", country="test3")
        query_params = {"name": "name1"}

        full_url = f"{MANUFACTURER_LIST_URL}?{urlencode(query_params)}"
        response = self.client.get(full_url)
        self.assertEquals(
            list(Manufacturer.objects.filter(name="name1")),
            list(response.context["manufacturer_list"])
        )

    def test_filter_for_drivers_list(self):
        get_user_model().objects.create(
            username="user1",
            password="password12345",
            license_number="ABC12345"
        )
        get_user_model().objects.create(
            username="user2",
            password="password12345",
            license_number="ABD12345"
        )
        get_user_model().objects.create(
            username="user3",
            password="password12345",
            license_number="ABF12345"
        )
        full_url = (
            f""
            f"{reverse('taxi:driver-list')}"
            f"?{urlencode({'username':'u'})}"
        )
        response = self.client.get(full_url)

        self.assertEquals(
            list(get_user_model().objects.filter(username__icontains="u")),
            list(response.context["driver_list"])
        )

    def test_filter_for_cars_list(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW", country="Germany"
        )
        Car.objects.create(model="model1", manufacturer=manufacturer)
        Car.objects.create(model="model2", manufacturer=manufacturer)
        Car.objects.create(model="volvo", manufacturer=manufacturer)

        full_url = (
            f""
            f"{reverse('taxi:car-list')}"
            f"?{urlencode({'model': 'model'})}"
        )
        response_with_filter = self.client.get(full_url)

        self.assertEquals(
            list(Car.objects.filter(model__icontains="model")),
            list(response_with_filter.context["car_list"])
        )

        response_without_filter = self.client.get(reverse("taxi:car-list"))
        self.assertEquals(
            list(Car.objects.all()),
            list(response_without_filter.context["car_list"])
        )
