import pytest
from httpx import AsyncClient

from fast_acl.db import Database
from fast_acl.models import ClassRoom
from fast_acl.repository import ClassroomRepository


@pytest.fixture
def classroom():
    yield ClassroomRepository(Database).get_random_classroom()


class TestStudentOperations:
    @pytest.mark.asyncio
    async def test_add_student(self, student_client: AsyncClient, classroom: ClassRoom):
        TestStudentOperations.classroom_id = classroom.id

        # Add student to classroom.
        new_student_data = {
            "username": "new_student",
            "password": "password123",
            "classroom_id": str(self.classroom_id),
        }
        response = await student_client.post(
            f"/classroom/{self.classroom_id}/student", json=new_student_data
        )
        assert response.status_code == 200
        TestStudentOperations.student_id = response.json()["student_id"]

        # Check if the student has been added
        response = await student_client.get(
            f"/classroom/{self.classroom_id}/student/{self.student_id}"
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_expel_student(self, student_client: AsyncClient):
        # Make sure student isn't expeled yet
        response = await student_client.get(
            f"/classroom/{self.classroom_id}/student/{self.student_id}"
        )
        assert response.status_code == 200
        assert response.json()["is_expeled"] is False

        # Expel the student
        response = await student_client.patch(
            f"/classroom/{self.classroom_id}/student/{self.student_id}"
        )
        assert response.status_code == 200

        # Check if the student has been expelled
        response = await student_client.get(
            f"/classroom/{self.classroom_id}/student/{self.student_id}"
        )
        assert response.status_code == 200
        assert response.json()["is_expeled"] is True

    @pytest.mark.asyncio
    async def test_update_student_grade(self, student_client: AsyncClient):
        response = await student_client.get(
            f"/classroom/{self.classroom_id}/student/{self.student_id}"
        )
        assert response.status_code == 200
        grade = response.json()["grade"] or 50
        final_grade = grade + 10

        response = await student_client.put(
            f"/classroom/{self.classroom_id}/student/{self.student_id}",
            json={"grade": final_grade},
        )
        assert response.status_code == 200

        response = await student_client.get(
            f"/classroom/{self.classroom_id}/student/{self.student_id}"
        )
        assert response.status_code == 200
        assert response.json()["grade"] == final_grade
