from urllib.parse import quote

from base_request import BaseRequest, BASE_URL_PETSTORE


class UserRequests(BaseRequest):
    """Запросы для работы с пользователями Petstore API."""

    def create_user(self, user_data):
        """POST /user — создание пользователя."""
        response = self.post(
            "user",
            data=user_data,
            expected_status=200
        )
        return self.get_json(response)

    def get_user(self, username):
        """GET /user/{username} — получение пользователя."""
        endpoint = f"user/{quote(username, safe='')}"
        response = self.get(
            endpoint,
            expected_status=200
        )
        return self.get_json(response)

    def update_user(self, username, user_data):
        """PUT /user/{username} — обновление пользователя."""
        endpoint = f"user/{quote(username, safe='')}"
        response = self.put(
            endpoint,
            data=user_data,
            expected_status=200
        )
        return self.get_json(response)

    def delete_user(self, username):
        """DELETE /user/{username} — удаление пользователя."""
        endpoint = f"user/{quote(username, safe='')}"
        response = self.delete(
            endpoint,
            expected_status=200
        )
        return self.get_json(response)


if __name__ == "__main__":
    api = UserRequests(BASE_URL_PETSTORE)

    username = "student_kt3_lxp"

    user_data = {
        "id": 10001,
        "username": username,
        "firstName": "Ivan",
        "lastName": "Petrov",
        "email": "ivan.petrov@example.com",
        "password": "test_password_123",
        "phone": "79990000000",
        "userStatus": 1
    }

    updated_user_data = {
        **user_data,
        "firstName": "Petr",
        "email": "petr.petrov@example.com"
    }

    try:
        print("1. CREATE USER")
        print(api.create_user(user_data))

        print("\n2. GET USER")
        print(api.get_user(username))

        print("\n3. UPDATE USER")
        print(api.update_user(username, updated_user_data))

        print("\n4. GET UPDATED USER")
        print(api.get_user(username))

        print("\n5. DELETE USER")
        print(api.delete_user(username))

    finally:
        api.close()
