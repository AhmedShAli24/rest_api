
####################################
##Used Thunde Cleint to test Users##
####################################
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource,Api,reqparse,fields,marshal_with,abort

app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

##Created Database
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),unique=True, nullable=False)
    email = db.Column(db.String(80),unique=True, nullable=False)
    
    def __repr__(self):
        return f"User(name ={self.name}, email = {self.email})"
    
user_args = reqparse.RequestParser()

## Expected Fields##
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('email', type=str, required=True, help="email cannot be blank")

## Definig format users data when returning in a response##
userFields={
    'id':fields.Integer,
    'name':fields.String,
    'email':fields.String,
}

##First Inpoint
class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        ## Retreatin all the users from the database
        users = UserModel.query.all()
        return users
    
    ##Create
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        ## Creating a user
        user = UserModel(name=args["name"], email=args["email"])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201 ## 201 is http status for created 

class User(Resource):
    ## Read
    @marshal_with(userFields)
    def get(self, id):
        ## Retreatin all the users from the database
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404), "user not found"
        return user
   
   ## Update ##
    @marshal_with(userFields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404), "user not found"
        user.name = args["name"]
        user.email = args["email"]
        db.session.commit()
        return user
    
    ## Delete ##
    @marshal_with(userFields)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404), "user not found"
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users,

##Assigning to a URL
api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>')
@app.route('/')
def home():
    return '<h1> Flask API</h1>'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)