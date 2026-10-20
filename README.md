# repro
# Lab 1

## Requirements

Java must be installed on the computer.

## Compile the programs

Run this command in the project directory:

```bash
javac Associativity.java BankingProblem.java
```

## Run the programs

For the associativity problem:

```bash
java Associativity
```

The result is saved in `answer_associativity.txt`.

For the banking problem:

```bash
java BankingProblem
```

The result is saved in `answer_banking.txt`.


## COMPILE WITH DOCKER
-  it's required to download docker 
After that : 
1. create the docker image

```bash
sudo docker build -t rep-lab2 .
```
2. run the docker image :
```bash
sudo docker run --rm   --user "$(id -u):$(id -g)"   -v "$(pwd):/out"   -e OUTPUT_DIR=/out   rep-lab2
```

GitHub Actions

GitHub Actions runs the Docker container automatically every time I push changes to the repository. It generates answer_associativity.txt and answer_banking.txt and pushes the updated files to the repository

## Reproduce with Nix

Install [Nix](https://nixos.org/download/), then open the project directory and enter the pinned development shell:

```bash
nix-shell
```

The shell provides the pinned nixpkgs snapshot and Java 21. Compile and run the programs with:

```bash
javac Associativity.java BankingProblem.java
./run.sh
```

The programs write `answer_associativity.txt` and `answer_banking.txt`. The nixpkgs revision and its archive checksum are pinned in `nixpkgs-pin.nix`, so `nix-shell` uses the same package catalog across machines.
