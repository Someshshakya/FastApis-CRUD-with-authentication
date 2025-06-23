import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging

#set up logger 
logger = logging.getLogger("request_logger")
logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(levelname)s -%(message)s")

# async def log_request(request:Request,call_next):
#     start_time = time.time()
#     #read the body of the request (cloneable)
#     body = await request.body()
#     logger.info(f">> {request.method} {request.url.path} | Body: {body.decode('utf-8') if body else '{}'} ")
#     response = await call_next(request)

#     process_time = time.time() - start_time
#     logger.info(f"<< {request.method} {request.url.path} | Status: {response.status_code} | Time: {process_time:.4f}s")
#     return response

class LoggingMIddleware(BaseHTTPMiddleware):
    async def dispatch(self,request:Request, call_next):
        start_time = time.time()
    #read the body of the request (cloneable)
        body = await request.body()
        logger.info(f">> {request.method} {request.url.path} | Body: {body.decode('utf-8') if body else '{}'} ")
        response = await call_next(request)

        process_time = time.time() - start_time
        logger.info(f"<< {request.method} {request.url.path} | Status: {response.status_code} | Time: {process_time:.4f}s")
        return response
    