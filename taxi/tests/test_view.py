from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

URLS_DB = {
    "MANUFACTURER_LIST": "taxi:manufacturer-list",
    "CAR_LIST": "taxi:car-list",
    "DRIVER_LIST": "taxi:driver-list",
    "HOME_PAGE": "taxi:index"
}


class PublicAcsessTest(TestCase):
    def test_login_required(self):
        """
        Test that all required pages request authorization,
        if not return list of pages that need to be protected.
        """
        out = []
        for key, value in URLS_DB.items():
            url = reverse(value)
            response = self.client.get(url)
            if response.status_code == 200:
                out.append(key)
        self.assertFalse(
            out,
            f"Acsess to {out} must be denied for unauthorized users"
        )


class PrivateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="test566",
            password="test1234",
        )

        driver1 = Driver.objects.create(
            username="test111",
            password="111test",
            license_number="HHH12345"
        )
        driver2 = Driver.objects.create(
            username="test222",
            password="222test",
            license_number="GGG54321"
        )
        manufacturer1 = Manufacturer.objects.create(
            name="test1",
            country="testcountry1"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="test2",
            country="testcountry2"
        )

        car1 = Car.objects.create(model="testmodel1",
                                  manufacturer=manufacturer1)
        car2 = Car.objects.create(model="testmodel2",
                                  manufacturer=manufacturer2)
        car1.drivers.add(driver1)
        car2.drivers.add(driver2)

    def setUp(self):
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        response = self.client.get(reverse(URLS_DB["MANUFACTURER_LIST"]))
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturer_by_name(self):
        search_name = "t"
        response = self.client.get(
            reverse(URLS_DB["MANUFACTURER_LIST"]),
            {"name": search_name})
        self.assertEqual(response.status_code, 200)
        context = Manufacturer.objects.filter(
            name__icontains=search_name
        )
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(context)
        )

    def test_retrieve_cars(self):
        response = self.client.get(reverse(URLS_DB["CAR_LIST"]))
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_drivers(self):
        response = self.client.get(reverse(URLS_DB["DRIVER_LIST"]))
        self.assertEqual(response.status_code, 200)
        cars = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
