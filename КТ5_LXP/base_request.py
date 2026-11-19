import json

import requests


class BaseRequest:
    """Базовый класс для выполнения HTTP-запросов к API."""

    def __init__(self, base_url, timeout=15):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })

    def _request(
        self,
        method,
        endpoint,
        data=None,
        params=None,
        expected_status=None
    ):
        """Выполняет HTTP-запрос и возвращает объект Response."""

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        response = self.session.request(
            method=method.upper(),
            url=url,
            json=data,
            params=params,
            timeout=self.timeout
        )

        # Вывод информации о запросе и ответе
        print("\n========== API REQUEST ==========")
        print(f"Method: {method.upper()}")
        print(f"URL: {response.url}")
        print(f"Status code: {response.status_code}")
        print(f"Reason: {response.reason}")
        print(f"Response body: {response.text}")
        print("=================================\n")

        if expected_status is not None:
            if response.status_code != expected_status:
                raise AssertionError(
                    f"Expected status {expected_status}, "
                    f"received {response.status_code}"
                )
        elif not response.ok:
            raise requests.HTTPError(
                f"HTTP error {response.status_code}: {response.text}",
                response=response
            )

        return response

    def get(self, endpoint, params=None, expected_status=None):
        return self._request(
            "GET",
            endpoint,
            params=params,
            expected_status=expected_status
        )

    def post(self, endpoint, data=None, expected_status=None):
        return self._request(
            "POST",
            endpoint,
            data=data,
            expected_status=expected_status
        )

    def put(self, endpoint, data=None, expected_status=None):
        return self._request(
            "PUT",
            endpoint,
            data=data,
            expected_status=expected_status
        )

    def delete(self, endpoint, expected_status=None):
        return self._request(
            "DELETE",
            endpoint,
            expected_status=expected_status
        )

    @staticmethod
    def get_json(response):
        """Безопасно получает JSON из ответа."""
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return None

    def close(self):
        self.session.close()


BASE_URL_PETSTORE = "https://petstore.swagger.io/v2"
