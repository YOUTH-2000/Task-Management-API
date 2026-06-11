# Multi-User Task Management API

## Project Description
A full-stack task management application buit with FastAPI, SQLAlchemy, MySQL and Kivy. This project supports multi-user authentication and task management features with RESTful APIs. User can register, login, and manage their own tasks securely.

## Features

- User registration and login
- JWT authentication
- Multi-user support
- Create, update, delete and view tasks
- Task priority and status system
- Secure hashing password
- FastAPI backend
- Kivy frontend application
- MySQL database integration

## Technologies Used

### Backend
- Python
- FastAPI
- SQLAlchemy
- Pydantic
- MySQL
- Uvicorn
- Passlib
- Python-Jose(JWT)

### Frontend
- Kivy
- Requests

## Project Structure
multi-user task management api/
|
├── backend/
|   ├── core/
|   |   ├── config.py
|   |   └── security.py
|   |
|   ├── database/
|   |   ├── connection.py
|   |   ├── dependency.py
|   |   └── models.py
|   |
|   ├── routes/
|   |   ├── auth.py
|   |   └── tasks.py
|   |  
|   ├── schemas/
|   |   ├── enums.py
|   |   ├── task.py
|   |   └── user.py 
|   |  
|   ├── services/
|   |   ├── task_service.py
|   |   └── user_service.py 
|   |
|   └── main.py 
|   
├── fronend/
|   ├── api/
|   |   └── client.py 
|   └── main.py
|
├── .env
├── .gitignore
├── README.md 
└── requirements.txt

## Installation 

### Backend Setup
- Create Virtual Environment
    - python -m venv venv
- Activate Virtual Environment
    - venv\Scripts\activate
- pip install -r requirements.txt
- Run FastAPI Server
    - uvicorn backend.main:app --reload

### Frontend
- Run Kivy Application
    - python frontend.main.py

## Author
Moth Moth Thet Lwin


