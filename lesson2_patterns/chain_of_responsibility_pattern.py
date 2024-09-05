import re
from abc import abstractmethod


class ArithmeticOperation:
    """Handler interface"""
    def __init__(self):
        self._next_handler = None
        self.result = None

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    @abstractmethod
    def calculate(self, expression):
        if 'result' in expression:
            self.result = expression['result']
        elif self._next_handler:
            return self._next_handler.calculate(expression)


class PlusOperation(ArithmeticOperation):
    """Concrete handlers"""
    def calculate(self, expression):
        if expression['operation'] == '+':
            expression['result'] = (expression['ints'][0] + expression['ints'][1])
        return super().calculate(expression)


class MinusOperation(ArithmeticOperation):
    def calculate(self, expression):
        if expression['operation'] == '-':
            expression['result'] = (expression['ints'][0] - expression['ints'][1])
        return super().calculate(expression)


class MultiplyOperation(ArithmeticOperation):
    def calculate(self, expression):
        if expression['operation'] == '*':
            expression['result'] = (expression['ints'][0] * expression['ints'][1])
        return super().calculate(expression)


class DivideOperation(ArithmeticOperation):
    def calculate(self, expression):
        if expression['operation'] == '/':
            if expression['ints'][1] != 0:
                expression['result'] = (expression['ints'][0] / expression['ints'][1])
            else:
                raise ZeroDivisionError('Ошибка: деление на ноль невозможно')
        return super().calculate(expression)


def main():
    """
    Example usage
    Chain of responsibility
    """
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
    ]

    """Process requests"""
    for expression in expressions:
        transformed_exp = transform_validate(expression)
        if transformed_exp:
            add_handler.calculate(transformed_exp)
            print(f"{expression} = {transformed_exp['result']}")
        else:
            raise ValueError('Ошибка: выражение некорректно')


def transform_validate(expression):
    operation = re.search(r'[+-/*]', expression)
    ints = list(map(int, re.findall(r'\d+', expression)))
    if operation and len(ints) == 2:
        return {
            'operation': operation.group(),
            'ints': ints
        }


if __name__ == "__main__":
    main()
