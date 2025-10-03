from fastapi import FastAPI                           
from fastapi import HTTPException                   
from storage_gist import GistStorage                     
app = FastAPI()                                     
storage = GistStorage()                              
# we display a list of all received tasks.
@app.get("/tasks")                                    
def get_tasks():                                      
    return storage.load()                            
# We add a new task, add it to the task list, and increment the id counter.
@app.post("/tasks")                                     
def create_task(name: str, condition: str = 'new'):     
    tasks = storage.load()                              
    new_id = max((task['id'] for task in tasks), default = 0) + 1  
    task = {'id': new_id, 'name': name, 'condition': condition}  
    tasks.append(task)                                 
    storage.save(tasks)                               
    return task                                        
# We update the task; if the task is missing, we raise an error.
@app.put("/tasks/{task_id}")                            
def update_task(task_id: int, name: str, condition: str):
    tasks = storage.load()                            
    for task in tasks:                                  
        if task['id'] == task_id:                    
            task['name'] = name                         
            task['condition'] = condition             
            storage.save(tasks)                      
            return task                                 
    raise HTTPException(status_code = 404, detail = 'task not found') 
# We search for a task by ID, if we find it, we delete it, if not, we raise an error
@app.delete("/tasks/{task_id}")                       
def delete_task(task_id: int):                          
    tasks = storage.load()                           
    for task in tasks:                               
        if task['id'] == task_id:                       
            tasks.remove(task)                         
            storage.save(tasks)                        
            return 'task deleted'                       
    raise HTTPException(status_code = 404, detail = 'task not found')