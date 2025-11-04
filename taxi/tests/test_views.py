from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car
from taxi.views import ManufacturerListView


class ViewTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="TestDriver", password="TestPass1234"
        )
        self.client.force_login(self.driver)

    def test_login_required(self):
        self.client.logout()
        url = reverse("taxi:index")
        response = self.client.get(url, follow=True)
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertContains(response, "Please login")

    def test_manufacturer_search_by_name(self):
        mn_one = Manufacturer.objects.create(name="TEST116", country="3321")
        mn_two = Manufacturer.objects.create(name="TEST117", country="1158")
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, data={"searched_name": mn_one.name})
        self.assertContains(response, mn_one.name)
        self.assertContains(response, mn_one.country)
        self.assertNotContains(response, mn_two.name)
        self.assertNotContains(response, mn_two.country)

    def test_manufacturer_create(self):
        url = reverse("taxi:manufacturer-create")
        response = self.client.post(
            url, data={"name": "889988", "country": "3321"}, follow=True
        )
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.assertContains(response, "889988")

    def test_manufacturer_update(self):
        mn = Manufacturer.objects.create(name="TEST116", country="3321")
        url = reverse("taxi:manufacturer-update", kwargs={"pk": mn.pk})
        response = self.client.post(url, data={"name": "TEST117"}, follow=True)
        self.assertContains(response, "TEST117")
        self.assertNotContains(response, "TEST116")

    def test_manufacturer_delete(self):
        mn = Manufacturer.objects.create(name="TEST116", country="3321")
        url = reverse("taxi:manufacturer-delete", kwargs={"pk": mn.pk})
        response = self.client.post(url, follow=True)
        self.assertNotContains(response, "TEST117")
        self.assertNotContains(response, "3321")

    def test_car_toggle_driver_on(self):
        mn = Manufacturer.objects.create(name="TEST116", country="3321")
        car = Car.objects.create(manufacturer=mn, model="TEST1133")
        url = reverse("taxi:toggle-car-assign", kwargs={"pk": car.pk})
        self.client.post(url)
        self.assertEqual(list(car.drivers.all()), [self.driver])

    def test_car_toggle_driver_off(self):
        mn = Manufacturer.objects.create(name="TEST116", country="3321")
        car = Car.objects.create(manufacturer=mn, model="TEST1133")
        car.drivers.add(self.driver)
        url = reverse("taxi:toggle-car-assign", kwargs={"pk": car.pk})
        self.client.post(url)
        self.assertEqual(list(car.drivers.all()), [])

    def test_manufacturer_list_pagination(self):
        paginate_by = ManufacturerListView.paginate_by
        Manufacturer.objects.bulk_create(
            [
                Manufacturer(name=f"TEST{i}", country=f"TT{i}")
                for i in range(paginate_by * 4)
            ]
        )
        Manufacturer.objects.create(name="ZZZZ", country="3321")
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, data={"page": "5"})
        self.assertContains(response, "ZZZZ")
        self.assertFalse(response.context["page_obj"].has_next())
        self.assertTrue(response.context["page_obj"].has_previous())
