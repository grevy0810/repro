FROM eclipse-temurin:21-jdk
WORKDIR /app
copy Associativity.java BankingProblem.java run.sh ./

RUN javac Associativity.java BankingProblem.java
RUN chmod +x /app/run.sh
CMD ["/app/run.sh"]