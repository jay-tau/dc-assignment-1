FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app/load_balancer/load_balancer.py /code/load_balancer.py

CMD ["python", "load_balancer.py"]
