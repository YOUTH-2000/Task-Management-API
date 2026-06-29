import requests

BASE_URL = "http://localhost:8000"

def login_user(email, password):

    return requests.post(
        f"{BASE_URL}/auth/login",
        json = {
            "email": email,
            "password": password
        }
    )

def register_user(username, email, password):
    url = f"{BASE_URL}/auth/register"

    data = {
        "username": username,
        "email": email,
        "password": password
    }

    response = requests.post(url, json=data)
    return response

def get_tasks(token):
    headers = {"Authorization": f"Bearer {token}"}

    return requests.get(
        f"{BASE_URL}/tasks",
        headers=headers
    )

def create_task(token, title):
    headers = {"Authorization": f"Bearer {token}"}

    return requests.post(
        f"{BASE_URL}/tasks",
        json = {
            "title": title,
            "description": "",
            "status": "pending",
            "priority": "low"
        },
        headers = headers
    )

def edit_task(token,task_id, title):
    headers = {"Authorization": f"Bearer {token}"}

    return requests.put(
        f"{BASE_URL}/tasks/{task_id}",
        json = {"title" : title},
        headers = headers
    )

def delete_task_api(token, task_id):
    headers = {"Authorization": f"Bearer {token}"}

    return requests.delete(
        f"{BASE_URL}/tasks/{task_id}",
        headers = headers
    )

def update_task(token, task_id, status):
    headers = {"Authorization": f"Bearer {token}"}

    return requests.put(
        f"{BASE_URL}/tasks/{task_id}",
        json = {
            "status": status
        },
        headers = headers
    )
