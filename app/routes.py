from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.task import Task


task_bp = Blueprint("task", __name__,url_prefix = "/tasks")

# wave 1 
# create a task
@task_bp.route("", methods = ["POST"])
def get_task():
    response_body = request.get_json()
    if "title" not in response_body or "description" not in response_body:
        return jsonify({ "details": "Invalid data"}), 400

    # using class method
    new_task = Task.from_dict(response_body)

    db.session.add(new_task)
    db.session.commit() 

    return jsonify({"task":{
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": False
    }
    }), 201

# get all tasks
# @task_bp.route("", methods = ["GET"])
# def get_all_tasks():
#     response = []
#     tasks = Task.query.all()
#     for task in tasks:
#         response.append(task.to_dict())
#     return jsonify(response), 200


# get one task
@task_bp.route("/<task_id>", methods = ["GET"])
def get_one_task(task_id):
    tasks = validate_task(Task,task_id)

    return jsonify({"task":{
            "id": tasks.task_id,
            "title": tasks.title,
            "description": tasks.description,
            "is_complete": False}
            }), 200


# get update
@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    tasks = validate_task(Task,task_id)
    request_data = request.get_json()
    
    tasks.title = request_data["title"]
    tasks.description = request_data["description"]
    tasks.completed_at = request_data.get("completed_at", None)

    db.session.commit()

    return jsonify({"task":{
            "id": tasks.task_id,
            "title": tasks.title,
            "description": tasks.description,
            "is_complete": False
            }
            }), 200


# delete task
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = validate_task(Task,task_id)

    db.session.delete(tasks)
    db.session.commit()

    return {"details": f'Task {task_id} "Go on my daily walk 🏞" successfully deleted'}



# helper function
def validate_task(model,task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return abort(make_response({"msg": "id is invalide input"}, 400))
    
    # return Task.query.get_or_404(task_id_num)
 
    task = model.query.get(task_id)
    if task is None:
        abort(make_response({"msg": "Task not found"}, 404))
    return task


# wave 2 
# get task by asc and desc order
@task_bp.route("", methods =["GET"])
def sort_title_asc_and_desc():
    sort_by = request.args.get("sort")
    response =[]

    if sort_by == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_by == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    for task in tasks:
        response.append(task.to_dict())
    #     response.append({
    #         "id": task.task_id,
    #         "title":task.title,
    #         "description": task.description,
    #         "is_complete": False
    # })

    return jsonify(response), 200
