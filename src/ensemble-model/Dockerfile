FROM custom-spark:latest

WORKDIR /app

COPY ensemble-model.py /app/
COPY --chmod=555 spark-submit-ensemble-model.sh /app/

CMD [ "/app/spark-submit-ensemble-model.sh" ]
