#!/bin/sh
set -e
cd "$(dirname "$0")"
echo "running Associativity"
java Associativity
echo "running BankingProblem"
java BankingProblem

echo "finished"
