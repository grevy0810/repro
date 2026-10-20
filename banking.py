import math
import os

output_dir = os.getenv("OUTPUT_DIR", ".")
os.makedirs(output_dir, exist_ok=True)

money = math.e
years = 50

for n in range(1, years + 1):
    money = (money - 1) * n

money -= 1

with open(
    os.path.join(output_dir, "answer_banking_llm.txt"),
    "w",
    encoding="utf-8"
) as file:
    file.write(f"Initial money: {math.e}\n")
    file.write(f"Years: {years}\n")
    file.write("Annual operation: (money - 1) * n\n")
    file.write("Final withdrawal fee: 1 euro\n")
    file.write(f"Final money: {money} euros\n")

print(f"Banking result: {money} euros")