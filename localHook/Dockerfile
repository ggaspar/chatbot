FROM python:3
ADD . /code/localHook
WORKDIR /code/localHook
RUN pip install -r requirements.txt
CMD ["python", "-u", "server.py"]
EXPOSE 5044