"""
test_task2.py — Тести для інтерпретатора арифметичних виразів (task2.py).

Секції:
  1. Лексер          — розпізнавання токенів
  2. Парсер          — правильна структура AST / пріоритет операцій
  3. Інтерпретатор   — додавання та віднімання
  4. Інтерпретатор   — множення та ділення
  5. Інтерпретатор   — пріоритет без дужок
  6. Інтерпретатор   — вирази з дужками
  7. Інтерпретатор   — крайні випадки
  8. Обробка помилок — LexicalError / ParsingError / ZeroDivisionError
"""

from task2 import (BinOp, evaluate, Lexer, LexicalError, Num, Parser,
                   ParsingError, TokenType)

# ─────────────────────────────────────────────
#  Мінімальний тест-раннер
# ─────────────────────────────────────────────

_passed = 0
_failed = 0


def check(description: str, got, expected):
    global _passed, _failed
    if got == expected:
        _passed += 1
        print(f"  ✅ PASSED  {description}")
    else:
        _failed += 1
        print(f"  ❌ FAILED  {description}")
        print(f"             очікувано: {expected!r}")
        print(f"             отримано:  {got!r}")


def check_raises(description: str, func, error_type):
    global _passed, _failed
    try:
        func()
        _failed += 1
        print(f"  ❌ FAILED  {description}")
        print(
            f"             очікувано виняток {error_type.__name__}, але його не було")
    except error_type:
        _passed += 1
        print(f"  ✅ PASSED  {description}")
    except Exception as e:
        _failed += 1
        print(f"  ❌ FAILED  {description}")
        print(
            f"             очікувано {error_type.__name__}, отримано {type(e).__name__}: {e}")


def section(title: str):
    print(f"\n{'─' * 57}")
    print(f"  {title}")
    print(f"{'─' * 57}")


# ─────────────────────────────────────────────
#  Допоміжна функція: токенізація рядка
# ─────────────────────────────────────────────

def tokenize(expr: str):
    lexer = Lexer(expr)
    tokens = []
    tok = lexer.get_next_token()
    while tok.type != TokenType.EOF:
        tokens.append(tok)
        tok = lexer.get_next_token()
    return tokens


def token_types(expr: str):
    return [t.type for t in tokenize(expr)]


# ─────────────────────────────────────────────
#  Допоміжна функція: корінь AST
# ─────────────────────────────────────────────

def ast(expr: str):
    return Parser(Lexer(expr)).expr()


# ═══════════════════════════════════════════════════════════
#  1. ЛЕКСЕР — розпізнавання токенів
# ═══════════════════════════════════════════════════════════
section("1. Лексер — розпізнавання токенів")

check("INTEGER розпізнається",
      token_types("42"), [TokenType.INTEGER])

check("PLUS розпізнається",
      token_types("1 + 2"),
      [TokenType.INTEGER, TokenType.PLUS, TokenType.INTEGER])

check("MINUS розпізнається",
      token_types("5 - 3"),
      [TokenType.INTEGER, TokenType.MINUS, TokenType.INTEGER])

check("MUL розпізнається",
      token_types("6 * 7"),
      [TokenType.INTEGER, TokenType.MUL, TokenType.INTEGER])

check("DIV розпізнається",
      token_types("8 / 2"),
      [TokenType.INTEGER, TokenType.DIV, TokenType.INTEGER])

check("LPAREN та RPAREN розпізнаються",
      token_types("(2 + 3)"),
      [TokenType.LPAREN, TokenType.INTEGER, TokenType.PLUS,
       TokenType.INTEGER, TokenType.RPAREN])

check("значення токена INTEGER зчитується правильно",
      [(t.type, t.value) for t in tokenize("3 + 5")],
      [(TokenType.INTEGER, 3), (TokenType.PLUS, "+"), (TokenType.INTEGER, 5)])

check("пробіли ігноруються",
      token_types("  42  "), [TokenType.INTEGER])

check("багатоцифрове число '123'",
      [(t.type, t.value) for t in tokenize("123")],
      [(TokenType.INTEGER, 123)])

check_raises("невідомий символ '@' → LexicalError",
             lambda: tokenize("2 @ 3"), LexicalError)

check_raises("невідомий символ '$' → LexicalError",
             lambda: tokenize("2 $ 3"), LexicalError)

# ═══════════════════════════════════════════════════════════
#  2. ПАРСЕР — структура AST та пріоритет операцій
# ═══════════════════════════════════════════════════════════
section("2. Парсер — структура AST (пріоритет операцій)")

tree = ast("2 + 3 * 4")
check("2 + 3 * 4  →  корінь дерева: PLUS (не MUL)",
      tree.op.type, TokenType.PLUS)
check("2 + 3 * 4  →  праве піддерево кореня: MUL",
      tree.right.op.type, TokenType.MUL)

tree = ast("(2 + 3) * 4")
check("(2 + 3) * 4  →  корінь дерева: MUL",
      tree.op.type, TokenType.MUL)
check("(2 + 3) * 4  →  ліве піддерево кореня: PLUS",
      tree.left.op.type, TokenType.PLUS)

tree = ast("10 / 2 - 1")
check("10 / 2 - 1  →  корінь: MINUS",
      tree.op.type, TokenType.MINUS)
check("10 / 2 - 1  →  ліве піддерево кореня: DIV",
      tree.left.op.type, TokenType.DIV)

tree = ast("1 + 2 + 3")
check("1 + 2 + 3  →  ліво-асоціативне (корінь — другий PLUS)",
      isinstance(tree.left, BinOp) and tree.left.op.type == TokenType.PLUS,
      True)

tree = ast("42")
check("одне число '42'  →  вузол Num(42)",
      isinstance(tree, Num) and tree.value == 42, True)

check_raises("незакрита дужка '(2 + 3' → ParsingError",
             lambda: ast("(2 + 3"), ParsingError)

check_raises("вираз починається з оператора '+ 3' → ParsingError",
             lambda: ast("+ 3"), ParsingError)

# ═══════════════════════════════════════════════════════════
#  3. ІНТЕРПРЕТАТОР — додавання та віднімання
# ═══════════════════════════════════════════════════════════
section("3. Інтерпретатор — додавання та віднімання")

check("3 + 5 = 8", evaluate("3 + 5"), 8)
check("10 - 4 = 6", evaluate("10 - 4"), 6)
check("1 + 2 + 3 = 6", evaluate("1 + 2 + 3"), 6)
check("10 - 3 - 2 = 5", evaluate("10 - 3 - 2"), 5)
check("0 + 7 = 7", evaluate("0 + 7"), 7)
check("5 - 5 = 0", evaluate("5 - 5"), 0)

# ═══════════════════════════════════════════════════════════
#  4. ІНТЕРПРЕТАТОР — множення та ділення
# ═══════════════════════════════════════════════════════════
section("4. Інтерпретатор — множення та ділення")

check("6 * 7 = 42", evaluate("6 * 7"), 42)
check("20 / 4 = 5.0", evaluate("20 / 4"), 5.0)
check("3 * 3 * 3 = 27", evaluate("3 * 3 * 3"), 27)
check("100 / 10 / 2 = 5.0", evaluate("100 / 10 / 2"), 5.0)
check("0 * 999 = 0", evaluate("0 * 999"), 0)

# ═══════════════════════════════════════════════════════════
#  5. ІНТЕРПРЕТАТОР — пріоритет без дужок
# ═══════════════════════════════════════════════════════════
section("5. Інтерпретатор — пріоритет без дужок")

check("2 + 3 * 4 = 14  (не 20)", evaluate("2 + 3 * 4"), 14)
check("10 - 2 * 3 = 4  (не 24)", evaluate("10 - 2 * 3"), 4)
check("8 / 2 + 1 = 5.0", evaluate("8 / 2 + 1"), 5.0)
check("7 * 3 + 2 = 23", evaluate("7 * 3 + 2"), 23)
check("3 + 4 * 2 - 1 = 10", evaluate("3 + 4 * 2 - 1"), 10)

# ═══════════════════════════════════════════════════════════
#  6. ІНТЕРПРЕТАТОР — вирази з дужками
# ═══════════════════════════════════════════════════════════
section("6. Інтерпретатор — вирази з дужками")

check("(2 + 3) * 4 = 20", evaluate("(2 + 3) * 4"), 20)
check("(10 - 4) / 3 = 2.0", evaluate("(10 - 4) / 3"), 2.0)
check("100 / (2 * 5) = 10.0", evaluate("100 / (2 * 5)"), 10.0)
check("(1 + 2) * (3 + 4) = 21", evaluate("(1 + 2) * (3 + 4)"), 21)
check("((2 + 3)) * 4 = 20", evaluate("((2 + 3)) * 4"), 20)
check("(5 - 3) * (8 / 4) = 4.0", evaluate("(5 - 3) * (8 / 4)"), 4.0)
check("2 * (3 + (4 - 1)) = 12", evaluate("2 * (3 + (4 - 1))"), 12)

# ═══════════════════════════════════════════════════════════
#  7. ІНТЕРПРЕТАТОР — крайні випадки
# ═══════════════════════════════════════════════════════════
section("7. Інтерпретатор — крайні випадки")

check("одне число: 42 = 42", evaluate("42"), 42)
check("одне число: 0 = 0", evaluate("0"), 0)
check("1 * 1 * 1 = 1", evaluate("1 * 1 * 1"), 1)
check("(0 + 5) = 5", evaluate("(0 + 5)"), 5)
check("число у дужках: (7)", evaluate("(7)"), 7)

# ═══════════════════════════════════════════════════════════
#  8. ОБРОБКА ПОМИЛОК
# ═══════════════════════════════════════════════════════════
section("8. Обробка помилок")

check_raises("10 / 0  → ZeroDivisionError",
             lambda: evaluate("10 / 0"), ZeroDivisionError)

check_raises("(2 + 3  → ParsingError (незакрита дужка)",
             lambda: evaluate("(2 + 3"), ParsingError)

check_raises("+ 3  → ParsingError (вираз починається з оператора)",
             lambda: evaluate("+ 3"), ParsingError)

check_raises("2 $ 3  → LexicalError (невідомий символ)",
             lambda: evaluate("2 $ 3"), LexicalError)

check_raises("2 @ 3  → LexicalError (невідомий символ)",
             lambda: evaluate("2 @ 3"), LexicalError)

# ═══════════════════════════════════════════════════════════
#  Підсумок
# ═══════════════════════════════════════════════════════════
total = _passed + _failed
print(f"\n{'═' * 57}")
print(f"  Результат: {_passed}/{total} тестів пройдено", end="  ")
print("🎉" if _failed == 0 else "⚠️  є помилки")
print(f"{'═' * 57}")
