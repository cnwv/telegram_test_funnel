Как запустить:

1)Создать .env file

2)Создать venv и установить requirements.txt

3)Внутри машины запустить две команды, чтобы авторизироваться в Telegram API:
```python
alembic upgrade head
python app.py
PYTHONPATH=$(pwd) python src/funnel.py
```
4)После появления баз данных сессий можно запускать через команду
```shell
docker-compose up -d
```
