from fastapi import FastAPI, HTTPException, status
from .schemas import User

app = FastAPI() # create FastAPI instance
users: list[User] = [] # in-memory store for users


# checking if the server is running
@app.get("/hello")
def hello():
    return {"message": "Hello, World!"}

# CRUD operations for users
@app.get("/api/users") # get all users
def get_users():
    return users

@app.get("/api/users/{user_id}") # get user by user_id
def get_user(user_id: int):
    for u in users:
        if u.user_id == user_id: # if user is found by user_id return user
            return u
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@app.post("/api/users", status_code=status.HTTP_201_CREATED) # creating a new user
def add_user(user: User):
    if any(u.user_id == user.user_id for u in users): # check if user_id already exists
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user_id already exists")
    users.append(user) # add user to the in-memory list
    return user

@app.put("/api/users/{user_id}", status_code=status.HTTP_202_ACCEPTED) # update user by user_id
def update_user(user_id: int, user: User):
    user.user_id = user_id # ensure the user_id in path and body are the same
    for i, u in enumerate(users): # find user by user_id and update
        if u.user_id == user_id:
            users[i] = user # update user in the in-memory list
            return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user_id not found")

@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT) # delete user by user_id
def delete_user(user_id: int):
    for i, u in enumerate(users): # find user by user_id and delete
        if u.user_id == user_id: 
            users.pop(i) # remove user from the in-memory list
            return 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@app.get("/health") # health check endpoint
def health():
    return { "status": "ok" } 
    




    
    
