from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse


class MockException(Exception):
    pass


class PostOrderTests(APITestCase):
    '''Post order service tests
    '''
    fixtures = ['post_order/fixtures/testfixture.json']

    def setUp(self) -> None:
        User.objects.create_user(username='test', password='test')
        is_auth = self.client.login(username='test', password='test')
        self.assertEqual(is_auth, True, 'authorization failed')

    def test_create_client(self):
        '''Create client'''
        response = self.client.post(
            reverse('api:client-list'),
            {
                'id': 1,
                'phone_number': '79199888888',
                'mobile_code': 900,
                'tag': 'pomidor',
                'timezone': 'Europe/Moscow'
            },
            format='json'
        )
        self.assertEqual(
            response.status_code, 201, 
            'Error on client creation'
        )

    def test_list_post_orders(self):
        '''Check client receiving list'''
        response = self.client.get(
            reverse('api:client-list'), 
            format='json'
        )
        self.assertEqual(
            response.status_code, 200, 
            'Error on retriving list of clients'
        )
        response_data = response.data
        self.assertTrue(
            len(response_data['results']) > 0, 
            'Error on retriving list of clients'
        )

    def test_list_post_orders(self):
        '''Check all post order list receiving'''
        response = self.client.get(
            reverse('api:post_order-list'), 
            format='json'
        )
        self.assertEqual(
            response.status_code, 200, 
            'Error on retriving list of post orders'
        )
        response_data = response.data
        self.assertTrue(
            len(response_data['results']) > 0, 
            'Error on retriving list of post orders'
        )

