# Сайт корейского языка

Мой pet-проект - это платформа для изучения корейского языка, прохождение онлайн курсов.

### Cтек технологий:
* Python
* Django
* PostgreSQL
* Docker
* Celery
* Redis

# Установка

### Скопируйте проект.
  
```console
git clone https://github.com/NaiNaniNai/korean-site.git
```

### Настройте проект.
 * Создайте .env файл
 * Установите переменные в этом файле:
    * `DB_HOST=` <- Хост для БД
    * `DB_NAME=` <- Название БД
    * `DB_USER=` <- Имя пользователя БД
    * `DB_PASSWORD` <- Пароль пользователя БД
    * `DEBUG=` <- Дебаг режим
    * `SECRET_KEY=` <- Секретный ключ проекта
   Если вы хотите использовать другую базу данных воспользуйтесь [официальной документацией Django](https://docs.djangoproject.com/en/5.0/ref/settings/#databases).
  * Выполните команду по сборке образа:
    ```console
    docker-compose build
    ```
  * Добавьте супер пользователя (администратора) Django, выполнив следующую команду:
    ```console
    docker-compose run --rm web sh -c "poetry run python manage.py createsuperuser"
    ```
### Запустите проект
  * Используйте команду:
    ```console
    docker-compose up
    ```
