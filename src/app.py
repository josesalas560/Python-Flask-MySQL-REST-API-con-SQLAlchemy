from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
#conectamos nuestra base de datos#
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:18040081@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
#aqui definimos nuestras tareas que se van a estar guardando en la base de datos#
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(100))
#definimos nuestras variables#
    def __init__(self, title, description):
        self.title = title
        self.description = description
#crea las tablas#
db.create_all()
#crea el esquemas de la tabla#
class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
#metodo para el post para insertar informacion#
@app.route('/tasks', methods=['Post'])
def create_task():
  title = request.json['title']
  description = request.json['description']
  new_task= Task(title, description)
  db.session.add(new_task)
  db.session.commit()
  return task_schema.jsonify(new_task)
#metodo get para obtener informacion#
@app.route('/tasks', methods=['GET'])
def get_tasks():
  all_tasks = Task.query.all()
  result = tasks_schema.dump(all_tasks)
  return jsonify(result)
#metodo get para buscar tarea por id#
@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
  task = Task.query.get(id)
  return task_schema.jsonify(task)
#metodo put para editar la infromacion#
@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
  task = Task.query.get(id)
  title = request.json['title']
  description = request.json['description']
  task.title = title
  task.description = description
  db.session.commit()
  return task_schema.jsonify(task)
#metodo delete para eliminar infromacion#
@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
  task = Task.query.get(id)
  db.session.delete(task)
  db.session.commit()
  return task_schema.jsonify(task) 
#corremos nuestra api#
if __name__ == "__main__":
    app.run(debug=True)