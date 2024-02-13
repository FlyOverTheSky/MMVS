# Тестовое задание для MMVS
Тестовый сервис для хранения и изменения разрешения видео.

## Технологии
- Python
- DRF
- ADRF
- PostgreSQL

## Использование

```
git clone git@github.com:FlyOverTheSky/MMVS.git
```

```
python -m venv venv

sourve venv/Scripts/activate

pip install -r requirements.txt

python api/backend/manage.py makemigrations

python api/backend/manage.py migrate

python manage.py runserver
```

### Документация
- /swagger
- /redoc

### Выполненые задачи
- Автодокументация в swagger и redoc формате
- Логирование инструментами Django
