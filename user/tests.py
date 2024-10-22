from django.test import TestCase
from rest_framework import status
from .models import Follower, User


class BaseTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.api = self.client
        self.client = None


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

        response = self.api.post(path="/api/user/", data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)

        result_data = response.data
        del result_data["id"]
        expect_data = data
        del expect_data["password"]
        self.assertDictEqual(result_data, expect_data)

    def test_create_2(self):
        """
        Dado:
          - um payload com username inválido para cadastro de um usuário
        Quando:
          - for feita a requisição de criação de um usuário
            `POST /api/user/`
        Então:
          - o status da resposta deve ser HTTP_400_BAD_REQUEST
        """
        # TODO: why the UnicodeUsernameValidator is not working? If username=" Foo  Barr" it is not failing
        data = dict(
            username="",
            email="foo@bar.com",
            name="Foo",
            password="1",
        )

        response = self.api.post(path="/api/user/", data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_3(self):
        """
        Dado:
          - um payload sem email para cadastro de um usuário
        Quando:
          - for feita a requisição de criação de um usuário
            `POST /api/user/`
        Então:
          - o status da resposta deve ser HTTP_400_BAD_REQUEST
        """
        data = dict(
            username="foobar",
            name="Foo",
            password="1",
        )

        response = self.api.post(path="/api/user/", data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_4(self):
        """
        Dado:
          - um payload sem password para cadastro de um usuário
        Quando:
          - for feita a requisição de criação de um usuário
            `POST /api/user/`
        Então:
          - o status da resposta deve ser HTTP_400_BAD_REQUEST
        """
        data = dict(
            username="foobar",
            name="Foo",
            email="foo@bar.com",
        )

        response = self.api.post(path="/api/user/", data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_follow_1(self):
        """
        Dado:
          - dois usuários cadastrados em um segue o outro
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

        user1 = User.objects.create(**data1)
        user2 = User.objects.create(**data2)

        Follower.objects.create(following=user1, follower=user2)

        response = self.api.get(path=f"/api/user/{user1.id}/followers/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result_data = response.data
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
