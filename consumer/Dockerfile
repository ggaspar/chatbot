FROM python:3
ADD . /code/consumer
WORKDIR /code/consumer
ENV PYTHONUNBUFFERED 0
RUN pip install -r requirements.txt
CMD ["python", "-u", "consumer.py"]
