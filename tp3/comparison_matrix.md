## Comparison matrix

| Program | Language | Repetitions | Data type | Random generator | Seed | Value range | Distribution | Negative values | Comparison | Result |
|---|---|---:|---|---|---|---|---|---|---|---:|
| Yours (Lab #1) | Java | 100,000,000 | `double` | `java.util.Random` | Default | [0, 1) | Uniform | No | `==` | 82.809352% |
| LLM (Lab #2) | Python | 1,000,000 | `float` | Mersenne Twister | 42 | [-1e16, 1e16] | Uniform | Yes | `==` | 92.4212% |
| LLM (Lab #3) | Java | 1,000,000 | `double` | `java.util.Random` | 42 | [-1e16, 1e16) | Uniform | Yes | `==` | 92.4047% |

## What does the third program tell us?

- Lab #1 and Lab #3 show that two Java implementations can produce different results because of their implementation choices.
- Lab #2 and Lab #3 produce very similar results (92.4212% and 92.4047%), despite using different programming languages.
- This suggests that the value range and other experimental parameters have a strong influence on the results.