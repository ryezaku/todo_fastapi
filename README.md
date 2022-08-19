# todo
todo api
## Package required
Go to working directory and enter the command
```
pip install -r requirements.txt
```

   
# Running The FastAPI 
1.to run the fast api service,go to the directory path and type 
```
python todo.py
```

After the message below is shown on the console, we may start to send the POST request
```
INFO:     Started server process [3024]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:5000 (Press CTRL+C to quit)
```
- The POST request was tested using Postman
- The json body is shown below:

We require the access token to  be included in the postman in order to use the api
send the request to here to register the user:
```
http://localhost:5000/reg
```
##  example for registration of user
```
{   
"username": "asasasass123",
"password": "abc123"
}
```
- for the user-id request, we may pass null for the track id 

## For add task:
```
http://localhost:5000/todo/add
```
```
{   
"username": "asasasass123",
"password": "abc123",
"task": "add number1"
}

```

## For getting task:
```
http://localhost:5000/todo/get_all_todo
```
```
{   
"username": "asasasass123",
"password": "abc123"

}

```

## For updating task:
we can assign task as "completed" because newly added task will be marked as "incomplete"
```
http://localhost:5000/todo/update
```
```
{   
"username": "asasasass123",
"password": "abc123",
"task_name": "add number"
"task_status": "completed"

}

```

## For deleting task:
```
http://localhost:5000/todo/delete
```
```
{   
"username": "asasasass123",
"password": "abc123",
"task_name": "add number"

}

```