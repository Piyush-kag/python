from fastapi import FastAPI
from controller import (post_controller, user_controller, student_controller, course_controller, employee_controller)
from database import create_db
from exception.exception import CustomException, custom_exception_handler, generic_exception_handler
from inheritance.oops import Cappuccino, Coffee, Espresso, Latte

create_db()

app = FastAPI()

app.add_exception_handler(CustomException, custom_exception_handler )
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(user_controller.router)
app.include_router(post_controller.router)
app.include_router(student_controller.router)
app.include_router(course_controller.router)
app.include_router(employee_controller.router)
# app.include_router(employee_details_controller.router)

# x = Coffee("Normal Coffee", 3.00)
# x.make_coffee()
# x.serve_coffee()

# x = Cappuccino(3.50)
# x.make_coffee()
# x.serve_coffee()

# x = Latte(4.00)
# x.add_milk()
# x.make_coffee()
# x.serve_coffee()
#
# x = Espresso(5.00)
# x.make_coffee()
# x.serve_coffee()
