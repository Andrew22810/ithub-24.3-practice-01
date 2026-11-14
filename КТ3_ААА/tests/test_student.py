"""Собственные проверки проекта «Медиаполка»."""

from copy import deepcopy

from mediapolka import issue, new_state, return_loan

import unittest


class StudentTests(unittest.TestCase):

    def test_repeated_return_does_not_change_state(self):
        state = new_state()

        issued = issue(state, "mic", "1")
        loan_id = issued["loan_id"]

        first_return = return_loan(state, loan_id)
        self.assertTrue(first_return["ok"])

        before = deepcopy(state)
        second_return = return_loan(state, loan_id)

        self.assertFalse(second_return["ok"])
        self.assertEqual(second_return["message"], "Уже возвращено")
        self.assertEqual(state, before)

    def test_unknown_loan_id_does_not_change_state(self):
        state = new_state()
        before = deepcopy(state)

        result = return_loan(state, 999)

        self.assertFalse(result["ok"])
        self.assertEqual(result["message"], "Выдача не найдена")
        self.assertEqual(state, before)

    def test_return_issued_loan(self):
        state = new_state()

        result = issue(state, "mic", "2")
        loan_id = result["loan_id"]

        returned = return_loan(state, loan_id)

        self.assertTrue(returned["ok"])
        self.assertEqual(returned["message"], "Возвращено")
        self.assertEqual(state["stock"]["mic"], 3)
        self.assertEqual(len(state["loans"]), 1)
        self.assertEqual(state["loans"][0]["status"], "returned")
        self.assertEqual(state["loans"][0]["quantity"], 2)

    def test_successful_issuance_and_next_id(self):
        state = new_state()

        first = issue(state, "mic", "1")

        self.assertTrue(first["ok"])
        self.assertEqual(first["message"], "Выдано")
        self.assertEqual(first["loan_id"], 1)
        self.assertEqual(state["stock"]["mic"], 2)
        self.assertEqual(len(state["loans"]), 1)
        self.assertEqual(state["loans"][0]["status"], "issued")

        second = issue(state, "tripod", "1")

        self.assertTrue(second["ok"])
        self.assertEqual(second["loan_id"], 2)
        self.assertEqual(state["stock"]["tripod"], 0)
        self.assertEqual(len(state["loans"]), 2)

    def test_insufficient_stock_does_not_change_state(self):
        state = new_state()
        before = deepcopy(state)

        result = issue(state, "tripod", "2")

        self.assertFalse(result["ok"])
        self.assertEqual(result["message"], "Недостаточно оборудования")
        self.assertEqual(state, before)

    def test_invalid_quantities_do_not_change_state(self):
        invalid_values = ("", "abc", "1.5", "-1", "0", "4")

        for value in invalid_values:
            with self.subTest(value=value):
                state = new_state()
                before = deepcopy(state)

                result = issue(state, "mic", value)

                self.assertFalse(result["ok"])
                self.assertEqual(
                    result["message"],
                    "Введите целое количество от 1 до 3"
                )
                self.assertEqual(state, before)

    def test_valid_quantities(self):
        for quantity in ("1", "2", "3"):

            with self.subTest(quantity=quantity):
                state = new_state()

                result = issue(state, "mic", quantity)

                self.assertTrue(result["ok"])
                self.assertEqual(result["message"], "Выдано")
                self.assertEqual(state["stock"]["mic"], 3 - int(quantity))
                self.assertEqual(len(state["loans"]), 1)
                self.assertEqual(state["loans"][0]["quantity"], int(quantity))

    def test_initial_state(self):
        state = new_state()

        self.assertEqual(
            state,
            {
                "stock": {
                    "mic": 3,
                    "tripod": 1,
                    "light": 0,
                },
                "loans": [],
                "next_id": 1,
            },
        )

    def test_states_are_independent(self):
        first = new_state()
        second = new_state()

        first["stock"]["mic"] = 0

        self.assertEqual(second["stock"]["mic"], 3)
        self.assertEqual(second["loans"], [])
        self.assertEqual(second["next_id"], 1)


if __name__ == "__main__":
    unittest.main()
