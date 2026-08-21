# Лексичний аналізатор (токенізатор) для простого інтерпретатора арифметичних виразів.
class TokenType:
    INTEGER = "INTEGER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    EOF = "EOF"  # Означає кінець строки


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {repr(self.value)})"


class LexicalError(Exception):
    pass


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def error(self):
        raise LexicalError(f"Invalid character: {self.current_char}")

    def advance(self):
        """Переміщує позицію вперед і оновлює current_char."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Кінець вводу
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        """Пропускає пробіли."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Повертає багатозначне ціле число з вводу."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """Лексичний аналізатор (токенізатор)."""
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(TokenType.INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-')

            self.error()

        return Token(TokenType.EOF, None)


# Статичний аналізатор (парсер) для простого інтерпретатора арифметичних виразів.
class AST:
    pass


class BinOp(AST):
    def __init__(self, left, op, right) -> None:
        self.left = left
        self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token) -> None:
        self.token = token
        self.value = token.value


class ParsingError(Exception):
    pass


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self) -> None:
        raise ParsingError('Помилка синтаксичного аналізу')

    def eat(self, token_type) -> None:
        """
        Порівнюємо поточний токен з очікуваним токеном і, якщо вони збігаються,
        'поглинаємо' його й переходимо до наступного токена.
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def term(self):
        """ Парсер для 'term' правил граматики. У нашому випадку - це цілі числа."""
        token = self.current_token
        self.eat(TokenType.INTEGER)
        return Num(token)

    def expr(self):
        """ Парсер для арифметичних виразів. """
        node = self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node


def print_ast(node, level=0):
    indent = ' ' * level
    if isinstance(node, Num):
        print(f"{indent}Num({node.value})")
    elif isinstance(node, BinOp):
        print(f"{indent}BinOp:")
        print(f"{indent} left: ")
        print_ast(node.left, level + 2)
        print(f"{indent} op: {node.op.type}")
        print(f"{indent} right: ")
        print_ast(node.right, level + 2)
    else:
        print(f"{indent}Unknown node type: {type(node)}")


# Створення Інтерпретатора
class Interpreter:
    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):
        if node.op.type == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def interpret(self):
        tree = self.parser.expr()
        print_ast(tree)
        return self.visit(tree)

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'Немає методу visit_{type(node).__name__}')


def main():
    while True:
        try:
            text = input('Введіть вираз (або "exit" для виходу): ')
            if text.lower() == 'exit':
                print("Вихід із програми.")
                break
            lexer = Lexer(text)
            parser = Parser(lexer)
            interpreter = Interpreter(parser)
            result = interpreter.interpret()
            print(result)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
