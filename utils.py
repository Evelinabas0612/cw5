import psycopg2
import requests


class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(host='localhost', database='hh', user='postgres', password='root')
        self.conn.autocommit = True
        self.employer_url = 'https://api.hh.ru/employers?only_with_vacancies=true'

    def get_employers_data(self, keyword) -> list[dict]:
        """Выборка работодателей """
        params = {'text': keyword.lower()}
        response = requests.get(self.employer_url, params=params).json()['items']
        return response

    def create_tables(self):
        """Создание таблицы Компания и Bакансия"""

        with self.conn.cursor() as cur:
            cur.execute("""
                            DROP TABLE IF EXISTS vacancies;
                            DROP TABLE IF EXISTS companies;
                        """)
            cur.execute("""
                       CREATE TABLE companies (
                           id SERIAL PRIMARY KEY,
                           name VARCHAR(100) NOT NULL,
                           city VARCHAR(100) NOT NULL,
                           url VARCHAR(100) NOT NULL
                       );
                       """)
            cur.execute("""
                       CREATE TABLE vacancies (
                           id SERIAL PRIMARY KEY,
                           name VARCHAR(100) NOT NULL,
                           companies_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
                           salary_min REAL,
                           salary_max REAL,
                           snippet VARCHAR(500),
                           url VARCHAR(100) NOT NULL
                       );                
                   """)

    def insert_tables(self, company, vacancies):
        """Заполнение таблиц Компания и Bакансия"""
        with self.conn.cursor() as cur:
            cur.execute("""
            INSERT INTO companies (id, name, city, url)
            VALUES (%s, %s, %s, %s)""",
                        (int(company['id']), company['name'], company['area']['name'],
                         company['alternate_url'])
                        )

            for item in vacancies['items']:
                try:
                    if item['salary'] is None:
                        salary_min = 0
                        salary_max = 0
                    else:
                        salary_min = item['salary']['from']
                        salary_max = item['salary']['to']
                    if salary_min is None:
                        salary_min = 0
                    elif salary_max is None:
                        salary_max = 0
                except TypeError as e:
                    f"Неверный формат{e}"
                cur.execute(f"""
                        INSERT INTO vacancies (name, companies_id, salary_min, salary_max, snippet, url)
                        VALUES (%s, %s, %s, %s, %s, %s)""",
                            (item['name'], item['employer']['id'], salary_min, salary_max,
                             item['snippet']['requirement'], item['alternate_url'])
                            )


    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""

        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT companies.name, COUNT(*)
                FROM companies
                INNER JOIN vacancies ON vacancies.companies_id = companies.id
                GROUP BY companies.name;
            """)
            return cur.fetchall()


    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и
    зарплаты и ссылки на вакансию."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT companies.name, vacancies.name, vacancies.salary_min, vacancies.salary_max, vacancies.url
                FROM vacancies INNER JOIN companies ON vacancies.companies_id = companies.id;
            """)
            return cur.fetchall()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""

        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT vacancies.name, AVG((vacancies.salary_min + vacancies.salary_max)/2) as salary
                FROM vacancies
                GROUP BY vacancies.name
                ORDER BY salary DESC
            """)
            return cur.fetchall()

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""

        with self.conn.cursor() as cur:
            cur.execute(f"""
                SELECT vacancies.name, vacancies.salary_min, url
                FROM vacancies
                WHERE vacancies.salary_min > (SELECT AVG((vacancies.salary_min + vacancies.salary_max) / 2) FROM vacancies)
                ORDER BY salary_min DESC;
            """)
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например 'python'"""

        with self.conn.cursor() as cur:
            cur.execute(f"""
                SELECT *
                FROM vacancies WHERE vacancies.name LIKE '%{keyword}%';
            """)
            return cur.fetchall()
