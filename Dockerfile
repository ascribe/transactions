FROM python:2.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --upgrade pip

COPY . /usr/src/app

RUN pip install -e .[dev]

CMD ["py.test", "-v", "tests/"]
