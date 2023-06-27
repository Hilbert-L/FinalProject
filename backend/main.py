import uvicorn
from fastapi import FastAPI, Depends, status, HTTPException, Header, Body
from decouple import config
from routers.GeneralRouters import GeneralRouter
from routers.ProtectedEndpoints import ProtectedRouter
from routers.UserRouters import UserRouter
from routers.CarSpaceRouters import CarSpaceRouter
from routers.AdminRouters import AdminRouter
from routers.SearchRouters import SearchRouter
from fastapi.middleware.cors import CORSMiddleware

import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(title=config("projectName"))

origins = [
    "http://localhost:5173",  # Allow requests from this origin
    # Add other origins as needed
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(GeneralRouter)
app.include_router(ProtectedRouter)
app.include_router(UserRouter)
app.include_router(CarSpaceRouter)
app.include_router(SearchRouter)
app.include_router(AdminRouter)

# Can do this instead of CLI (python3 main.py) in which it will run on local host 9000 
# instead of port 8000 (which is entered via uvicorn main:app --reload)
if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port = '9000')
