FROM python:3.10

WORKDIR /app/
COPY . /app/

RUN pip install --upgrade pip --user &&  \
  pip install "poetry==1.7.1" &&  \
  poetry config virtualenvs.create false
RUN poetry install

# RUN poetry run python manage.py collectstatic --noinput
# RUN poetry run python manage.py compilemessages

RUN apt-get -qq update && \
  apt-get -qq install gettext

EXPOSE 5000
