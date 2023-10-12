from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app=Flask(__name__)
'''
@app.route('/',methods=['GET'])
def home():
    return jsonify(
        {
            'name': 'selva','msg':'Welcome'
         })
'''
basedir=os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)
marsh=Marshmallow(app)

class user(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100))
    contact=db.Column(db.String(100),unique=True)

    def __init__(self,name,contact):
        self.name=name
        self.contact=contact  

class UserSchema(marsh.Schema):
    class Meta:
        fields = ('id', 'name', 'contact')

user_schema = UserSchema()
users_schema=UserSchema(many=True)

# Add new user POST
@app.route('/user', methods=['POST'])
def add_user():
    name=request.json['name']
    contact=request.json['contact']
    new_user=user(name,contact)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)

# Show All User GET
@app.route('/user',methods=['GET'])
def getallUsers():
    all_user=user.query.all()
    result=users_schema.dump(all_user)
    return jsonify(result)

# show User By ID
@app.route('/user/<id>',methods=['GET'])
def getUsersByid(id):
    users=user.query.get(id)
    return user_schema.jsonify(users)

#Update User By ID
@app.route('/user/<id>',methods=['PUT'])
def UpdateUser(id):
    users=user.query.get(id)
    name=request.json['name']
    contact=request.json['contact']
    users.name=name
    users.contact=contact
    db.session.commit()
    return user_schema.jsonify(users)

#Delete user by id
@app.route('/user/<id>',methods=['DELETE'])
def DeleteUser(id):
    users=user.query.get(id)
    db.session.delete(users)
    db.session.commit()
    return user_schema.jsonify(users)



if __name__=='__main__':
    app.run(debug=True)