from decimal import Decimal, getcontext, ROUND_DOWN

print(Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))
print(Decimal("0.1") + Decimal("0.2"))

getcontext().prec = 6

print(Decimal("1") / Decimal("7"))

getcontext().prec = 8
print(Decimal("1") / Decimal("7"))

getcontext().prec = 6
print(Decimal("233") / Decimal("7"))

number = Decimal('3.1415926535897932384626433832795')

rounded_number = number.quantize(Decimal('0.00'), ROUND_DOWN)
print(rounded_number)