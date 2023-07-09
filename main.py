from utils import DBManager
import requests


def get_request(url):
    """Получение данных"""
    try:
        data = requests.get(url)
        return data.json()
    except Exception as e:
        return f'Проблема с получением данных: {e}'


def main():
    db = DBManager()
    db.create_tables()

    employees = [1410365, 581458, 5657254, 1455, 1035722, 12550, 15478, 5694, 1740, 1122462]

    for employer in employees:
        company = get_request(f'https://api.hh.ru/employers/{employer}')
        vacancies = get_request(f'https://api.hh.ru/vacancies?employer_id={employer}&per_page=50')
        db.insert_tables(company, vacancies)

    while True:
        rows = []
        print("Выберите команду, какой запрос выполнить:\n")
        command = input(
            '1 - Cписок всех компаний и количество вакансий у каждой компании;\n'
            '2 - Cписок всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию";\n'
            '3 - Средняя зарплата по вакансиям;\n'
            '4 - Cписок всех вакансий, у которых зарплата выше средней по всем вакансиям;\n'
            '5 - Cписок всех вакансий, в названии которых содержатся переданные в метод слова, например \'python\';\n'
            '6 - Выход;\n')
        if command == '6':
            print("До свидания!")
            break
        elif command == '1':
            print("Cписок всех компаний и количество вакансий у каждой компании")
            rows = db.get_companies_and_vacancies_count()
        elif command == '2':
            print(
                "Cписок всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию")
            rows = db.get_all_vacancies()
        elif command == '3':
            print("""Средняя зарплата по вакансиям""")
            rows = db.get_avg_salary()
        elif command == '4':
            print("Cписок всех вакансий, у которых зарплата выше средней по всем вакансиям")
            rows = db.get_vacancies_with_higher_salary()
        elif command == '5':
            print(
                "Cписок всех вакансий, в названии которых содержатся переданные в метод слова, например 'python'")
            keyword = input("Введите слово, по-которому будет осуществлен поиск: ")
            rows = db.get_vacancies_with_keyword(keyword.upper())
        else:
            print("Выберите команду из списка:")

        for row in rows:
            print(row)
        print("\n")


if __name__ == '__main__':
    main()
