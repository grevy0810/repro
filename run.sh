#!/bin/sh
set -e
echo "running Associativity"
java Associativity
echo "running BankingProblem"
java BankingProblem

echo "finished"