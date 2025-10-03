from fastapi import FastAPI                             # import FastApi class
from fastapi import HTTPException                       # import HHTPExeption class
from storage import TaskStorage                         # import TaskStorage class
app = FastAPI()                                         # create copy of FastAPi class
storage = TaskStorage()                                 # create copy of TaskStorage class
# we display a list of all received tasks.
@app.get("/tasks")                                      # use standart FastApi get decorator
def get_tasks():                                        # get task method 
    return storage.load()                               # return task lsit
# We add a new task, add it to the task list, and increment the id counter.
@app.post("/tasks")                                     # use standart FastAPI post decorator
def create_task(name: str, condition: str = 'new'):     # create new task method
    tasks = storage.load()                              # task list now in tasks
    new_id = max((task['id'] for task in tasks), default = 0) + 1    # crate new id fo task
    task = {'id': new_id, 'name': name, 'condition': condition}  # task dict   
    tasks.append(task)                                  # append task on list
    storage.save(tasks)                                 # save task
    return task                                         # return new task
# We update the task; if the task is missing, we raise an error.
@app.put("/tasks/{task_id}")                            # use standart FastAPI put decorator
def update_task(task_id: int, name: str, condition: str):  # update task meyhod
    tasks = storage.load()                              # loads all tasks list
    for task in tasks:                                  # finding task cicle
        if task['id'] == task_id:                       # check task id in list
            task['name'] = name                         # update name if id in list
            task['condition'] = condition               # update status if id in list
            storage.save(tasks)                         # save task in list
            return task                                 # return updated task
    raise HTTPException(status_code = 404, detail = 'task not found') # raise if id not in list
# We search for a task by ID, if we find it, we delete it, if not, we raise an error
@app.delete("/tasks/{task_id}")                         # use standart FastApi delete decorator
def delete_task(task_id: int):                          # delete task method
    tasks = storage.load()                              # loads all tasks list
    for task in tasks:                                  # finding task cicle
        if task['id'] == task_id:                       # check task id in list
            tasks.remove(task)                          # remove task if id in list
            storage.save(tasks)                         # save tasks list
            return 'task deleted'                       # return delete message
    raise HTTPException(status_code = 404, detail = 'task not found') # raise if id not in list