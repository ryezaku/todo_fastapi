from email import header
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import pandas as pd
import json
import uvicorn
from fastapi import Security, Depends, FastAPI, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
import secrets
from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse
import os
path = os.path.dirname(os.path.abspath(__file__))
generated_key = secrets.token_urlsafe(16)
a = os.path.join(path, "access_key.json")
with open(a) as f:
    key = json.loads(f.read())
if "access_token" in key["access_key"]:
    API_KEY = key["access_key"]["access_token"]
    API_KEY_NAME = "access_token"
else:
    API_KEY = None
    API_KEY_NAME = "access_token"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)

def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    api_key_cookie: str = Security(api_key_cookie),
):
    if api_key_query == API_KEY:
        return api_key_query
    elif api_key_header == API_KEY:
        return api_key_header
    elif api_key_cookie == API_KEY:
        return api_key_cookie
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
class LogUser(BaseModel):
    username: str
    password: str

class RegUser(BaseModel):
    username: str
    password: str
class Todo(BaseModel):
    username: str
    password: str
    task: str

class UpdateTodo(BaseModel):
    username: str
    password: str
    task_name: str
    task_status: str

class DeleteTodo(BaseModel):
    username: str
    password: str
    task_name: str

app = FastAPI(title="Todo API")

# Create, Read, Update, Delete
store_todo = {}
user = {}

@app.post('/register')
async def registration(user: RegUser):
    try:
        df = pd.read_csv('data.csv')
    except:
        df = pd.DataFrame(columns=['username', 'password'])
    details = 'username already exists'
    if user.username in df['username'].unique():
        raise HTTPException(status_code=404, detail=details)
    user_info = user
    user = dict(user)
    user = pd.DataFrame([user])
    task_df = pd.DataFrame(columns=['task', 'status'])
    task_df.to_csv(user_info.username + '.csv',  index = False)
    # user = {'username': user.username, 'password': user.password, 'task':user.password}
    df = df.append(user, ignore_index=True)
    df.to_csv('data.csv',  index = False)
    # df.to_csv('data.csv',mode= 'a', index=False)
    return {'status':'registration done'}

@app.post('/todo/add')
async def add_todo(todo: Todo):
    df = pd.read_csv('data.csv')
    try:
        detail = "username is incorrect"
        dfuser_index = df.loc[df['username'] == todo.username].index
        detail = "password is incorrect"
        user_password = df.at[dfuser_index[0], 'password']
        if str(user_password) == str(todo.password):
            df_task = pd.read_csv(todo.username + '.csv')
            task_dict = {}
            task_dict['task'] = todo.task
            task_dict['status'] = "incomplete"
            task = pd.DataFrame([task_dict])
            df_task = df_task.append(task, ignore_index=True)
            df_task.to_csv(todo.username + '.csv',index = False)   
        else:
            raise HTTPException(status_code=404, detail=detail)
        return {'status':"added to list"}  
    except Exception as e:
        raise HTTPException(status_code=404, detail=detail)

    # dfuser = df.loc[df['username'] == todo.username].index
    store_todo.append(todo)
    return todo
@app.post('/todo/get_all_todo')
async def get_all_todos(todo:Todo):
    df = pd.read_csv('data.csv')
    try:
        detail = "username is incorrect"
        dfuser_index = df.loc[df['username'] == todo.username].index
        detail = "password is incorrect"
        user_password = df.at[dfuser_index[0], 'password']
        if str(user_password) == str(todo.password):
            user_tasks = pd.read_csv(todo.username + '.csv')
            user_tasks = user_tasks.to_dict(orient='records')
        return user_tasks 
    except:
        raise HTTPException(status_code=404, detail=detail)

@app.post('/todo/update')
async def update_todo(todo: UpdateTodo):
    try:
        df = pd.read_csv('data.csv')
        detail = "username is incorrect"
        dfuser_index = df.loc[df['username'] == todo.username].index
        detail = "password is incorrect"
        user_password = df.at[dfuser_index[0], 'password']
        if str(user_password) == str(todo.password):
            df_tasks = pd.read_csv(todo.username + '.csv')
            
            detail = "task is not available"
            user_task_index = df_tasks.loc[df_tasks['task'] == todo.task_name].index
           
            task = df_tasks.at[user_task_index[0], 'task']
            if todo.task_name ==task:
                df_tasks.loc[df_tasks['task'] == todo.task_name, 'status'] = todo.task_status
                
                df_tasks.to_csv(todo.username + '.csv',index = False)   
            else:
                raise HTTPException(status_code=404, detail=detail)

        return "update complete"
    except:
        raise HTTPException(status_code=404, detail=detail)

@app.post('/todo/delete')
async def delete_todo( todo: DeleteTodo):
    try:
        df = pd.read_csv('data.csv')
        detail = "username is incorrect"
        dfuser_index = df.loc[df['username'] == todo.username].index
        detail = "password is incorrect"
        user_password = df.at[dfuser_index[0], 'password']
        if str(user_password) == str(todo.password):
            df_tasks = pd.read_csv(todo.username + '.csv') 
            detail = "task is not available"
            user_task_index = df_tasks.loc[df_tasks['task'] == todo.task_name].index
            task = df_tasks.at[user_task_index[0], 'task']
            if todo.task_name ==task:
                df_tasks.drop(user_task_index[0],axis=0, inplace=True)
                df_tasks.to_csv(todo.username + '.csv',index = False)   
            else:
                raise HTTPException(status_code=404, detail=detail)
        return "item deleted"
    except:
        raise HTTPException(status_code=404, detail=detail)
if __name__ == "__main__":
    uvicorn.run(app, host = '127.0.0.1', port = 5000, debug = True)