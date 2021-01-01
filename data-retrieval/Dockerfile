FROM python:3.7

COPY . /app/

WORKDIR /app/twsapi_macunix.976.01/IBJts/source/pythonclient
RUN python3 setup.py bdist_wheel
RUN python3 -m pip install --user --upgrade dist/ibapi-9.76.1-py3-none-any.whl

WORKDIR /app/
RUN pip3 install pandas sqlalchemy psycopg2-binary celery
RUN export DATABASE_URL=postgresql://
# CMD echo DATABASE_URL is $DATABASE_URL
# CMD echo "$PWD"
ENTRYPOINT celery -A tasks worker --loglevel=info