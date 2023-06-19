import uvicorn
from fastapi import FastAPI, Depends, status, HTTPException, Header, Body
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from typing import Optional, List
from models.Authentication import UserRegistrationSchema, UserSchema, LoginSchema, LogoutSchema
from models.UpdateUserInfo import UpdatePassword, UpdateEmail, UpdateName, UpdateProfilePicture
from models.CreateCarSpace import CarSpaceReview, CarSpaceSchema, CreateCarSpaceSchema
from models.UpdateCarSpace import UpdateCarSpaceAddress, UpdateCarSpaceDimensions, UpdateCarSpacePrice
from wrappers.wrappers import check_token
from passlib.context import CryptContext
import jwt 
from decouple import config
from jwt import PyJWTError
from datetime import datetime


# Next steps
# Finish endpoints
# Connect to mongodb
# Write a script to clear from db
# Write unit tests with pymongo
# Create the frontend


# GET  - read from table
# POST - create in table
# PUT - update from table
# DELETE - delete from table

# This is in the .env file, it is generate through secrets.token_hex(16)
JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

# This is for mocking, we will connect to MongoDB via pymongo at a later stage
users_db : List[UserSchema] = []
admins_db : List[UserSchema] = []
carspace_db : List[CarSpaceSchema] = []
carspace_reviews : List[CarSpaceReview]= []

app = FastAPI()
security = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Password hashing context
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

# Helper function to generate JWT token
def generate_token(username: str):
    payload = {"username": username}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

# Helper function to verify JWT token 
# def verify_token(token: Annotated[str, Header(...)]):
def verify_token(token: str = Header(...)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithm=JWT_ALGORITHM)
        username = payload.get("username")
        user = next((u for u in users_db if u.username == username), None)
        if user and user.isloggedin:
            return username
        return None
    
    except PyJWTError:
        return None
    

@app.get("/users", tags=["Information"])
def get_users():
    return {"users": users_db}

@app.get("/admins", tags=["Information"])
def get_admins():
    return {"admins": admins_db}

@app.get("/carspace", tags=["Information"])
def get_car_spaces():
    return {"car_spaces": carspace_db}

@app.get("/carspacereviews", tags=["Information"])
def get_car_space_reviews():
    return {"carspace_reviews": carspace_reviews}


# Example route that requires authentication
@app.get("/protected", tags=["Protected Endpoint Examples"])
@check_token
def protected_route(token: str = Depends(verify_token)):
    # if not token:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    return {"Message": "This is a protected route"}


@app.post("/getuserfromtoken", tags=["Protected Endpoint Examples"])
@check_token
def get_user_from_token(token: str =Depends(verify_token), tags=["Dependency"]):
    username = verify_token(token)
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"access_token": token, "username": username}

# Everything here is an example for our project
@app.post("/user/auth/register", tags=["User Authentication"])
def register(userRegistrationSchema: UserRegistrationSchema): 
    # Check to see if username already exists
    if any(u.username == userRegistrationSchema.username for u in users_db):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
        
    # Hash the password
    hashed_password = pwd_context.hash(userRegistrationSchema.password)

    # Create a new user instance 
    new_user = UserSchema(
        userId=len(users_db), 
        firstname=userRegistrationSchema.firstname,
        lastname=userRegistrationSchema.lastname,
        username=userRegistrationSchema.lastname,
        email=userRegistrationSchema.email,
        password=hashed_password,
        phonenumber=userRegistrationSchema.phonenumber,
        profilepicture=userRegistrationSchema.profilepicture,
        isloggedin=False,
        DateCreated = datetime.now(),
        Reviews=[]
    )

    # Save the user to the database
    users_db.append(new_user)
    token = generate_token(new_user.username)
    return {"message": "User Registered Successfully", "token": token}

@app.post("/user/auth/login", tags=["User Authentication"])
def login(UserLogin: LoginSchema): 
    # Find the user by username
    stored_user : UserSchema = next((u for u in users_db if UserLogin.username == u.username), None)

    # Check if the user exists
    if stored_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user name or password")

    # Verify the password
    if not pwd_context.verify(UserLogin.password, stored_user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user name or password")
    
    if stored_user.isloggedin:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User is already logged in")

    stored_user.isloggedin = True

    # Generate and return a JWT token
    token = generate_token(UserLogin.username)
    return {"message": "User Login Successfully", "token": token}

@app.post("/user/auth/logout", tags=["User Authentication"])
def logout(token: str = Depends(verify_token)):
    # Check if authorization token is provided
    username : UserSchema = verify_token(token)

    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization token")

    # Get stored user
    stored_user = next((u for u in users_db if username == u.username), None)
    if stored_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization token")

    # Updated user login status
    stored_user.isloggedin = False

    return {"Message": "Logout Successfully"}


@app.put("/user/change_password", tags=["Update User Profile"])
@check_token
def change_password(password_update: UpdatePassword, token: str = Depends(verify_token)):
    # Find the user by username
    stored_user : UserSchema = next((u for u in users_db if u.username == password_update.username), None)

    if stored_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user")

    if not pwd_context.verify(password_update.currentPassword, stored_user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid password")

    new_hashed_password = pwd_context.hash(password_update.newPassword)

    stored_user.password = new_hashed_password
    return {"Outcome": "Password Changed Successfully"}


@app.put("/user/change_email", tags=["Update User Profile"])
@check_token
def change_email(email_update: UpdateEmail, token: str = Depends(verify_token)):
    # Find the user by username
    stored_user : UserSchema = next((u for u in users_db if u.username == email_update.username), None)

    if stored_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user")

    stored_user.email = email_update.newEmail

    return {"Outcome": "Email Changed Successfully"}


@app.put("/user/change_name", tags=["Update User Profile"])
@check_token
def change_name(name_update: UpdateName, token: str = Depends(verify_token)):
    # Find the user by username
    stored_user : UserSchema = next((u for u in users_db if u.username == name_update.username), None)

    if stored_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user")

    outcome = {}
    outcome["Outcome"] = "User Exists"
    outcome["First Name"] = "Not Changed"
    outcome["Last Name"] = "Not Changed"

    if name_update.newFirstName is not None:
        stored_user.firstname = name_update.newFirstName
        outcome["First Name"] = f"Changed to {name_update.newFirstName}"


    if name_update.newLastName is not None:
        stored_user.lastname = name_update.newLastName
        outcome["Last Name"] = f"Changed to {name_update.newLastName}"

    return outcome


@app.put("/user/change_profile_picture", tags=["Update User Profile"])
@check_token
def change_profile_picture(profile_picture_update: UpdateProfilePicture, token: str = Depends(verify_token)):
    # Find the user by username
    stored_user : UserSchema = next((u for u in users_db if u.username == profile_picture_update.username), None)
    
    if stored_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user")

    if profile_picture_update.newProfilePic is not None:
        stored_user.newProfilePic = profile_picture_update.newProfilePic
        outcome = {"Outcome": "Profile Picture Changed Successfully"}

    else:
        outcome = {"Outcome": "No Profile Picture for update"}    

    return outcome


@app.post("/carspace/create_car_space", tags=["Car Spaces"])
@check_token
def create_car_space(create_car_space: CreateCarSpaceSchema, token: str = Depends(verify_token)):
    
    stored_user: UserSchema = next((u for u in users_db if u.username == create_car_space.UserName), None)
    
    if stored_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user")

    # Find the user by username
    user_car_spaces = [space for space in carspace_db if space.UserName == create_car_space.UserName]
    
    new_car_space = CarSpaceSchema(
        UserName=create_car_space.UserName,
        CarSpaceId=len(user_car_spaces),
        DateCreated=datetime.now(),
        Title=create_car_space.Title,
        FirstName=create_car_space.FirstName,
        LastName=create_car_space.LastName,
        Email=create_car_space.Email,
        PhoneNumber=create_car_space.PhoneNumber,
        Address=create_car_space.Address,
        AccessKeyRequired=create_car_space.AccessKeyRequired,
        VehicleSize=create_car_space.VehicleSize,
        Currency=create_car_space.Currency,
        Price=create_car_space.Price,
        Frequency=create_car_space.Frequency,
        Pictures=create_car_space.Pictures,
        Reviews=[]
    )
    
    carspace_db.append(new_car_space)

    return {"Message": "Car Space Added Successfully"}

@app.post("/carspace/create_review", tags=["Car Spaces"])
@check_token
def create_car_space_review(car_space_review: CarSpaceReview, token: str = Depends(verify_token)):
    Reviewer : UserSchema = next((u for u in users_db if u.username == car_space_review.ReviewerUserName))
    CarSpace : CarSpaceSchema = next((s for s in carspace_db if s.UserName == car_space_review.OwnerUserName and s.CarSpaceId == car_space_review.CarSpaceId))    
    carspace_reviews.append(car_space_review)
    Reviewer.Reviews.append(car_space_review)
    CarSpace.Reviews.append(car_space_review)

    return {"Message": "Car Space Review Added Successfully"}


@app.put("/carspace/updatelocation", tags=["Car Spaces"])
@check_token
def update_car_space_address(update_space_address: UpdateCarSpaceAddress, token: str = Depends(verify_token)):
    CarSpace : CarSpaceSchema = next((s for s in carspace_db if s.UserName == update_space_address.OwnerUserName and s.CarSpaceId == update_space_address.CarSpaceId))    
    Outcome = {
        "Message": "Car Space Updated Successfully",
        "Address": "Address is unchanged",
        "Postcode": "Postcode is unchanged",
        "Suburb": "Suburb is unchanged"
        }
    
    if update_space_address.NewAddress is not None:
        CarSpace.Address = update_space_address.NewAddress
        Outcome["Address"] = "Address Updated Succesfully"
    
    if update_space_address.NewSuburb is not None:
        CarSpace.Suburb = update_space_address.NewSuburb
        Outcome["Suburb"] = "Suburb Updated Succesfully"
    
    if update_space_address.NewPostcode is not None:
        CarSpace.Postcode = update_space_address.NewPostcode
        Outcome["Postcode"] = "Postcode Updated Succesfully"

    return Outcome


@app.put("/carspace/updatespacedimensions", tags=["Car Spaces"])
@check_token
def update_car_space_details(update_space_dimensions: UpdateCarSpaceDimensions, token: str = Depends(verify_token)):
    CarSpace : CarSpaceSchema = next((s for s in carspace_db if s.UserName == update_space_dimensions.UserName and s.CarSpaceId == update_space_dimensions.CarSpaceId))    
    
    Outcome = {
        "Message": "Car Space Updated Successfully",
        "Width": "Width is unchanged",
        "Breadth": "Breadth is unchanged",
        "SpaceType": "Space Type is unchanged",
        "AccessKeyRequired": "Access Key required is unchanged",
        "VehicleSize": "Vehicle Size is unchanged",
    }
    
    if update_space_dimensions.NewWidth is not None:
        CarSpace.Width = update_space_dimensions.NewWidth
        Outcome["Width"] = "Width has been updated"

    if update_space_dimensions.NewBreadth is not None:
        CarSpace.Breadth = update_space_dimensions.NewWidth
        Outcome["Breadth"] = "Breadth has been updated"

    if update_space_dimensions.NewSpacetype is not None:
        CarSpace.Breadth = update_space_dimensions.NewWidth
        Outcome["Space Type"] = "Space Type has been updated"

    if update_space_dimensions.NewAccessKeyRequired is not None:
        CarSpace.AccessKeyRequired = update_space_dimensions.NewAccessKeyRequired
        Outcome["AccessKeyRequired"] = "Access Key has been updated"

    if update_space_dimensions.NewVehicleSize is not None:
        CarSpace.VehicleSize = update_space_dimensions.NewVehicleSize
        Outcome["VehicleSize"] = "Vehicle Size has been updated"

    return Outcome


@app.put("/carspace/updatespaceprice", tags=["Car Spaces"])
@check_token
def update_car_space_price(update_car_space_price: UpdateCarSpacePrice, token: str = Depends(verify_token)):
    CarSpace : CarSpaceSchema = next((s for s in carspace_db if s.UserName == update_car_space_price.UserName and s.CarSpaceId == update_car_space_price.CarSpaceId))    
    Outcome = {
        "Message": "Car Space Updated Successfully",
        "Currency": "Currency is unchanged",
        "Price": "Price is unchanged",
        "Frequency": "Frequency is unchanged",
    }

    if update_car_space_price.NewCurrency is not None:
        Outcome["Currency"] = "Currency has been updated"
        CarSpace.Currency = update_car_space_price.NewCurrency
    
    if update_car_space_price.NewFrequency is not None:
        Outcome["Frequency"] = "Payment Frequency has been updated"
        CarSpace.Frequency - update_car_space_price.NewFrequency

    if update_car_space_price.NewPrice is not None:
        Outcome["Price"] = "Price has been updated"
        CarSpace.Price = update_car_space_price.NewPrice

    return Outcome


# Can do this instead of CLI (python3 main.py) in which it will run on local host 9000 
# instead of port 8000 (which is entered via uvicorn main:app --reload)
if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port = '9000')


####TUTORIAL CODE!!!
# Everything below is dummy code created via the tutorial
# @app.get("/protected", tags=["User Authentication"])
# def protected_route(token: str = Header(...)):
# Get - for testing
@app.get("/", tags=["Tutorial Routes"])
def greet():
    return {"Hello": "World"}

@app.get("/{id}", tags=["Tutorial Routes"])
def greet(id: int):
    return {"testId": id}

#Example http://127.0.0.1:8000/test/123?num_published=20&published=False
#Example http://127.0.0.1:8000/test/123?num_published=20&published=True
@app.get("/test/{id}", tags=["Tutorial Routes"])
def test_id(id: int, num_published: int, published: bool):
    if published:
        return {'data': f"{num_published} published for page {id}"}
    else:
        return {'data': f"{num_published} not published for page {id}"}

@app.get("/test/sort", tags=["Tutorial Routes"])
def index(limit=10, published: bool=True, sort: Optional[bool] = None): # Default value specified
    if published: 
        return {'data': "it is published"}
    if not published:
        return {'data': 'not published'}
    


# # Dependency function to authenticate the user
# def authenticated_user(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]) -> UserSchema:
#     if credentials:
#         token = credentials.credentials
#         username = verify_token(token)

#         if username:
#             user = next((u for u in users_db if u.username == username), None)
#             if user and user.isloggedin:
#                 return user
    
#     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")


# This does autocomplete :) 
# @app.post("/blog", status_code=status.HTTP_201_CREATED)
# async def create

