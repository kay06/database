from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy

from flask_marshmallow import Marshmallow

from flask_cors import CORS

from flask_bcrypt import Bcrypt



import os



app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, 'app.sqlite')



db = SQLAlchemy(app)

ma = Marshmallow(app)

bcrypt = Bcrypt(app)

CORS(app)



class User(db.Model):

    id = db.Column(db.Integer, primary_key = True)

    username = db.Column(db.String, nullable = False, unique = True)

    password = db.Column(db.String, nullable= False)

    email = db.Column(db.String, nullable = False, unique = True)



    def __init__(self, username, password, email):

        self.username = username

        self.password = password

        self.email = email



class UserSchema(ma.Schema):

    class Meta:

        fields = ("id", "username", "password", "email")



user_schema = UserSchema()

multi_user_schema = UserSchema(many = True)



# Add Endpoints Here

@app.route("/user/add", methods=["POST"])

def add_user():

    if request.content_type != "application/json":

        return jsonify("Error Adding User Enter AS type JSON!")



    post_data = request.get_json()

    username = post_data.get("username")

    password = post_data.get("password")

    email = post_data.get("email")



    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')



    new_record = User(username, pw_hash, email)

    db.session.add(new_record)

    db.session.commit()



    return jsonify(user_schema.dump(new_record))



# Verification Endpoint

@app.route('/user/verify', methods=["POST"])

def verification():

    if request.content_type != "application/json":

        return jsonify("Error Improper Validation Credintials!")



    post_data = request.get_json()

    username = post_data.get("username")

    password = post_data.get("password")



    user = db.session.query(User).filter(User.username == username).first()



    if user is None:

        return jsonify("User could not be Verified")



    if not bcrypt.check_password_hash(user.password, password):

        return jsonify("User could not be Verified")



    return jsonify("User Verified")



# Get All Users

@app.route("/user/get", methods=["GET"])

def get_users():

    all_users = db.session.query(User).all()

    return jsonify(multi_user_schema.dump(all_users))



# Delete User EndPoint



@app.route('/user/delete/<id>', methods=["DELETE"])

def user_delete(id):

    delete_user = db.session.query(User).filter(User.id == id).first()

    db.session.delete(delete_user)

    db.session.commit()

    return jsonify(" Another one Bites the Dust!")





# Update Username/Email 



@app.route('/user/update/<id>', methods=["PUT"])

def update_usermail(id):

    if request.content_type != "application/json":

        return jsonify("JSON Needed or no Coookies for you!")



    put_data = request.get_json()

    username = put_data.get("username")

    email = put_data.get("email")



    usermail_update = db.session.query(User).filter(User.id == id).first()



    if username != None:

        usermail_update.username = username

    if email != None:

        usermail_update.email = email



    db.session.commit()

    return jsonify(user_schema.dump(usermail_update))



# Password Update

@app.route('/user/pw/<id>', methods=["PUT"])

def pw_update(id):

    if request.content_type != "application/json":

        return jsonify("JSON JSon JSoN")



    password = request.get_json().get("password")

    user = db.session.query(User).filter(User.id == id).first()

    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    user.password = pw_hash



    db.session.commit()

    return jsonify(user_schema.dump(user))



















if __name__ == "__main__":

    app.run(debug = True)
