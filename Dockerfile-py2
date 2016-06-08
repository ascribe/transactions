FROM python:2.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip install --no-cache-dir --upgrade pip

COPY . /usr/src/app

RUN pip install --no-cache-dir --process-dependency-links -e .[dev]

CMD ["py.test", "-v", "tests/"]
