from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.user.models import User, Apprentice, Mentor, Trainer
import uuid
from rest_framework_simplejwt.tokens import RefreshToken


class UsersTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.trainer_user = User.objects.create_user(
            id=uuid.uuid4(),
            email="trainer@example.com",
            first_name="Trainer",
            last_name="User",
            password="password123",
            is_trainer=True,
        )
        self.trainer = Trainer.objects.create(id=uuid.uuid4(), user=self.trainer_user)
        self.apprentice_user = User.objects.create_user(
            id=uuid.uuid4(),
            email="apprentice@example.com",
            first_name="Apprentice",
            last_name="User",
            password="password123",
            is_apprentice=True,
        )
        self.apprentice = Apprentice.objects.create(
            id=uuid.uuid4(),
            user=self.apprentice_user,
            year_of_apprenticeship=1,
            status="active",
        )
        self.mentor_user = User.objects.create_user(
            id=uuid.uuid4(),
            email="mentor@example.com",
            first_name="Mentor",
            last_name="User",
            password="password123",
            is_mentor=True,
            is_external=False,
        )
        self.mentor = Mentor.objects.create(id=uuid.uuid4(), user=self.mentor_user)

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_create_apprentice(self):
        token = self.get_jwt_token(self.trainer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        data = {
            "user": {
                "email": "new_apprentice@example.com",
                "first_name": "New",
                "last_name": "Apprentice",
                "password": "password123",
            },
            "year_of_apprenticeship": 2,
            "status": "active",
        }
        response = self.client.post("/users/apprentices/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Apprentice.objects.count(), 2)

    def test_create_apprentice_unauthorized(self):
        token = self.get_jwt_token(self.apprentice_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        data = {
            "user": {
                "email": "new_apprentice@example.com",
                "first_name": "New",
                "last_name": "Apprentice",
                "password": "password123",
            },
            "year_of_apprenticeship": 2,
            "status": "active",
        }
        response = self.client.post("/users/apprentices/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_apprentice(self):
        token = self.get_jwt_token(self.apprentice_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        data = {"year_of_apprenticeship": 2, "status": "inactive"}
        response = self.client.put(
            f"/users/apprentices/{self.apprentice.id}/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.apprentice.refresh_from_db()
        self.assertEqual(self.apprentice.year_of_apprenticeship, 2)
        self.assertEqual(self.apprentice.status, "inactive")

    def test_update_apprentice_unauthorized(self):
        other_user = User.objects.create_user(
            id=uuid.uuid4(),
            email="other@example.com",
            first_name="Other",
            last_name="User",
            password="password123",
            is_apprentice=True,
        )
        token = self.get_jwt_token(other_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        data = {"year_of_apprenticeship": 2}
        response = self.client.put(
            f"/users/apprentices/{self.apprentice.id}/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_apprentice(self):
        token = self.get_jwt_token(self.trainer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.delete(f"/users/apprentices/{self.apprentice.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Apprentice.objects.count(), 0)
        self.assertEqual(User.objects.filter(id=self.apprentice_user.id).count(), 0)

    def test_list_apprentices(self):
        token = self.get_jwt_token(self.trainer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get("/users/apprentices/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_mentor(self):
        token = self.get_jwt_token(self.trainer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        data = {
            "user": {
                "email": "new_mentor@example.com",
                "first_name": "New",
                "last_name": "Mentor",
                "password": "password123",
                "is_external": True,
            }
        }
        response = self.client.post("/users/mentors/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Mentor.objects.count(), 2)

    def test_create_trainer(self):
        token = self.get_jwt_token(self.trainer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        data = {
            "user": {
                "email": "new_trainer@example.com",
                "first_name": "New",
                "last_name": "Trainer",
                "password": "password123",
            }
        }
        response = self.client.post("/users/trainers/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Trainer.objects.count(), 2)

    def test_model_str(self):
        self.assertEqual(str(self.apprentice), self.apprentice_user.email)
        self.assertEqual(str(self.mentor), self.mentor_user.email)
        self.assertEqual(str(self.trainer), self.trainer_user.email)

    def test_jwt_authentication(self):
        data = {"email": "trainer@example.com", "password": "password123"}
        response = self.client.post("/users/token/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
