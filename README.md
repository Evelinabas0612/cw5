# Курсовая 5. Работа с базами данных

## Платформа HeadHunter 

В рамках проекта необходимо получить данные о компаниях и вакансиях с сайта hh.ru, 
спроектировать таблицы в БД PostgreSQL и загрузить полученные данные в созданные таблицы.

Требования
Для запуска программы вам понадобится:
Python 3.6 или выше
Библиотеки Python: requests, psycopg2


Создание и загрузка данных в БД PostgreSQL
Для проекта необходимо создать базу данных.
Для создания таблиц в БД PostgreSQL используется Python-модуль psycopg2. 
Вы можете создать таблицы, выполнив скрипт CREATE TABLE из файла queries.sql в среде, поддерживающей SQL, или с помощью функции main.py, которая обращается к методу create_tables(self) класса DBManager в модуле dbmanager.py.

Методы для работы с вакансиями
Помимо прочего Класс DBManager содержит следующие методы:

get_companies_and_vacancies_count(): получает список всех компаний и количество вакансий у каждой компании.
get_all_vacancies(): получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
get_avg_salary(): получает среднюю зарплату по вакансиям.
get_vacancies_with_higher_salary(): получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
get_vacancies_with_keyword(): получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”.
Результаты, полученные с помощью данных методов, выводятся автоматически при запуске главной функции main.py

Откройте файл dbmanager.py, введите параметры подключения к вашей БД PostgreSQL Например: (dbname='postgres', user='user', password='password', host='localhost', port=5432)

Откройте файл main.py и запустите его. Введите запрашиваемые в коде ключевые слова для сужения поиска. Полученные данные о компаниях и вакансиях по будут сохранены в переменных companies и vacancies. Далее код создаст таблицы в вашей БД, загрузит полученные данные и выведет информацию, полученную с помощью методов работы с вакансиями класса DBManager, перечисленные в секции "Методы для работы с вакансиями".