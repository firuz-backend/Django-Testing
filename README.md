eal# 📝 Django Testing Project

Проект содержит набор тестов для двух Django-приложений: **YaNote** (заметки) и **YaNews** (новостной сайт).  
В проекте реализовано тестирование с использованием двух фреймворков: **unittest** и **pytest**.

---

## 📂 Структура проекта

    Dev
        └── django_testing 
        ├── ya_news/                # Проект YaNews 
        │   ├── news/               # Приложение news 
        │   │   ├── pytest_tests/   # Тесты pytest 
        │   │   └── ... 
        │   ├── templates/ 
        │   └── manage.py 
        │ 
        ├── ya_note/                # Проект YaNote 
        │   ├── notes/              # Приложение notes 
        │   │   ├── tests/          # Тесты unittest 
        │   │   └── ... 
        │   ├── templates/ 
        │   └── manage.py 
        │ 
        └── requirements.txt        # Зависимости проекта

---

## 📊 Тестовое покрытие

### YaNote (unittest)
- **test_routes.py**: тестирование маршрутов, доступности страниц, авторизации и прав доступа.
- **test_content.py**: проверка корректности данных в шаблонах, изоляции заметок и работы форм.
- **test_logic.py**: тестирование создания, редактирования и удаления заметок, уникальности slug.

### YaNews (pytest)
- **test_routes.py**: тестирование доступности страниц новостей, авторизации и прав доступа к комментариям.
- **test_content.py**: проверка отображения контента на страницах.
- **test_logic.py**: тестирование добавления и удаления комментариев.

---

## 🛠️ Технологии

- Python 3.9+
- Django
- unittest
- pytest

---

## 📦 Установка

1. Клонируйте репозиторий:
   ```bash
   git clone git@github.com:ваш-аккаунт/django_testing.git
   cd django_testing

Установите зависимости:
pip install -r requirements.txt

Выполните миграции:
python manage.py migrate

🚀 Запуск тестов

Для YaNote (unittest)
python manage.py test

Для YaNews (pytest)
pytest

📑 Лицензия
Проект создан в учебных целях.