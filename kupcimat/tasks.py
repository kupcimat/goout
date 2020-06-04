import json

from google.cloud import tasks_v2

from kupcimat import util


def create_queue_path(project: str, location: str, queue: str) -> str:
    return tasks_v2.CloudTasksClient.queue_path(project, location, queue)


def create_task(queue_path: str, url: str, payload: dict) -> str:
    tasks_client = tasks_v2.CloudTasksClient()

    task_id = util.generate_id()
    task = {
        "name": f"{queue_path}/tasks/{task_id}",
        "http_request": {
            "http_method": "POST",
            "url": url,
            "body": convert_payload(payload)
        }
    }
    tasks_client.create_task(queue_path, task)
    return task_id


def convert_payload(payload: dict) -> bytes:
    return json.dumps(payload).encode()
