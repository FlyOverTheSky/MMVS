# Тестовое задание для MMVS
Тестовый сервис для хранения и изменения разрешения.

## Технологии
- Python
- DRF
- ADRF

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
