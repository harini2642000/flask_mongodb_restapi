from flask import Flask, request, jsonify,render_template
from flask_restful import Resource,Api,reqparse, abort, fields, marshal_with
from flask_mongoengine import MongoEngine
app = Flask(__name__)
api =Api(app)
app.config['MONGODB_SETTINGS'] = {
    'db': 'mydb',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

task_post_args =reqparse.RequestParser()
#task_post_args.add_argument("Student_id",type=int,help="student id is required",required=True)
task_post_args.add_argument("First_name",type=str,help="First name is required",required=True)
task_post_args.add_argument("Last_name",type=str,help="Last name is required",required=True)
task_post_args.add_argument("email",type=str,help="E mail is required",required=True)

task_update_args = reqparse.RequestParser()
task_update_args.add_argument("First_name", type = str)
task_update_args.add_argument("Last_name", type =str)
task_update_args.add_argument("email",type=str)

resorce_fields ={
    '_id':fields.Integer,
    'First_name':fields.String,
    'Last_name' :fields.String,
    'email' :fields.String
}
class Student(db.Document):
    _id=db.IntField()
    First_name = db.StringField(required=True)
    Last_name = db.StringField(required = True)
    email = db.StringField( required = True)

class Student_Rest(Resource):
    @marshal_with(resorce_fields)
    def get(self,student_id):
        student = Student.objects.get(_id=student_id)
        if not student:
            abort(404, message="Could not find the id")
        return student

    @marshal_with(resorce_fields)
    def post(self,student_id):
        args = task_post_args.parse_args()
        student = Student(_id=student_id,First_name=args["First_name"],Last_name=args["Last_name"],email=args["email"]).save()
        return student,201

    @marshal_with(resorce_fields)    
    def put(self,student_id):
        args =task_update_args.parse_args()
        if args['First_name']:
            Student.objects.get(_id=student_id).update(First_name=args['First_name'])
        if args['Last_name']:
            Student.objects.get(_id=student_id).update(Last_name=args['Last_name'])
        if args['email']:
            Student.objects.get(_id=student_id).update(email=args['email'])
        return"{} updated".format(student_id),200

    @marshal_with(resorce_fields)
    def delete(self,student_id):
        Student.objects(_id=student_id).delete()
        return "student deleted",204

api.add_resource(Student_Rest,'/student/<int:student_id>')

if __name__ == "__main__":
    app.run(debug=True)

    

# @app.route('/', methods=['GET'])
# def query_records():
#     name = request.args.get('name')
#     user = User.objects(name=name).first()
#     if not user:
#         return jsonify({'error': 'data not found'})
#     else:
#         return jsonify(user.to_json())
#
# @app.route('/', methods=['PUT'])
# def create_record():
#     record = json.loads(request.data)
#     user = User(name=record['name'],
#                 email=record['email'])
#     user.save()
#     return jsonify(user.to_json())
#
# @app.route('/', methods=['POST'])
# def update_record():
#     record = json.loads(request.data)
#     user = User.objects(name=record['name']).first()
#     if not user:
#         return jsonify({'error': 'data not found'})
#     else:
#         user.update(email=record['email'])
#     return jsonify(user.to_json())
#
# @app.route('/', methods=['DELETE'])
# def delete_record():
#     record = json.loads(request.data)
#     user = User.objects(name=record['name']).first()
#     if not user:
#         return jsonify({'error': 'data not found'})
#     else:
#         user.delete()
#     return jsonify(user.to_json())

if __name__ == "__main__":
    app.run(debug=True)