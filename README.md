# InfoSearch
Репозиторий для учебного проекта поисковой системы

- НЕОБХОДИМ Python версии 3.6.x

## Чтобы запустить проект:
- Клонируйте репозиторий
- Откройте терминал
- Переместитесь в директорию проекта
- Установите все необходимые пакеты ```pip install -r requirements.txt```
- Примените миграции ```python manage.py migrate```
- Запустите ```python manage.py runserver```
- Откройте ```127.0.0.1:8000``` в браузере

## Работа с проектом
### "Служебная":
- Есть возможность сгенерировать список из N случайных статей из википедии, а также выгрузить или удалить их
- Чтобы воспользоваться булевым поиском, необходимо сгенерировать инвертированные индексы для загруженных статей (требуются сами статьи)
- Чтобы воспользоваться векторным поиском, необходимо сгенерировать TF-IDF индексы (требуется сгенерированный файл инвертированных индексов)

### Поиск:
Как только были загружены все статьи и сгенерированы индексы, можно пользоваться системами булевого и векторного поиска. Результаты отобразятся в виде ссылок на оригиналы статей, а правила булевого поиска описаны на самой странице

## Файлы
- Файлы загруженных статей по-умолчанию находятся в папке ```media/downloads/```, также сами статьи можно посмотреть по ссылке на странице "Служебная"
- Файлы TF-IDF и инвертированных индексов по-умолчанию находятся в папке ```static/```
