**FarmCalculator**

Используемые фреймворки:
-  Bootstrap
-  Flask

Необходимые библиотеки находятся в requriments.txt

Запуск:
1. Склонировать репозиторий себе
2. Создать виртуальное окружение
3. Установить зависимости "python -m pip install -r requriments.txt"
4. Запуск "python run.py"


Создание БД:
1. Python bd_reset.py (Удаление существующей бд и создание новой)

Создание пользователя (тестовый режим):
1. После запуска пройти по ссылке 127.0.0.1:5000/register и зарегистрировать пользователя.
2. Войти


FarmCalculator - пакет со всеми модулями.
run.py - исполняемый файл
В пакете FarmCalculator находятся:
- routes.py
  Отвечает за обработку всех ссылок.
- models.py
  Отвечает за репрезентацию сущностей базы данных в коде питона
- forms.py
  Отвечает за обработку форм, на основе которых генерируется html-формы для пользователей
- \__init__.py
  Отвечает за настройку фреймворка
