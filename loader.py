import csv
from db import db_session
from models import Company, Employee, Payment
import time


def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['company',  'city', 'address', 'phone_company', 'name', 'job',
                  'phone_person', 'email', 'date_of_birth', 'payment_date', 'ammount']
        reader = csv.DictReader(f, fields, delimiter=';')
        payments_data = []
        for row in reader:
            payments_data.append(row)
        return payments_data


def save_companies(all_data):
    processed = []
    companies_unique = []
    for row in all_data:
        if row['company'] not in processed:
            company = {'name': row['company'], 'city': row['city'],
                        'address': row['address'], 'phone': row['phone_company'],
            }
            companies_unique.append(company)
            processed.append(company['name'])
# return_defaults=True говорит bulk_insert_mappings, 
# что когда база присвоит компаниям id, их нужно добавить в companies_unique.
    db_session.bulk_insert_mappings(Company, companies_unique, return_defaults=True)
    db_session.commit()
    return companies_unique


# перебирает список уникальных компаний и, 
# когда находит нужное название, возвращает идентификатор:
def get_company_id(company_name, companies_unique):
    for row in companies_unique:
        if row['name'] == company_name:
            return row['id']
    return None


def save_employees(all_data, companies):
    processed = []
    employees_unique = []
    for row in all_data:
        if row['phone_person'] not in processed:
            employee = {'name': row['name'], 'job': row['job'], 'email': row['email'],
            'phone': row['phone_person'], 'date_of_birth': row['date_of_birth']
            }
            employee['company_id'] = get_company_id(row['company'], companies)
            employees_unique.append(employee)
            processed.append(row['phone_person'])
    db_session.bulk_insert_mappings(Employee, employees_unique, return_defaults=True)
    db_session.commit()
    return employees_unique


def get_employee_id(phone, employees_unique):
    for row in employees_unique:
        if row['phone'] == phone:
            return row['id']
    return None


def make_employee_id_dict(phone, employees_unique):
    employee_id_dict ={}
    for row in employees_unique:
        if row['phone'] == phone:
            employee_id_dict[row['phone']] = row['id']
            return row['id']
    return employee_id_dict


def save_payments(all_data, employees):
    payments = []
    for row in all_data:
        payment = {'payment_date': row['payment_date'], 'ammount': row['ammount'],
                    'employee_id': get_employee_id(row['phone_person'], employees)
        }
        payments.append(payment)
    db_session.bulk_insert_mappings(Payment, payments)
    db_session.commit()

if __name__ == '__main__':
    data = read_csv('payments.csv')
    companies = save_companies(data)
    employees = save_employees(data, companies)
    print(employees)
    save_payments(data, employees)