from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class InvalidUserTests(TestCase):
    def test_login_required(self):
        def check_url(url, pk=None):
            if pk:
                res = self.client.get(reverse(url, kwargs={"pk": pk}))
            else:
                res = self.client.get(reverse(url))

            self.assertNotEqual(res.status_code, 200, url)

        check_url("taxi:manufacturer-list")
        check_url("taxi:manufacturer-create")
        check_url("taxi:manufacturer-update", pk=1)
        check_url("taxi:manufacturer-delete", pk=1)
        check_url("taxi:car-list")
        check_url("taxi:car-detail", pk=1)
        check_url("taxi:car-create")
        check_url("taxi:car-update", pk=1)
        check_url("taxi:car-delete", pk=1)
        check_url("taxi:driver-list")
        check_url("taxi:driver-detail", pk=1)
        check_url("taxi:driver-create")
        check_url("taxi:driver-update", pk=1)
        check_url("taxi:driver-delete", pk=1)


class ValidUserTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="text", password="test1234"
        )
        self.client.force_login(self.user)

    def test_logged_user(self):
        def check_url(url, pk=None):
            if pk:
                res = self.client.get(reverse(url, kwargs={"pk": pk}))
            else:
                res = self.client.get(reverse(url))

            self.assertEqual(res.status_code, 200, f"URL={url}")

        manufacturer = Manufacturer.objects.create(name="Test name")
        Car.objects.create(model="Test name", manufacturer=manufacturer)

        check_url("taxi:manufacturer-list")
        check_url("taxi:manufacturer-create")
        check_url("taxi:manufacturer-update", pk=1)
        check_url("taxi:manufacturer-delete", pk=1)
        check_url("taxi:car-list")
        check_url("taxi:car-detail", pk=1)
        check_url("taxi:car-create")
        check_url("taxi:car-update", pk=1)
        check_url("taxi:car-delete", pk=1)

    def test_template_names(self):
        def check_url(url, tpl=None):
            res = self.client.get(reverse(url))
            self.assertTemplateUsed(res, tpl, f"URL={url}, TPL={tpl}")

        check_url("taxi:manufacturer-list",
                  tpl="taxi/manufacturer_list.html")
        check_url("taxi:manufacturer-create",
                  tpl="taxi/manufacturer_form.html")
        check_url("taxi:car-list",
                  tpl="taxi/car_list.html")
        check_url("taxi:car-create",
                  tpl="taxi/car_form.html")
        check_url("taxi:driver-list",
                  tpl="taxi/driver_list.html")
        check_url("taxi:driver-create",
                  tpl="taxi/driver_form.html")


class SearchTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="text", password="test1234"
        )
        self.client.force_login(self.user)

        manufacturer = Manufacturer.objects.create(
            name="test name", country="test country")
        Car.objects.create(model="model name", manufacturer=manufacturer)
        Car.objects.create(model="another model", manufacturer=manufacturer)

    def test_with_search_text(self):
        search_text = "th"
        response = self.client.get(reverse("taxi:car-list"),
                                   data={"search": search_text})
        queryset = Car.objects.filter(model__icontains=search_text)

        self.assertEqual(response.context["search"], search_text)
        self.assertEqual(list(response.context["car_list"]), list(queryset))

    def test_without_search_text(self):
        response = self.client.get(reverse("taxi:car-list"))
        queryset = Car.objects.all()

        self.assertEqual(list(response.context["car_list"]), list(queryset))
