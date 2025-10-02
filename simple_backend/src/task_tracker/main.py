from fastapi import FastAPI
from fastapi import HTTPException

app = FastAPI()
tasks = []
task_id_counter = 1
# выводим список всех полученных задач
@app.get("/tasks")
def get_tasks():
    return tasks
# добавляем новую задачу, добавляем ее в список задач и увеличиваем счетчик id
@app.post("/tasks")
def create_task(name: str, condition: str = 'new'):
    task = {'id': task_id_counter, 'name': name, 'condition': condition}
    tasks.append(task)
    task_id_counter += 1
    return task
# обновляем задачу , в случае отсутствия задачи вызываем ошибку
@app.put("/tasks/{task_id}")
def update_task(task_id: int, name:str, condition: str):
    for task in tasks:
        if task['id'] == task_id:
            task[name] = name
            task[condition] = condition
        return task
    raise HTTPException(status_code = 404, detail = 'task not found')
# ищем задачу по id, если находи - удаляем, если нет - вызываем ошибку
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            return 'task deleted'
    raise HTTPException(status_code = 404, detail = 'task not found')