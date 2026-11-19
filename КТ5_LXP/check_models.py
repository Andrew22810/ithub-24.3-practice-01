from pydantic import ValidationError

from models import User, Order


user = User(
    id=10001,
    username="student_kt5",
    firstName="Ivan",
    lastName="Petrov",
    email="ivan.petrov@example.com",
    password="test_password_123",
    phone="79990000000",
    userStatus=1
)

order = Order(
    id=10003,
    petId=1,
    quantity=2,
    shipDate="2026-11-19T12:00:00Z",
    status="placed",
    complete=True
)

print("USER JSON:")
print(user.model_dump_json(by_alias=True, indent=2))

print("\nORDER JSON:")
print(order.model_dump_json(by_alias=True, indent=2))

print("\nПроверка некорректного пользователя:")

try:
    User(id=-1, username="", userStatus=-5)
except ValidationError as error:
    print("Ошибка валидации обнаружена:")
    print(error)
