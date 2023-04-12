#Importing necessary libraries
from application import app,db,api,jwt
from flask import render_template, jsonify, json
from application.models import users,courses
from flask_restx import Resource
from flask_jwt_extended import create_access_token,jwt_required

#Creating a namespace for our API
ns = api.namespace('api', description='My API')

@ns.route('/users')
class GetAndPostUser(Resource):
    def get(self):
        # Get all users and exclude password field
        return jsonify(users.objects.exclude('password'))
    
    def post(self):
        # Get request data from payload
        data=api.payload
        #increment user_id+1 and generate it automatically
        userid=users.objects.count()
        userid+=1
        # Create a new user and hash password
        user=users(user_id=userid,name=data['name'],email=data['email'])
        user.set_password(data['password'])
        user.save()
        return jsonify(users.objects(user_id=userid))
    
@ns.route('/users/<idx>')
class GetUpdateDeleteUser(Resource):
    def get(self,idx):
        # Get user object by user_id and exclude password field
        user = users.objects.exclude('password').get(user_id=idx)
        # Serialize user object to JSON
        user_json = json.loads(user.to_json())
        return jsonify(user_json)

    def put(self,idx):
        # Get request data from payload
        data = api.payload
        user = users.objects(user_id=idx).first()
        # Verify user with password and then update user details
        if not user.get_password(data['password']):
            return jsonify({"error": "Incorrect password, Cant Update!"})
        else:
            # Exclude password field from update
            data.pop('password', None)
            # Update user object with new values
            users.objects(user_id=idx).update(**data)
            # Get updated user object and exclude password field
            userwithoutpassword = users.objects.exclude('password').get(user_id=idx)
            # Serialize user object to JSON
            user_json = json.loads(userwithoutpassword.to_json())
            return jsonify(user_json)
    
    def delete(self, idx):
        # Get request data from payload
        data = api.payload
        user = users.objects(user_id=idx).first()
        # Verify user with password and then delete user account
        if not user.get_password(data['password']):
            return jsonify({"error": "Incorrect password"})
        else:
            user.delete()
            return jsonify("User is deleted!")
    
@ns.route('/users/<idx>/updatepassword')
class UpdateUserpassword(Resource):
    def put(self,idx):
        # Get request data from payload
        data=api.payload
        user=users.objects(user_id=idx).first()
        # Verify user with old password and then update new password
        if not user:
            return {'message': 'User not found'}, 404
        
        if not user.get_password(data['old_password']):
            return {'message': 'Incorrect password'}, 401
        
        user.set_password(data['new_password'])
        user.save()
        
        return {'message': 'User password updated successfully'}, 200
    
@ns.route('/login')
class Login(Resource):
    def post(self):
        # Get request data from payload
        data=api.payload
        user=users.objects(email=data['email']).first()
        
        if not user or not user.get_password(data['password']):
            return {'message': 'Invalid credentials'}, 401
        
        else:
            # Create access token for user
            access_token = create_access_token(identity=str(user.user_id))
            return {'access_token': access_token}, 200

@ns.route('/signout')
class SignOut(Resource):
    @jwt_required() # add this if you're using JWT for authentication
    def post(self):
        # Delete access token from client-side
        # Return success message
        return {'message': 'Logged out successfully'}, 200


#Defining endpoints for getting and posting courses
@ns.route('/courses')
class GetAndPost(Resource):
    def get(self):
        return jsonify(courses.objects.all())
    
    def post(self):
        data=api.payload
        course=courses(courseID=data['courseID'],title=data['title'],description=data['description'],credits=data['credits'],term=data['term'])
        course.save()
        return jsonify(courses.objects(courseID=data['courseID']))

#Defining endpoints for getting, updating and deleting courses by ID
@ns.route('/courses/<idx>')
class GetUpdateDelete(Resource):
    def get(self,idx):
        return jsonify(courses.objects(courseID=idx))
    
    def put(self,idx):
        data=api.payload
        courses.objects(courseID=idx).update(**data)
        return jsonify(courses.objects(courseID=idx))
    
    def delete(self,idx):
        courses.objects(courseID=idx).delete()
        return jsonify("Course is deleted!")
    
#Defining the route for the index page
@app.route("/")
@app.route("/index/")
def index():
    return render_template("index.html")