# LLM Banking

## Model information

- Model: GPT-6
- Interface: ChatGPT web interface
- Date: 2026-10-20
- Language generated: Python 3.12

## Prompt

Write a Python program to simulate the banking problem. Start with `e`, subtract one euro and multiply by the year number for each year from 1 to 50, then subtract one final euro. Save the result in `answer_banking_llm.txt`. Explain the assumptions and make the program reproducible and runnable with Docker.


## Choices and observations

The implementation uses Python floating-point arithmetic, `math.e` as the initial amount, 50 iterations, and the same operation order as the problem statement.
