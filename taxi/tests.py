from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

"""
testing code for the IndexView    
"""


class PrivateHomePageTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(username="test", password="12234")
        self.client.force_login(user)
        self.res = self.client.get(reverse("taxi:index"))

    def test_PrivateHomePage_test(self):
        self.assertEquals(self.res.status_code, 200)


class PublicHomePageTest(TestCase):
    def setUp(self):
        self.res = self.client.get(reverse("taxi:index"))

    def test_PublicHomePage(self):
        self.assertNotEquals(self.res.status_code, 200)


class IndexViewTest(TestCase):
    def setUp(self):
        driver_test = get_user_model().objects.create_user(
            username="Anton", password="tiguti26", license_number="NO55555"
        )

        manufacturer_test = Manufacturer.objects.create(
            name="test_Manufacturer", country="test_Country"
        )
        self.car = Car.objects.create(
            model="test_Model",
            manufacturer=manufacturer_test,
        )
        self.car.drivers.add(driver_test)
        self.client.force_login(driver_test)
        self.response = self.client.get(reverse("taxi:index"))

    def test_home_page_count(self):
        num_test = ["num_drivers", "num_cars", "num_manufacturers", "num_visits"]
        for data in num_test:
            self.assertTemplateUsed(self.response, "taxi/index.html")
            self.assertIn(data, self.response.context, f"key must be equal to {data}")
            self.assertGreaterEqual(
                self.response.context[data], 1, "count must be greater or equal 1"
            )


"""
     testing code for Manufacturer view    
"""
MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class TestManufacturerListView(TestCase):
    def setUp(self):
        pass


class PublicManufacturerPageTest(TestCase):
    def setUp(self):
        self.res = self.client.get(reverse("taxi:manufacturer-list"))

    def test_retrieve_login_manufacturer(self):
        self.assertNotEquals(self.res.status_code, 200)


class PrivateManufacturerPageTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(username="test", password="12234")
        manufacturer = Manufacturer.objects.create(
            name="test_Manufacturer", country="test_Country"
        )
        manufacturer1 = Manufacturer.objects.create(
            name="test_Manufacturer1", country="test_Country1"
        )
        self.client.force_login(user)
        self.res = self.client.get(reverse("taxi:manufacturer-list"))

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="test1_manufacturer", country="test1_country")
        Manufacturer.objects.create(name="test2_manufacturer", country="test1_country")
        self.assertEquals(self.client.get(MANUFACTURER_URL).status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEquals(
            list(self.client.get(MANUFACTURER_URL).context["manufacturer_list"]),
            list(manufacturers),
        )


class Manufacturers_Search_Context_Test(TestCase):
    def setUp(self):
        self.response = self.client.get(MANUFACTURER_URL)
        Manufacturer.objects.create(
            name="test_Manufacturer", country="test_Country"
        )
        Manufacturer.objects.create(
            name="test_Manufacturer1", country="test_Country1"
        )

    def test_check_valid_search_context(self):
        print(self.response.context)
        self.assertIn("search_form", self.response.context)

    def test_search_queryset(self):
        custom_query_set = self.response.context["search_form"]

        # self.assertTemplateUsed(
        #     self.client.get(
        #         MANUFACTURER_URL),
        #     "taxi/manufacturer_list.html"
        # )
