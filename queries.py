from db import db_session
from models import Company, Employee
import time

# найти компанию по названию и вывести для нее все сотрудников
def employees_by_company(company_name):
    company = Company.query.filter(Company.name == company_name).first()
    employee_list = []
    if company:
        for employee in Employee.query.filter(Employee.company_id == company.id):
            employee_list.append(f"{company.name} - сотрудник {employee.name}")
    return employee_list

# вариант с использованием join:
def employees_by_company_joined(company_name):
    employee_list = []
    query = db_session.query(Employee, Company).join(
        Company, Employee.company_id == Company.id
    ).filter(Company.name == company_name)

    for employee, company in query:
        employee_list.append(f"{company.name} - сотрудник {employee.name}")

    return employee_list


def employee_by_company_relation(company_name):
    company = Company.query.filter(Company.name == company_name).first()
    employee_list = []
    if company:
        for employee in company.employees:
            employee_list.append(f"{company.name} - сотрудник {employee.name}")

    return employee_list

if __name__ == '__main__':
    start = time.perf_counter()
    for _ in range(100):
        employees_by_company("Арктикгаз")
    print(f'employees_by_company {time.perf_counter() - start}')
    start = time.perf_counter()
    for _ in range(100):
        employees_by_company_joined("Арктикгаз")
    print(f'employees_by_company_joined {time.perf_counter() - start}')
    
    start = time.perf_counter()
    for _ in range(100):
        employee_by_company_relation("Арктикгаз")
    print(f'employee_by_company_relation {time.perf_counter() - start}')