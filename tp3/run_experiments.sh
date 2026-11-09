#!/bin/bash

javac AssociativityCLI.java

for seed in 42 123
do
    for range in 1e10 1e16
    do
        java AssociativityCLI \
            --tests=1000000 \
            --seed=$seed \
            --min=-$range \
            --max=$range
    done
done