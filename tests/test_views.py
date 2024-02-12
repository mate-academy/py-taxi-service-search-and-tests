import django.urls
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car
from taxi.urls import urlpatterns


def extract_urls(url_list: list[django.urls.path]) -> list[str]:
    extracted_urls = []
    for url in url_list:
        url_name = url.name
        if not url_name:
            continue
        if "<int:pk>" in url.pattern._route:
            url = reverse(f"taxi:{url_name}", kwargs={"pk": 1})
        else:
            url = reverse(f"taxi:{url_name}")
        extracted_urls.append(url)
    return extracted_urls


class PublicViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_views_accessible_when_logged(self):
        for url in extract_urls(urlpatterns):
            request = self.client.get(url)
            self.assertEqual(request.status_code, 302)


class LoginMixin(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="test",
            password="test123",
            license_number="TST12345"
        )
        self.client.force_login(self.user)


class CarListViewTest(LoginMixin):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse("taxi:car-list")
        self.template = "taxi/car_list.html"

        manufacturer1 = Manufacturer.objects.create(name="test1", country="TestCountry1")
        manufacturer2 = Manufacturer.objects.create(name="test2", country="TestCountry2")
        car1 = Car.objects.create(
            model="test1",
            manufacturer=manufacturer1,
        )
        car1.drivers.add(self.user)
        car2 = Car.objects.create(
            model="test2",
            manufacturer=manufacturer2,
        )
        car2.drivers.add(self.user)
        car3 = Car.objects.create(
            model="exclude_value_1",
            manufacturer=manufacturer2,
        )
        car3.drivers.add(self.user)

    def test_get_queryset_without_filtering(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        cars = Car.objects.select_related("manufacturer")
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars),
            "Data is partly passed to template"
        )
        self.assertTemplateUsed(response, self.template)

    def test_get_queryset_with_filtering(self):
        cars = Car.objects.filter(model__icontains="test")
        response = self.client.get(self.url, {"model": "test"})
        self.assertEqual(list(response.context["car_list"]),
                         list(cars),
                         "filtering works improperly")

    def test_get_context(self):
        response = self.client.get(self.url, {"model": "test"})
        self.assertIn("search_form", response.context)

        response = self.client.get(self.url)
        self.assertIn("search_form", response.context)


class ManufacturerListViewTest(LoginMixin):

    def setUp(self) -> None:
        super().setUp()
        self.url = reverse("taxi:manufacturer-list")
        self.template = "taxi/manufacturer_list.html"

        Manufacturer.objects.create(name="test1", country="TestCountry1")
        Manufacturer.objects.create(name="test2", country="TestCountry2")
        Manufacturer.objects.create(name="exclude_value_1", country="TestCountry3")

    def test_get_queryset_without_filtering(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
            "Data is partly passed to template"
        )

        self.assertTemplateUsed(response, self.template)

    def test_get_queryset_with_filtering(self):
        manufacturers = Manufacturer.objects.filter(name__icontains="test")
        response = self.client.get(self.url, {"name": "test"})
        self.assertEqual(list(response.context["manufacturer_list"]),
                         list(manufacturers),
                         "filtering works improperly")

    def test_get_context(self):
        response = self.client.get(self.url, {"name": "t"})
        self.assertIn("search_form", response.context)

        response = self.client.get(self.url)
        self.assertIn("search_form", response.context)


class ToggleAssignTest(LoginMixin):
    def setUp(self) -> None:
        super().setUp()
        self.template = "taxi/car-detail"
        self.url = reverse("taxi:toggle-car-assign", kwargs={"pk": self.user.pk})

        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test"
        )
        self.car1 = Car.objects.create(
            model="test1",
            manufacturer=manufacturer
        )
        self.car1.drivers.add(self.user)

    def test_if_exists(self):
        self.client.post(self.url)
        self.assertNotIn(self.car1, self.user.cars.all())

        self.client.post(self.url)

        self.assertIn(self.car1, self.user.cars.all())


