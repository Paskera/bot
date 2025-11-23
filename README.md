### Бот на закрытие третьего трудового семестра
### https://vk.com/club234144226

### Бот для прохождения тестов и получение статистики по пройденным тестам

### Установка
- git clone
- cd 

- poetry install

- Создайте .env по примеру .env.example
- Создайте api token в сообществе ВК и вставьте в VK_BOT_TOKEN

### Запуск
- poetry run dev
- python main.py

### Тесты
- Чтобы начать тест, нужно отсканировать qr code или перейти по ссылке с параметром ref в данном проекте (test1, test2, test3), чтобы при нажатии на кнопку начать тест активировался нужный тест
- Пример ссылок:
- https://vk.me/club234144226?ref=test1
- https://vk.me/club234144226?ref=test2
- https://vk.me/club234144226?ref=test3

- Команда /список выведет список всех участников прошедших тест

### Архитектура

\---bot
    |   .env
    |   .env.example
    |   .gitignore
    |   poetry.lock
    |   pyproject.toml
    |   README.md
    |
    +---src
    |   \---bot
    |       |   config.py
    |       |   main.py
    |       |   __init__.py
    |       |
    |       +---database
    |       |   |   base.py
    |       |   |   crud.py
    |       |   |   models.py
    |       |   |   session.py
    |       |   |   __init__.py
    |       |   |
    |       |
    |       +---tests
    |       |   |   tests.py
    |       |   |   __init__.py
    |       |   
    |       |   
    |       
    |
    \---tests
        |   __init__.py
