from fastapi import FastAPI
from fastapi import HTTPException

app = FastAPI()
tasks = []
task_id_counter = 1
# we display a list of all received tasks.
@app.get("/tasks")
def get_tasks():
    return tasks
# We add a new task, add it to the task list, and increment the id counter.
@app.post("/tasks")
def create_task(name: str, condition: str = 'new'):
    global task_id_counter
    task = {'id': task_id_counter, 'name': name, 'condition': condition}
    tasks.append(task)
    task_id_counter += 1
    return task
# We update the task; if the task is missing, we raise an error.
@app.put("/tasks/{task_id}")
def update_task(task_id: int, name:str, condition: str):
    for task in tasks:
        if task['id'] == task_id:
            task[name] = name
            task[condition] = condition
        return task
    raise HTTPException(status_code = 404, detail = 'task not found')
# We search for a task by ID, if we find it, we delete it, if not, we raise an error
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            return 'task deleted'
    raise HTTPException(status_code = 404, detail = 'task not found')