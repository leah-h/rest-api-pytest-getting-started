import requests
import uuid

ENDPOINT = "https://todo.pixegami.io"

def test_can_create_task():
    payload = new_task_payload()
    response_create_task = requests.put(ENDPOINT + "/create-task", json=payload)
    assert response_create_task.status_code == 200

    data = response_create_task.json()

    task_id = data["task"]["task_id"]
    response_get_task = requests.get(ENDPOINT + f"/get-task/{task_id}")

    assert response_get_task.status_code == 200
    get_task_data = response_get_task.json()
    assert get_task_data["content"] == payload["content"]
    assert get_task_data["user_id"] == payload["user_id"]


def test_can_update_task():
    payload = {
        "content": "test content",
        "user_id": "test_user",
        "is_done": False
    }
    response_create_task = create_task()
    assert response_create_task.status_code == 200

    data = response_create_task.json()
    task_id = data["task"]["task_id"]

    update_payload = {
        "task_id": task_id,
        "content": "updated content",
        "user_id": "test_user",
        "is_done": True
    }
    response_update_task = requests.post(ENDPOINT + "/update-task", json=update_payload)
    assert response_update_task.status_code == 200

    response_get_task = get_task()
    assert response_get_task.status_code == 200

    get_task_data = response_get_task.json()
    assert get_task_data["content"] == update_payload["content"]
    assert get_task_data["user_id"] == update_payload["user_id"]
    assert get_task_data["is_done"] == update_payload["is_done"]


def test_can_update_task():
    # create a task
    payload = new_task_payload()
    response_create_task = create_task(payload)
    task_id = response_create_task.json()["task"]["task_id"]
    #update the task
    new_payload = {
        "user_id": payload["user_id"],
        "task_id": task_id,
        "content": "updated content",
        "is_done": True,
    }
    update_task_response = update_task(new_payload)
    assert update_task_response.status_code == 200

    # get and validate the changes
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == new_payload["content"]
    assert get_task_data["is_done"] == new_payload["is_done"]

def test_can_list_tasks():
    # create N tasks
    n = 3
    payload = new_task_payload()
    for _ in range(n):
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200

    # lists tasks and validate the count
    user_id = payload["user_id"]
    list_task_response = list_tasks(user_id)
    assert list_task_response.status_code == 200
    data = list_task_response.json()

    tasks = data["tasks"]
    assert len(tasks) == n


def test_can_delete_task():
    # create a task
    #delete the task
    # get the task and check task is not found
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]

    delete_task_response = delete_task(task_id)
    assert delete_task_response.status_code == 200

    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404
    pass


def create_task(payload):
    return requests.put(ENDPOINT + "/create-task", json=payload)

def update_task(payload):
    return requests.put(ENDPOINT + "/update-task", json=payload)

def get_task(task_id):
    return requests.get(ENDPOINT + f"/get-task/{task_id}")

def list_tasks(user_id):
    return requests.get(ENDPOINT + f"/list-tasks/{user_id}")

def delete_task(task_id):
    return requests.delete(ENDPOINT + f"/delete-task/{task_id}")

def new_task_payload():
    user_id = f"test_user_{uuid.uuid4().hex}"
    content = f"test content {uuid.uuid4().hex}"

    print(f"Creating task for user {user_id} with content {content}")

    return {
        "content": content,
        "user_id": user_id,
        "is_done": False
    }
