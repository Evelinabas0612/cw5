 """Удаление и Создание таблиц Компания и Bакансия"""


DROP TABLE IF EXISTS vacancies;
DROP TABLE IF EXISTS companies;

CREATE TABLE companies (
   id SERIAL PRIMARY KEY,
   name VARCHAR(100) NOT NULL,
   city VARCHAR(100) NOT NULL,
   url VARCHAR(100) NOT NULL
   );

CREATE TABLE vacancies (
   id SERIAL PRIMARY KEY,
   name VARCHAR(100) NOT NULL,
   companies_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
   salary_min REAL,
   salary_max REAL,
   snippet VARCHAR(500),
   url VARCHAR(100) NOT NULL
);


 """Заполнение таблиц Компания и Bакансия"""

INSERT INTO companies (id, name, city, url)
VALUES (%s, %s, %s, %s)""",
            (int(company['id']), company['name'], company['area']['name'],
             company['alternate_url'])
            );


INSERT INTO vacancies (name, companies_id, salary_min, salary_max, snippet, url)
VALUES (%s, %s, %s, %s, %s, %s)""",
    (item['name'], item['employer']['id'], salary_min, salary_max,
     item['snippet']['requirement'], item['alternate_url'])
    );



"""Получает список всех компаний и количество вакансий у каждой компании"""


SELECT companies.name, COUNT(*)
FROM companies
INNER JOIN vacancies ON vacancies.companies_id = companies.id
GROUP BY companies.name;

"""Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""

SELECT companies.name, vacancies.name, vacancies.salary_min, vacancies.salary_max, vacancies.url
FROM vacancies INNER JOIN companies ON vacancies.companies_id = companies.id;


"""Получает среднюю зарплату по вакансиям."""

SELECT vacancies.name, AVG((vacancies.salary_min + vacancies.salary_max)/2) as salary
FROM vacancies
GROUP BY vacancies.name
ORDER BY salary DESC;


"""Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""


SELECT vacancies.name, vacancies.salary_min, url
FROM vacancies
WHERE vacancies.salary_min > (SELECT AVG((vacancies.salary_min + vacancies.salary_max) / 2) FROM vacancies)
ORDER BY salary_min DESC;


"""Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например 'python'"""


SELECT *
FROM vacancies WHERE vacancies.name LIKE '%{keyword}%';
