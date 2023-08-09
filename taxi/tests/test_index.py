from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car, Driver

INDEX_FORMATS_URL = reverse("taxi:index")


class PublicIndexFormatTests(TestCase):
    def test_login_requirement_index(self):
        res_list = self.client.get(INDEX_FORMATS_URL)

        self.assertNotEquals(res_list.status_code, 200)


class PrivateIndexFormatTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            password="qwe12345"
        )
        self.client.force_login(self.user)

        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        Car.objects.create(
            model="EQS",
            manufacturer=manufacturer
        )

    def test_retrieve_index(self):

        response = self.client.get(INDEX_FORMATS_URL)
        num_drivers = Driver.objects.count()
        num_cars = Car.objects.count()
        num_manufacturers = Manufacturer.objects.count()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context["num_drivers"], num_drivers)
        self.assertEquals(response.context["num_cars"], num_cars)
        self.assertEquals(
            response.context["num_manufacturers"],
            num_manufacturers
        )
        self.assertEquals(response.context["num_visits"], 1)
        self.assertTemplateUsed(response, "taxi/index.html")

    def test_view_url_index_exists_at_desired_location(self):
        response = self.client.get("")
        self.assertEquals(response.status_code, 200)
