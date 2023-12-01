FROM python:3.9

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN chmod a+x /app/docker/*.sh
