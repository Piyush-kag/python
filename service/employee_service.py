from typing import Type

from sqlalchemy.orm import Session
from repository import employee_repository
from models import Employee, EmployeeDetails


def get_employee_service(db: Session, employee_id: int) -> Employee:
    try:
        employee = employee_repository.get_employee_by_id(db, employee_id)
        if not employee:
            raise ValueError(f"Employee with id {employee_id} not found")
        return employee
    except Exception as e:
        raise ValueError(f"Employee not found with id : {employee_id}")


def create_employee_service(db: Session, name: str, address: str, phone_number: str) -> (Employee, EmployeeDetails):
    try:
        employee = employee_repository.create_employee(db, name)
        employee_details = employee_repository.create_employee_details(db, employee.id, address, phone_number)
        return employee, employee_details
    except Exception as e:
        raise ValueError("An error occurred while creating the employee")


def update_employee_service(db: Session, employee_id: int, name: str = None, address: str = None,
                            phone_number: str = None) -> Employee:
    try:
        employee_details = employee_repository.get_employee_details_by_id(db, employee_id)
        if not employee_details:
            raise ValueError(f"Employee with id {employee_id} not found")

        if name:
            employee_repository.update_employee(db, employee_id, {'name': name})
        if address or phone_number:
            update_data = {}
            if address:
                update_data['address'] = address
            if phone_number:
                update_data['phone_number'] = phone_number
            employee_repository.update_employee_details(db, employee_id, update_data)

        return employee_repository.get_employee_by_id(db, employee_id)
    except Exception as e:
        raise ValueError("An error occurred while updating the employee")


def delete_employee_service(db: Session, employee_id: int):
    try:
        employee_repository.delete_employee_details(db, employee_id)
        employee_repository.delete_employee(db, employee_id)
    except Exception as e:
        raise ValueError("An error occurred while deleting the employee")
