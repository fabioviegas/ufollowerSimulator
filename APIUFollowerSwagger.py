from flask import Flask
from flask_restplus import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='API UFollower',
    description='API UFollower',
)

ns = api.namespace('Operações: Nodo Pessoal', description='')

todo = api.model('Todo', {
    'id': fields.Integer(readOnly=True, description='Identificado único de cada nodo pessoal'),
    'nome': fields.String(required=True, description='Nome do nodo pessoal'),
    'pais': fields.String(required=True, description='The task details'),
    'idade': fields.String(required=True, description='Idade'),
    'genero': fields.String(required=True, description='Feminino e Masculino'),
    'endereco': fields.String(required=True, description='Endereço'),
    'e-mail': fields.String(required=True, description='E-mail'),
    'dt_nascimento': fields.String(required=True, description='Data de Nascimento'),
     'Lat': fields.String(required=True, description='Latitude'),
     'Lon': fields.String(required=True, description='Longitude'),
     'perfil': fields.String(required=True, description='Agente, Morador, Turista')

})


class TodoDAO(object):
    def __init__(self):
        self.counter = 0
        self.todos = []

    def get(self, id):
        for todo in self.todos:
            if todo['id'] == id:
                return todo
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        todo = data
        todo['id'] = self.counter = self.counter + 1
        self.todos.append(todo)
        return todo

    def update(self, id, data):
        todo = self.get(id)
        todo.update(data)
        return todo

    def delete(self, id):
        todo = self.get(id)
        self.todos.remove(todo)


DAO = TodoDAO()

@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''Listar Nodos'''
        return DAO.todos

    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        '''Criar um Recurso Nodo Pessoal'''
        return DAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        '''Buscar um Recurso Nodo Pessoal'''
        return DAO.get(id)

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Deletar um Recurso Nodo Pessoal através do seu identificador'''
        DAO.delete(id)
        return '', 204

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        '''Atualizar um Recurso Nodo Pessoal através do seu identificador'''
        return DAO.update(id, api.payload)


if __name__ == '__main__':
    app.run(debug=True)
