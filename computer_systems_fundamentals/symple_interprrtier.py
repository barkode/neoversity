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


def main() -> None:
    while True:
        try:
            text = input('Введіть вираз (або "exit" для виходу): ')
            if text.lower() == 'exit':
                print("Вихід із програми.")
                break
            if not text:
                continue
            lexer = Lexer(text)
            token = lexer.get_next_token()
            while token.type != TokenType.EOF:
                print(token)
                token = lexer.get_next_token()
        except LexicalError as e:
            print(e)
        except EOFError:
            break


class ACT:
    pass


class BinOp(ACT):
    def __init__(self, left, op, right) -> None:
        self.left = left
        self.op = op
        self.right = right


class Num(ACT):
    def __init__(self, token) -> None:
        self.token = token
        self.value = token.value


if __name__ == '__main__':
    main()
