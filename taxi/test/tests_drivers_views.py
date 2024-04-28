from django.contrib.auth import get_user_model
from django.db.models import Q
from django.test import TestCase, RequestFactory
from django.urls import reverse
from taxi.models import Driver
from taxi.views import DriverDetailView


class PrivateManufactureViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

        Driver.objects.create(
            username="namewith_i",
            first_name="Fordi",
            last_name="Harg",
            license_number="1234"
        )
        Driver.objects.create(
            username="namewith_i1",
            first_name="Ford",
            last_name="Hargi",
            license_number="1235"
        )
        Driver.objects.create(
            username="namewith_i2",
            first_name="Ford",
            last_name="Harg",
            license_number="1236"
        )
        Driver.objects.create(
            username="namewith_i3",
            first_name="Fordi",
            last_name="Hargi",
            license_number="1237"
        )

    def test_drivers_list_search(self):

        response = self.client.get(reverse("taxi:driver-list"),
                                   {"driver_name": "i"})
        self.assertEqual(
            list(response.context_data["driver_list"]),
            list(Driver.objects.filter(Q(first_name__icontains="i")
                 | Q(last_name__icontains="i"))
                 )
        )

    def test_driver_queryset_detail_view(self):
        request = RequestFactory().get("taxi:driver-detail")
        view = DriverDetailView()
        view.request = request
        qeryset = view.get_queryset()
        self.assertQuerysetEqual(
            qeryset,
            get_user_model().objects.prefetch_related("cars__drivers")
        )

    def test_driver_delete_get_succses_redirect(self):
        path = reverse("taxi:driver-delete", args=["5"])
        response = self.client.post(path=path)
        self.assertRedirects(response, reverse("taxi:driver-list"))
