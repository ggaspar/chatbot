FROM python:3
ADD . /code/facebookHook
WORKDIR /code/facebookHook
RUN pip install -r requirements.txt
CMD ["python", "-u", "hook.py"]
EXPOSE 5013