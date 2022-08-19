FROM python:3.8
RUN ls
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 5000
CMD ["python", "todo.py"]
