from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from service import employee_service
from schemas import EmployeeCreate, Employee
from logging_config import logging_config
from loguru import logger

router = APIRouter()


@router.get("/employees/{employee_id}", response_model=Employee, tags=["One-to-One/Employees"])
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Getting employee by id : {employee_id}")
        return employee_service.get_employee_service(db, employee_id)
    except ValueError as e:
        logger.error(f"Got a value error try entering according to suggested. : {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception("Exception occurred while creating an employee.")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/employees", response_model=Employee, tags=["One-to-One/Employees"])
def create_employee(employee: EmployeeCreate, address: str, phone_number: str, db: Session = Depends(get_db)):
    try:
        logger.info("Creating employee..")
        employee, employee_details = employee_service.create_employee_service(db, employee.name, address, phone_number)
        return employee
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/employees/{employee_id}", response_model=Employee, tags=["One-to-One/Employees"])
def update_employee(employee_id: int, name: str = None, address: str = None, phone_number: str = None,
                    db: Session = Depends(get_db)):
    try:
        logger.info("Updating employee..")
        return employee_service.update_employee_service(db, employee_id, name, address, phone_number)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/employees/{employee_id}", tags=["One-to-One/Employees"])
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    try:
        employee_service.delete_employee_service(db, employee_id)
        return {"detail": "Employee deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
