# Система генерации ваучеров для контрагентов сети КАРО

Веб-приложение позволяет сгенерировать pdf-версию ваучера на основе системы VISTA

## Как запустить

- Скачайте код
- Создайте виртуальное окружение  
из Bash  
```  
py -3.9 -m venv env  
source env/Scripts/activate  
```  

- Установите зависимости
```
python -m pip install -U pip
pip install -r requirements.txt
```

- Запустите сервер
```
uvicorn voucher_app.asgi:application --reload
```

- Перейдите на сайт 
```
http://127.0.0.1:8000/
```

```
docker compose exec -it admin_site bash
python manage.py compilemessages
python manage.py migrate
python manage.py collectstatic
```