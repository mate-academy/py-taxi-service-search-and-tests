from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer
from taxi.views import CarListView, DriverListView


class ViewTests(TestCase):
    def test_paginate_car_view(self):
        self.assertEqual(CarListView.paginate_by, 5)

    def test_paginate_driver_view(self):
        self.assertEqual(DriverListView.paginate_by, 5)

    def test_retrieve_manufactures(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

        Manufacturer.objects.create(name="test1", country="UK")
        Manufacturer.objects.create(name="test2", country="UK")

        res = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(res.status_code, 200)

        manufactures = Manufacturer.objects.all()
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufactures)
        )

        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")
