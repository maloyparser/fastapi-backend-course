'''backend'''
from fastapi import FastAPI, HTTPException

app = FastAPI()
tasks = []
task_id_counter = 1
# return tasks list
@app.get("/tasks")
def get_tasks():
    return tasks
#create a new task with id, name, and status 
@app.post("/tasks")
def create_task(name: str, condition: str = 'new'):
    global task_id_counter
    task = {'id': task_id_counter, 'name': name, 'condition': condition}
    tasks.append(task)
    task_id_counter += 1
    return task
#update task    
@app.put("/tasks/{task_id}")
def update_task(task_id: int, name: str, condition: str):
    for task in tasks:
        if task['id'] == task_id:
            task['name'] = name
            task['condition'] = condition
            return task
    raise HTTPException(status_code = 404, detail = 'task not found')
#delete task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            return 'task deleted'
 