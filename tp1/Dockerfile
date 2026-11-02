FROM eclipse-temurin:21-jdk
WORKDIR /app
COPY tp1/Associativity.java tp1/BankingProblem.java ./tp1/
COPY tp1/run.sh ./tp1/

RUN javac tp1/Associativity.java tp1/BankingProblem.java
RUN chmod +x /app/tp1/run.sh
CMD ["/app/tp1/run.sh"]
