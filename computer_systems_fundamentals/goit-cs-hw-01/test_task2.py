"""
Тести для інтерпретатора арифметичних виразів.
Перевіряє роботу Lexer, Parser та Interpreter.
"""

import importlib.util


def load(path):
    spec = importlib.util.spec_from_file_location("_mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_m = load("03_interpreter.py")
Lexer = _m.Lexer
Parser = _m.Parser
Interpreter = _m.Interpreter
TokenType = _m.TokenType
Token = _m.Token
LexicalError = _m.LexicalError
ParsingError = _m.ParsingError
BinOp = _m.BinOp
Num = _m.Num


# ─────────────────────────────────────────────
# Допоміжні функції
# ─────────────────────────────────────────────

def evaluate(expr: str):
    """Обчислює вираз через повний ланцюжок Lexer → Parser → Interpreter."""
    lexer = Lexer(expr)
    parser = Parser(lexer)
    return Interpreter(parser).interpret()


def tokenize(expr: str):
    """Повертає список токенів для виразу (без EOF)."""
    lexer = Lexer(expr)
    tokens = []
    tok = lexer.get_next_token()
    while tok.type != TokenType.EOF:
        tokens.append(tok)
        tok = lexer.get_next_token()
    return tokens


PASS = "✅ PASSED"
FAIL = "❌ FAILED"

passed = 0
failed = 0


def run_test(description: str, got, expected):
    global passed, failed
    ok = got == expected
    status = PASS if ok else FAIL
    if ok:
        passed += 1
    else:
        failed += 1
    print(f"  {status}  {description}")
    if not ok:
        print(f"           очікувано: {expected!r}")
        print(f"           отримано:  {got!r}")


def run_error_test(description: str, func, error_type):
    """Перевіряє, що func() кидає виняток error_type."""
    global passed, failed
    try:
        func()
        failed += 1
        print(f"  {FAIL}  {description}")
        print(
            f"           очікувано виняток {error_type.__name__}, але його не було")
    except error_type:
        passed += 1
        print(f"  {PASS}  {description}")
    except Exception as e:
        failed += 1
        print(f"  {FAIL}  {description}")
        print(
            f"           очікувано {error_type.__name__}, отримано {type(e).__name__}: {e}")


def section(title: str):
    print(f"\n{'─' * 55}")
    print(f"  {title}")
    print(f"{'─' * 55}")


# ═══════════════════════════════════════════════════════
# 1. ТЕСТИ ЛЕКСЕРА
# ═══════════════════════════════════════════════════════
section("1. Лексер — розпізнавання токенів")

toks = tokenize("3 + 5")
run_test("3 + 5  →  [INTEGER(3), PLUS, INTEGER(5)]",
         [(t.type, t.value) for t in toks],
         [(TokenType.INTEGER, 3), (TokenType.PLUS, "+"),
          (TokenType.INTEGER, 5)])

toks = tokenize("10 - 4")
run_test("10 - 4  →  [INTEGER(10), MINUS, INTEGER(4)]",
         [(t.type, t.value) for t in toks],
         [(TokenType.INTEGER, 10), (TokenType.MINUS, "-"),
          (TokenType.INTEGER, 4)])

toks = tokenize("6 * 7")
run_test("6 * 7  →  MUL розпізнається",
         any(t.type == TokenType.MUL for t in toks), True)

toks = tokenize("8 / 2")
run_test("8 / 2  →  DIV розпізнається",
         any(t.type == TokenType.DIV for t in toks), True)

toks = tokenize("(2 + 3)")
run_test("(2 + 3)  →  LPAREN та RPAREN розпізнаються",
         (any(t.type == TokenType.LPAREN for t in toks),
          any(t.type == TokenType.RPAREN for t in toks)),
         (True, True))

toks = tokenize("  42  ")
run_test("пробіли ігноруються — '  42  ' → один INTEGER(42)",
         [(t.type, t.value) for t in toks],
         [(TokenType.INTEGER, 42)])

run_error_test("невідомий символ '@' → LexicalError",
               lambda: tokenize("2 @ 3"), LexicalError)

# ═══════════════════════════════════════════════════════
# 2. ТЕСТИ ПАРСЕРА — пріоритет операцій
# ═══════════════════════════════════════════════════════
section("2. Парсер — правильна побудова AST (пріоритет)")


# Перевіряємо, що 2+3*4 будується як BinOp(2, +, BinOp(3, *, 4))

def ast_for(expr):
    return Parser(Lexer(expr)).expr()


tree = ast_for("2 + 3 * 4")
run_test("2 + 3 * 4  →  корінь дерева: PLUS (не MUL)",
         tree.op.type, TokenType.PLUS)
run_test("2 + 3 * 4  →  праве піддерево кореня: MUL",
         tree.right.op.type, TokenType.MUL)

tree = ast_for("(2 + 3) * 4")
run_test("(2 + 3) * 4  →  корінь дерева: MUL",
         tree.op.type, TokenType.MUL)
run_test("(2 + 3) * 4  →  ліве піддерево кореня: PLUS",
         tree.left.op.type, TokenType.PLUS)

tree = ast_for("10 / 2 - 1")
run_test("10 / 2 - 1  →  корінь: MINUS",
         tree.op.type, TokenType.MINUS)
run_test("10 / 2 - 1  →  ліве піддерево: DIV",
         tree.left.op.type, TokenType.DIV)

# ═══════════════════════════════════════════════════════
# 3. ТЕСТИ ІНТЕРПРЕТАТОРА — числові результати
# ═══════════════════════════════════════════════════════
section("3. Інтерпретатор — додавання та віднімання")

run_test("3 + 5 = 8", evaluate("3 + 5"), 8)
run_test("10 - 4 = 6", evaluate("10 - 4"), 6)
run_test("1 + 2 + 3 = 6", evaluate("1 + 2 + 3"), 6)
run_test("10 - 3 - 2 = 5", evaluate("10 - 3 - 2"), 5)
run_test("0 + 7 = 7", evaluate("0 + 7"), 7)

section("4. Інтерпретатор — множення та ділення")

run_test("6 * 7 = 42", evaluate("6 * 7"), 42)
run_test("20 / 4 = 5.0", evaluate("20 / 4"), 5.0)
run_test("3 * 3 * 3 = 27", evaluate("3 * 3 * 3"), 27)
run_test("100 / 10 / 2 = 5.0", evaluate("100 / 10 / 2"), 5.0)

section("5. Інтерпретатор — пріоритет (без дужок)")

run_test("2 + 3 * 4 = 14", evaluate("2 + 3 * 4"), 14)
run_test("10 - 2 * 3 = 4", evaluate("10 - 2 * 3"), 4)
run_test("8 / 2 + 1 = 5.0", evaluate("8 / 2 + 1"), 5.0)
run_test("7 * 3 + 2 = 23", evaluate("7 * 3 + 2"), 23)
run_test("3 + 4 * 2 - 1 = 10", evaluate("3 + 4 * 2 - 1"), 10)

section("6. Інтерпретатор — вирази з дужками")

run_test("(2 + 3) * 4 = 20", evaluate("(2 + 3) * 4"), 20)
run_test("(10 - 4) / 3 = 2.0", evaluate("(10 - 4) / 3"), 2.0)
run_test("100 / (2 * 5) = 10.0", evaluate("100 / (2 * 5)"), 10.0)
run_test("(1 + 2) * (3 + 4) = 21", evaluate("(1 + 2) * (3 + 4)"), 21)
run_test("((2 + 3)) * 4 = 20", evaluate("((2 + 3)) * 4"), 20)
run_test("(5 - 3) * (8 / 4) = 4.0", evaluate("(5 - 3) * (8 / 4)"), 4.0)

section("7. Інтерпретатор — крайні випадки")

run_test("одне число: 42 = 42", evaluate("42"), 42)
run_test("0 * 999 = 0", evaluate("0 * 999"), 0)
run_test("1 * 1 * 1 = 1", evaluate("1 * 1 * 1"), 1)
run_test("(0 + 5) = 5", evaluate("(0 + 5)"), 5)

section("8. Інтерпретатор — обробка помилок")

run_error_test("ділення на нуль → ZeroDivisionError",
               lambda: evaluate("10 / 0"), ZeroDivisionError)

run_error_test("незакрита дужка '(2 + 3' → ParsingError",
               lambda: evaluate("(2 + 3"), ParsingError)

run_error_test("неправильний вираз '+ 3' → ParsingError",
               lambda: evaluate("+ 3"), ParsingError)

run_error_test("невідомий символ '2 $ 3' → LexicalError",
               lambda: evaluate("2 $ 3"), LexicalError)

# ═══════════════════════════════════════════════════════
# Підсумок
# ═══════════════════════════════════════════════════════
total = passed + failed
print(f"\n{'═' * 55}")
print(f"  Результат: {passed}/{total} тестів пройдено", end="  ")
print("🎉" if failed == 0 else "⚠️  є помилки")
print(f"{'═' * 55}")
