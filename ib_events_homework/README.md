# Анализ событий информационной безопасности

Учебный проект: загрузка событий ИБ из JSON в `pandas.DataFrame`, подсчёт типов событий по полю `signature` и построение графика с помощью Seaborn/Matplotlib.

## Состав проекта

- `events.json` — учебный набор синтетических событий ИБ в формате JSON.
- `analyze_events.py` — код загрузки данных, анализа `signature` и построения графика.
- `requirements.txt` — необходимые Python-библиотеки.
- `output/` — создаётся при запуске; содержит CSV с подсчётами и PNG-график.

## Требования

- Python 3.10 или новее.
- Pandas, Matplotlib и Seaborn (устанавливаются из `requirements.txt`).

## Запуск в Kali Linux

Из каталога проекта выполните:

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python analyze_events.py
```

После успешного запуска:

- в терминале будет выведено количество событий каждого типа;
- `output/signature_counts.csv` будет содержать сводную таблицу;
- `output/signature_distribution.png` будет содержать график распределения.

Если JSON-файл находится в другом месте, можно передать путь явно:

```bash
python analyze_events.py --input /путь/к/events.json
```

## Как устроен анализ

1. `pandas.read_json(..., orient="records")` загружает JSON-массив объектов в DataFrame.
2. Скрипт проверяет наличие обязательного столбца `signature` и очищает пустые значения.
3. `value_counts()` подсчитывает количество событий каждого типа.
4. `seaborn.barplot()` строит горизонтальную столбчатую диаграмму; `matplotlib` сохраняет её в PNG.

## Примечание о данных

Данные в `events.json` сгенерированы для учебной демонстрации. IP-адреса взяты из диапазонов, зарезервированных для документации и примеров; реальные системы и пользователи не описываются.

Если преподаватель предоставил свой файл `events.json`, замените учебный файл предоставленным, не меняя имя, либо укажите его путь через аргумент `--input`.
