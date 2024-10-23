from django.test import TestCase
from rest_framework import status
from .models import User, Follower


from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager
from django.urls import reverse


class BaseTestCase(TestCase):
    def setUp(self):
        super().setUp()


class AuthTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_obtain_token(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpass'
        }

        self.assertEqual(1, User.objects.count())
        self.assertEqual(self.user, User.objects.get())
        self.assertEqual(url, '/api/token/')
        self.assertTrue(self.user.is_active)

        self.client.login(username='testuser', password='testpass')
        self.client.force_login(self.user)
        self.client.force_authenticate(self.user)
        response = self.client.post('/api/token/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_refresh_token(self):
        # First, obtain a token
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpass'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        refresh = response.data['refresh']

        # Now, refresh the token
        refresh_url = reverse('token_refresh')
        response = self.client.post(refresh_url, {'refresh': refresh}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_obtain_token_invalid_credentials(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token_invalid(self):
        url = reverse('token_refresh')
        response = self.client.post(url, {'refresh': 'invalidtoken'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserViewSetTestCase(BaseTestCase):
    def test_create_1(self):
        """
        Dado:
          - um payload com dados válidos para cadastro de um usuário
        Quando:
          - for feita a requisição de criação de um usuário
            `POST /api/user/`
        Então:
          - o status da resposta deve ser HTTP_201_CREATED
          - id do usuário deve está na resposta
          - a resposta não deve conter a senha
          - os demais campos devem ser iguais aos dados enviados
        """
        data = dict(
            username="foobar",
            email="foo@bar.com",
            name="Foo",
            password="123",
        )

        response = self.client.post(path="/api/user/", data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertIn("id", response.data)

        # result_data = response.data
        # del result_data["id"]
        # expect_data = data
        # del expect_data["password"]
        # self.assertDictEqual(result_data, expect_data)

#     def test_create_2(self):
#         """
#         Dado:
#           - um payload com username inválido para cadastro de um usuário
#         Quando:
#           - for feita a requisição de criação de um usuário
#             `POST /api/user/`
#         Então:
#           - o status da resposta deve ser HTTP_400_BAD_REQUEST
#         """
#         # TODO: why the UnicodeUsernameValidator is not working? If username=" Foo  Barr" it is not failing
#         data = dict(
#             username="",
#             email="foo@bar.com",
#             name="Foo",
#             password="1",
#         )
#
#         response = self.api.post(path="/api/user/", data=data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_create_3(self):
#         """
#         Dado:
#           - um payload sem email para cadastro de um usuário
#         Quando:
#           - for feita a requisição de criação de um usuário
#             `POST /api/user/`
#         Então:
#           - o status da resposta deve ser HTTP_400_BAD_REQUEST
#         """
#         data = dict(
#             username="foobar",
#             name="Foo",
#             password="1",
#         )
#
#         response = self.api.post(path="/api/user/", data=data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_create_4(self):
#         """
#         Dado:
#           - um payload sem password para cadastro de um usuário
#         Quando:
#           - for feita a requisição de criação de um usuário
#             `POST /api/user/`
#         Então:
#           - o status da resposta deve ser HTTP_400_BAD_REQUEST
#         """
#         data = dict(
#             username="foobar",
#             name="Foo",
#             email="foo@bar.com",
#         )
#
#         response = self.api.post(path="/api/user/", data=data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_followers_1(self):
        """
        Dado:
          - dois usuários cadastrados e um segue o outro
        Quando
          - for feita a requisição de
            `/api/user/{user1.id}/followers/`
        Então:
          - o status da resposta deve ser HTTP_200_OK
        """
        data1 = dict(
            username="foobar1",
            email="foo@bar.com",
            name="Foo1",
            password="123",
        )
        data2 = dict(
            username="foobar2",
            email="foo@bar2.com",
            name="Foo2",
            password="123",
        )

        user1 = User.objects.create_user(**data1)
        user2 = User.objects.create_user(**data2)

        Follower.objects.create(following=user1, follower=user2)

        data = dict(
            username="foobar1",
            password="123",
        )

        response = self.client.post(path="/api/token/", data=data)
        auth = {
            "HTTP_AUTHORIZATION": f"Bearer {response.data['access']}",
        }

        response2 = self.client.get(path=f"/api/user/{user1.id}/followers/", **auth)
        self.assertEqual(response2.status_code, status.HTTP_200_OK, response2.data)

        result_data = response2.data
        for result in result_data["results"]:
            self.assertIn("id", result)
            del result["id"]

        expected_data = {
             "count": 1,
             'next': None,
             'previous': None,
             'results': [{'username': 'foobar2', 'name': 'Foo2'}],
        }
        self.assertDictEqual(result_data, expected_data)
