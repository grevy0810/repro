import os
import random

output_dir = os.getenv("OUTPUT_DIR", ".")
os.makedirs(output_dir, exist_ok=True)

random.seed(42)

tests = 1_000_000
equal = 0

for _ in range(tests):
    x = random.uniform(-1e16, 1e16)
    y = random.uniform(-1e16, 1e16)
    z = random.uniform(-1e16, 1e16)

    if (x + y) + z == x + (y + z):
        equal += 1

percentage = equal / tests * 100

with open(
    os.path.join(output_dir, "answer_associativity_llm.txt"),
    "w",
    encoding="utf-8"
) as file:
    file.write(f"Tests: {tests}\n")
    file.write(f"Equal results: {equal}\n")
    file.write(f"Percentage: {percentage:.4f}%\n")
    file.write("Language: Python 3\n")
    file.write("Random seed: 42\n")
    file.write("Range: [-1e16, 1e16]\n")
    file.write("Comparison: exact floating-point equality\n")

print(f"Associativity: {percentage:.4f}%")