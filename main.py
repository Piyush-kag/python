from fastapi import Depends, FastAPI
from controller import post_controller, user_controller
from database import createDb
import logging
from exception.exception import CustomException, custom_exception_handler, generic_exception_handler

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

createDb()


app = FastAPI()

app.add_exception_handler(CustomException, custom_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(post_controller.router)
app.include_router(user_controller.router)
