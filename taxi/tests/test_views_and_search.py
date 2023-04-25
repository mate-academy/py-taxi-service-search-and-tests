from django.test import TestCase, Client
from django.urls import reverse
from mixer.backend.django import mixer
from taxi.models import Manufacturer, Driver


class ManufacturerListViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('taxi:manufacturer-list')
        self.user = Driver.objects.create_user(username='testuser', password='testpass')
        self.manufacturer1 = mixer.blend(Manufacturer, name='Manufacturer1')
        self.manufacturer2 = mixer.blend(Manufacturer, name='Manufacturer2')
        self.manufacturer3 = mixer.blend(Manufacturer, name='Another')
        self.client.force_login(self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('taxi:manufacturer-list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'taxi/manufacturer_list.html')

    def test_view_paginates_by_five(self):
        response = self.client.get(self.url)
        self.assertTrue('paginator' in response.context)
        self.assertTrue(response.context['paginator'].per_page == 5)

    def test_view_returns_all_manufacturers(self):
        response = self.client.get(self.url)
        manufacturers = response.context['manufacturer_list']
        self.assertTrue(len(manufacturers) == 3)

    def test_view_filters_manufacturers_by_name(self):
        response = self.client.get(self.url, {'query-manufacturer': 'Manufacturer'})
        manufacturers = response.context['manufacturer_list']
        self.assertEqual(len(manufacturers), 2)
        self.assertTrue(self.manufacturer1 in manufacturers)
        self.assertTrue(self.manufacturer2 in manufacturers)

    def test_view_returns_empty_queryset_if_no_matching_results(self):
        response = self.client.get(self.url, {'query-manufacturer': 'Non-existent manufacturer'})
        manufacturers = response.context['manufacturer_list']
        self.assertTrue(len(manufacturers) == 0)

    def test_view_redirects_to_login_if_user_not_authenticated(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, '/accounts/login/?next=' + self.url)
