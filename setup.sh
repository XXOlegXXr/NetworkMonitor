#!/bin/bash

echo "Налаштування Network Monitor "

if ! command -v python3 &> /dev/null
then
    echo "Помилка: Python3 не знайдено. Встановіть його."
    exit 1
fi
echo "Python 3 знайдено."

if [ ! -d "venv" ]; then
    echo "Створюємо віртуальне середовище (venv)..."
    python3 -m venv venv
else
    echo "Віртуальне середовище вже існує."
fi

echo "Активуємо віртуальне середовище..."
source venv/bin/activate

echo "Оновлюємо pip..."
pip install --upgrade pip

if [ -f "requirements.txt" ]; then
    echo "Встановлюємо залежності з requirements.txt..."
    pip install -r requirements.txt
else
    echo "Файл requirements.txt не знайдено. Якщо у вас є зовнішні бібліотеки, створіть цей файл."
fi


echo "Налаштування успішно завершено!"
echo "Щоб запустити програму, виконайте наступні команди:"
echo "source venv/bin/activate"
echo "python src/main.py"
