from decimal import Decimal, getcontext, ROUND_DOWN, ROUND_FLOOR, \
    ROUND_HALF_UP, ROUND_CEILING

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

number = Decimal("1.45")

# Default rounding to one decimal place
print("Default rounding ROUND_HALF_EVEN:",
      number.quantize(Decimal("0.0")))

# Rounding up on a tie (ROUND_HALF_UP)
print("Rounding up ROUND_HALF_UP:",
      number.quantize(Decimal("0.0"), rounding=ROUND_HALF_UP))

# Round down (ROUND_FLOOR)
print("Rounding down ROUND_FLOOR:",
      number.quantize(Decimal("0.0"), rounding=ROUND_FLOOR))

# Rounding up (ROUND_CEILING)
print("Rounding up ROUND_CEILING:",
      number.quantize(Decimal("0.0"), rounding=ROUND_CEILING))
