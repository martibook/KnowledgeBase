FROM python:3

EXPOSE 5000

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

CMD ["sh", "-c", "export MODE=docker && export FLASK_APP=project.app.py && export export FLASK_DEBUG=1 && flask run --host=0.0.0.0"]