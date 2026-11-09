import argparse
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tests", type=int, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--min", dest="minimum", type=float, required=True)
    parser.add_argument("--max", dest="maximum", type=float, required=True)
    parser.add_argument("--type", choices=("Float", "Double"), required=True)
    parser.add_argument(
        "--property",
        choices=(
            "AdditionAssociativity",
            "MultiplicationAssociativity",
            "Distributivity",
        ),
        required=True,
    )
    parser.add_argument("--inclusive", action="store_true")
    args = parser.parse_args()

    dtype = np.float32 if args.type == "Float" else np.float64
    random = np.random.Generator(np.random.MT19937(args.seed))
    equal = 0
    chunk_size = 1_000_000
    scale = 1 << 53

    for offset in range(0, args.tests, chunk_size):
        size = min(chunk_size, args.tests - offset)
        if args.inclusive:
            units = random.integers(0, scale + 1, size=(3, size), dtype=np.uint64)
            units = units.astype(np.float64) / scale
        else:
            units = random.random((3, size), dtype=np.float64)

        values = dtype(args.minimum) + dtype(args.maximum - args.minimum) * units
        x, y, z = values.astype(dtype, copy=False)

        if args.property == "AdditionAssociativity":
            left = np.add(np.add(x, y, dtype=dtype), z, dtype=dtype)
            right = np.add(x, np.add(y, z, dtype=dtype), dtype=dtype)
        elif args.property == "MultiplicationAssociativity":
            left = np.multiply(np.multiply(x, y, dtype=dtype), z, dtype=dtype)
            right = np.multiply(x, np.multiply(y, z, dtype=dtype), dtype=dtype)
        else:
            left = np.multiply(x, np.add(y, z, dtype=dtype), dtype=dtype)
            right = np.add(
                np.multiply(x, y, dtype=dtype),
                np.multiply(x, z, dtype=dtype),
                dtype=dtype,
            )
        equal += int(np.count_nonzero(left == right))

    print(json.dumps({
        "equal": equal,
        "percentage": 100.0 * equal / args.tests,
    }))


if __name__ == "__main__":
    main()
