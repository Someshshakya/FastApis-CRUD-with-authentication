from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse


from routes.product import router as ProductRouter
from routes.customer import router as CustomerRouter
from routes.uploadFile import router as FileUpload
from middlewares.logging import LoggingMIddleware


from exceptions import NotFoundException, BadRequestException, DatabaseException



app = FastAPI()

## adding logging middleware 
app.add_middleware(LoggingMIddleware)
app.include_router(ProductRouter,tags=["Products"],prefix="/product")
app.include_router(CustomerRouter,tags=["Customer"])
app.include_router(FileUpload,tags=["FileUpload"])
# Exception handling 
@app.exception_handler(NotFoundException)
async def not_found_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=404,
        content={"success": False, "detail": exc.detail, "code": 404}
    )

@app.exception_handler(BadRequestException)
async def bad_request_handler(request: Request, exc: BadRequestException):
    return JSONResponse(
        status_code=400,
        content={"success": False, "detail": exc.detail, "code": 400}
    )

@app.exception_handler(DatabaseException)
async def db_error_handler(request: Request, exc: DatabaseException):
    return JSONResponse(
        status_code=500,
        content={"success": False, "detail": exc.detail, "code": 500}
    )

@app.get("/")
def read_root():
    return ({"message":"this is the home route here."})