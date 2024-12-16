from flask import Flask, jsonify, request

app = Flask(__name__)

# Lista para almacenar las tareas
tasks = []
task_id_counter = 1  # Contador para generar IDs únicos

# GET /tasks: Devuelve la lista de tareas
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks), 200

# POST /tasks: Crea una nueva tarea
@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_counter
    data = request.get_json()

    # Validar que se reciba el campo 'title'
    if not data or 'title' not in data or not isinstance(data['title'], str) or not data['title'].strip():
        return jsonify({"error": "Invalid input. 'title' is required and must be a non-empty string"}), 400

    # Crear la nueva tarea
    new_task = {
        "id": task_id_counter,
        "title": data['title'].strip(),
        "completed": False  # Por defecto, las tareas nuevas no están completadas
    }
    tasks.append(new_task)
    task_id_counter += 1
    return jsonify(new_task), 201

# PUT /tasks/<id>: Actualiza una tarea específica
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()

    # Buscar la tarea por ID
    task = next((task for task in tasks if task['id'] == id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404

    # Validar datos de entrada
    if 'title' in data:
        if not isinstance(data['title'], str) or not data['title'].strip():
            return jsonify({"error": "Invalid input. 'title' must be a non-empty string"}), 400
        task['title'] = data['title'].strip()
    if 'completed' in data:
        if not isinstance(data['completed'], bool):
            return jsonify({"error": "Invalid input. 'completed' must be a boolean"}), 400
        task['completed'] = data['completed']

    return jsonify(task), 200

# DELETE /tasks/<id>: Elimina una tarea por su ID
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    global tasks
    # Buscar la tarea por ID
    task = next((task for task in tasks if task['id'] == id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404

    # Eliminar la tarea
    tasks = [task for task in tasks if task['id'] != id]
    return jsonify({"message": "Task deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
