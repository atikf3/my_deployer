FROM python:3.8-alpine
LABEL authors="AMT <dev@talamona.com>"

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["app.py"]