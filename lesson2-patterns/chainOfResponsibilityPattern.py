import re
from abc import abstractmethod


# Handler interface
class ArithmeticOperation:
    def __init__(self):
        self._next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    @abstractmethod
    def calculate(self, expression):
        if self._next_handler:
            return self._next_handler.calculate(expression)
        return None


# Concrete handlers
class PlusOperation(ArithmeticOperation):
    def calculate(self, expression):
        if expression['operation'] == '+':
            return expression['ints'][0] + expression['ints'][1]
        return super().calculate(expression)


class MinusOperation(ArithmeticOperation):
    def calculate(self, expression):
        if expression['operation'] == '-':
            return expression['ints'][0] - expression['ints'][1]
        return super().calculate(expression)


class MultiplyOperation(ArithmeticOperation):
    def calculate(self, expression):
        if expression['operation'] == '*':
            return expression['ints'][0] * expression['ints'][1]
        return super().calculate(expression)


class DivideOperation(ArithmeticOperation):
    def calculate(self, expression):
        if expression['operation'] == '/':
            if expression['ints'][1] != 0:
                return expression['ints'][0] / expression['ints'][1]
            else:
                return 'Ошибка: деление на ноль невозможно'
        return super().calculate(expression)


# Example usage
def main():
    # Chain of responsibility
    add_handler = PlusOperation()
    minus_handler = MinusOperation()
    multiply_handler = MultiplyOperation()
    divide_handler = DivideOperation()

    add_handler.set_next(minus_handler).set_next(multiply_handler).set_next(divide_handler)

    expressions = [
        "5+3",
        "10-4",
        "7*2",
        "9/3",
        "'operation': '*', 'a': 11, 'b': 2",
        "10/0",
        "1001",
        "10+",
        "+10",
        "+++",
        "ошибка"
    ]

    # Process requests
    for expression in expressions:
        transformed_exp = transform_validate(expression)
        if transformed_exp:
            print(f"{expression} = {add_handler.calculate(transformed_exp)}")
        else:
            print('Ошибка: выражение некорректно')


def transform_validate(expression):
    operation = re.search(r'[+-/*]', expression)
    ints = list(map(int, re.findall(r'\d+', expression)))
    if operation and len(ints) == 2:
        return {
            'operation': operation.group(),
            'ints': ints
        }
    else:
        return None


if __name__ == "__main__":
    main()
