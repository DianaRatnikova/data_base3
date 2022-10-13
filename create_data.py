import csv
import random
from faker import Faker

# для фейковых платежей
from datetime import date
import random
# для записи в файл
import csv

fake = Faker('ru_RU')

# Создадим список, в котором каждый вложенный список - компания:
def fake_companies(num_rows=10):
    companies = []
    for _ in range(num_rows):
        companies.append(
            [fake.large_company(), fake.city_name(),
              fake.street_address(), fake.phone_number()]
        )
    return companies

# Функция, создающая по 10 сотрудников для каждой компании
def fake_employees(companies, num_rows=10):
    employees = []
    for company in companies:
        for _ in range(num_rows):
            employee = [fake.name(), fake.job(), fake.phone_number(),
                fake.free_email(), fake.date_of_birth(minimum_age=18, maximum_age=70)]
            employees.append(company + employee)
    return employees

# создание платежей за 12 месяцев:
def fake_payments(employees):
    payments = []
    for employee in employees:
        for month in range(1, 13):
            payment_date = date(2020, month, random.randint(10, 29))
            ammount = random.randint(20000, 200000)
            payment = [payment_date, ammount]
            payments.append(employee + payment)
    return payments


# записываем данные в csv-файл построчно:
def generate_data(payments):
    with open('payments.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        for payment in payments:
            writer.writerow(payment)


if __name__ == '__main__':
    companies = fake_companies()
    employees = fake_employees(companies)
    payments = fake_payments(employees)
    print(f"{len(payments) = }")
    generate_data(payments)
#    generate_data()