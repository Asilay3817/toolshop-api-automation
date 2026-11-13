## Подготовка
1. Установка Homebrew 
>/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
2. Установка python/allure/openjdk
>brew install python
>brew install allure
>brew install openjdk
3. Создание виртуального окружения в папке проекта
>python3 -m venv .venv
4. Активация виртуального окружения
>source .venv/bin/activate
5. Установка зависимостей
>pip install -r requirements.txt


## Запуск
- pytest - запуск тестов и генерация allure-results
- allure serve allure-results - открытие отчета

## Выборочный запуск 
- pytest -m smoke
- pytest -m regress