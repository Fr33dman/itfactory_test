FROM python:3.10-alpine

RUN apk update
RUN apk add python3-dev  \
    libpq-dev  \
    libc-dev \
    musl-dev \
    libffi-dev \
    gcc
RUN pip install --upgrade pip wheel \
    && pip install psycopg2-binary

COPY ./ /var/app/
RUN pip install -r /var/app/requirements.txt

EXPOSE 8000
WORKDIR /var/app/

COPY entrypoint.sh /

RUN ["chmod", "+x", "/entrypoint.sh"]

CMD ["/entrypoint.sh"]