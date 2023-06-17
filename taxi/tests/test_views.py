from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm
from taxi.models import Manufacturer
from taxi.views import ManufacturerListView

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertNotEquals(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username="driver1",
            password="test12345",
            first_name="first_name1",
            last_name="last_name1",
            license_number="AAA12345"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="manufacturer1",
            country="country1",
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="manufacturer2",
            country="country2",
        )
        self.manufacturer3 = Manufacturer.objects.create(
            name="Another",
            country="Country3",
        )

    def test_retrieve_manufacturers_list(self):
        response = self.client.get(MANUFACTURERS_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEquals(response.status_code, 200)
        self.assertContains(response, self.manufacturer2.name)
        self.assertEquals(
            list(response.context_data["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html"
        )

    def test_search_box_filter_by_name_manufacturers_list(self):
        manufacturer1 = Manufacturer.objects.create(
            name="Skoda",
            country="Country1"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Skoda two",
            country="Country2"
        )
        manufacturer3 = Manufacturer.objects.create(
            name="Citroen",
            country="Country3"
        )
        response = self.client.get(MANUFACTURERS_URL, {"name": "Sko"})
        manufacturers = Manufacturer.objects.filter(name__icontains="Sko")
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, manufacturer1.name)
        self.assertContains(response, manufacturer2.name)
        self.assertNotContains(response, manufacturer3.name)
        self.assertEqual(len(response.context_data["manufacturer_list"]), 2)
        self.assertEqual(
            list(response.context_data["manufacturer_list"]),
            list(manufacturers)
        )

    def test_get_queryset_without_search(self):
        # Create a request instance
        request = self.factory.get(reverse("taxi:manufacturer-list"))

        # Create the view instance
        view = ManufacturerListView()
        view.setup(request)

        # Get the queryset using the get_queryset method
        queryset = view.get_queryset()

        # Assert that all manufacturers are included in the queryset
        self.assertQuerysetEqual(queryset, Manufacturer.objects.all())

    def test_get_queryset_with_search(self):
        # Create a request instance with search parameter
        request = self.factory.get(
            reverse("taxi:manufacturer-list"),
            data={"name": "manufacturer"}
        )

        # Create the view instance
        view = ManufacturerListView()
        view.setup(request)

        # Get the queryset using the get_queryset method
        queryset = view.get_queryset()

        # Assert that only manufacturers with name containing "Manufacturer"
        # are included in the queryset
        expected_queryset = Manufacturer.objects.filter(
            name__icontains="manufacturer"
        )
        self.assertQuerysetEqual(
            queryset,
            expected_queryset,
            transform=lambda x: x
        )


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123456",
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "driver_test",
            "password1": "test1234567",
            "password2": "test1234567",
            "first_name": "first_name3",
            "last_name": "last_name3",
            "license_number": "DDD52345",
        }

        url = reverse("taxi:driver-create")
        self.client.post(
            path=url,
            data=form_data,
        )
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
