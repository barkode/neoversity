# ─────────────────────────────────────────────────────────
#  task2.py  —  Інтерпретатор арифметичних виразів
#
#  Підтримувані операції: + - * /  та дужки ( )
#  Граматика:
#      expr   : term   ((PLUS  | MINUS) term)*
#      term   : factor ((MUL   | DIV)   factor)*
#      factor : INTEGER | LPAREN expr RPAREN
# ─────────────────────────────────────────────────────────


# ═══════════════════════════════
#  Винятки
# ═══════════════════════════════

class LexicalError(Exception):
    pass


class ParsingError(Exception):
    pass


# ═══════════════════════════════
#  Типи токенів
# ═══════════════════════════════

class TokenType:
    INTEGER = "INTEGER"
    PLUS = "PLUS"  # +
    MINUS = "MINUS"  # -
    MUL = "MUL"  # *
    DIV = "DIV"  # /
    LPAREN = "LPAREN"  # (
    RPAREN = "RPAREN"  # )
    EOF = "EOF"


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {repr(self.value)})"


# ═══════════════════════════════
#  Лексер
# ═══════════════════════════════

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def advance(self):
        """Переміщуємо 'вказівник' на наступний символ."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        """Пропускаємо пробільні символи."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Збираємо послідовність цифр у ціле число."""
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """Повертає наступний токен з вхідного рядка."""
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(TokenType.INTEGER, self.integer())

            if self.current_char == "+":
                self.advance()
                return Token(TokenType.PLUS, "+")

            if self.current_char == "-":
                self.advance()
                return Token(TokenType.MINUS, "-")

            if self.current_char == "*":
                self.advance()
                return Token(TokenType.MUL, "*")

            if self.current_char == "/":
                self.advance()
                return Token(TokenType.DIV, "/")

            if self.current_char == "(":
                self.advance()
                return Token(TokenType.LPAREN, "(")

            if self.current_char == ")":
                self.advance()
                return Token(TokenType.RPAREN, ")")

            raise LexicalError(
                f"Помилка лексичного аналізу: невідомий символ '{self.current_char}'"
                )

        return Token(TokenType.EOF, None)


# ═══════════════════════════════
#  Вузли AST
# ═══════════════════════════════

class AST:
    pass


class BinOp(AST):
    """Бінарна операція: ліве піддерево  оператор  праве піддерево."""

    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Num(AST):
    """Числовий літерал."""

    def __init__(self, token):
        self.token = token
        self.value = token.value


# ═══════════════════════════════
#  Парсер
# ═══════════════════════════════

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise ParsingError("Помилка синтаксичного аналізу")

    def eat(self, token_type):
        """Поглинаємо поточний токен, якщо він збігається з очікуваним."""
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """
        factor : INTEGER | LPAREN expr RPAREN

        Найвищий пріоритет: числа та вирази у дужках.
        """
        token = self.current_token

        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(token)

        if token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()  # рекурсивно обробляємо вміст дужок
            self.eat(TokenType.RPAREN)
            return node

        self.error()

    def term(self):
        """
        term : factor ((MUL | DIV) factor)*

        Середній пріоритет: множення та ділення.
        """
        node = self.factor()

        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            token = self.current_token
            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
            else:
                self.eat(TokenType.DIV)
            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        """
        expr : term ((PLUS | MINUS) term)*

        Найнижчий пріоритет: додавання та віднімання.
        """
        node = self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            else:
                self.eat(TokenType.MINUS)
            node = BinOp(left=node, op=token, right=self.term())

        return node


# ═══════════════════════════════
#  Інтерпретатор
# ═══════════════════════════════

class Interpreter:
    def __init__(self, parser):
        self.parser = parser

    def visit(self, node):
        method = "visit_" + type(node).__name__
        return getattr(self, method, self.generic_visit)(node)

    def generic_visit(self, node):
        raise Exception(f"Немає методу visit_{type(node).__name__}")

    def visit_Num(self, node):
        return node.value

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op.type == TokenType.PLUS:
            return left + right
        if node.op.type == TokenType.MINUS:
            return left - right
        if node.op.type == TokenType.MUL:
            return left * right
        if node.op.type == TokenType.DIV:
            if right == 0:
                raise ZeroDivisionError("Ділення на нуль!")
            return left / right

    def interpret(self):
        tree = self.parser.expr()
        return self.visit(tree)


# ═══════════════════════════════
#  Допоміжна функція
# ═══════════════════════════════

def evaluate(expr: str):
    """Обчислює рядковий арифметичний вираз."""
    return Interpreter(Parser(Lexer(expr))).interpret()


# ═══════════════════════════════
#  Запуск у режимі REPL
# ═══════════════════════════════

def main():
    print('Інтерпретатор арифметичних виразів. Введіть "exit" для виходу.')
    while True:
        try:
            text = input(">>> ")
            if text.strip().lower() == "exit":
                print("Вихід із програми.")
                break
            if not text.strip():
                continue
            print(evaluate(text))
        except (LexicalError, ParsingError, ZeroDivisionError) as e:
            print(f"Помилка: {e}")


if __name__ == "__main__":
    main()
