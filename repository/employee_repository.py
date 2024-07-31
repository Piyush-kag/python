from typing import Optional, Type

from sqlalchemy.orm import Session, joinedload

from models import Employee, EmployeeDetails


def get_employee_by_id(db: Session, employee_id: int) -> Employee:
    return db.query(Employee).options(joinedload(Employee.details)).filter(Employee.id == employee_id).first()


def create_employee(db: Session, name: str) -> Employee:
    employee = Employee(name=name)
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def update_employee(db: Session, employee_id: int, details: dict):
    db.query(Employee).filter(Employee.id == employee_id).update(details)
    db.commit()


def delete_employee(db: Session, employee_id: int):
    db.query(Employee).filter(Employee.id == employee_id).delete()
    db.commit()


def get_employee_details_by_id(db: Session, employee_id: int) -> Optional[Type[EmployeeDetails]]:
    return db.query(EmployeeDetails).filter(EmployeeDetails.employee_id == employee_id).first()


def create_employee_details(db: Session, employee_id: int, address: str, phone_number: str) -> EmployeeDetails:
    employee_details = EmployeeDetails(employee_id=employee_id, address=address, phone_number=phone_number)
    db.add(employee_details)
    db.commit()
    db.refresh(employee_details)
    return employee_details


def update_employee_details(db: Session, employee_id: int, details: dict):
    db.query(EmployeeDetails).filter(EmployeeDetails.employee_id == employee_id).update(details)
    db.commit()


def delete_employee_details(db: Session, employee_id: int):
    db.query(EmployeeDetails).filter(EmployeeDetails.employee_id == employee_id).delete()
    db.commit()
