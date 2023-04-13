#Importing necessary libraries
from application import app,db,api,jwt,mail,serializer
from flask import render_template, jsonify, json, redirect, flash, url_for, request
from application.models import users,courses
from flask_restx import Resource
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_jwt_extended import create_access_token,jwt_required,get_jwt

#Creating a namespace for our API
ns = api.namespace('api', description='My API')

@ns.route('/users')
class GetAndPostUser(Resource):
    def get(self):
        # Get all users and exclude password field
        return jsonify(users.objects.exclude('password','verified'))
    
    def post(self):
        # Get request data from payload
        data=api.payload
        #increment user_id+1 and generate it automatically
        userid=users.objects.count()
        userid+=1
        if not users.objects(email=data['email']).first():
            # Create a new user and hash password and then send verification link to mail
            verified=False
            user=users(user_id=userid,name=data['name'],email=data['email'],verified=verified)
            user.set_password(data['password'])
            user.save()
            emailid=data['email']
            token = serializer.dumps(emailid, salt='email-verification') 
            # create verification URL with token
            verification_url = f'http://localhost:8000/verify_email/{token}'
            # create message and send email
            message = Message('Verify Your Email', recipients=[emailid])
            message.body = f'Click the following link to verify your email: {verification_url}'
            mail.send(message)
            return {'message': 'Please click on the Verification Link Sent to mail'}, 200
        elif users.objects(email=data['email']).first():
            return {'message': 'User Account already register'}, 401
        else:
            return {'message': 'Error occured'}, 401

    
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
        elif user.verified==False:
            return jsonify({"error": "Not verified, Cant Update!"})
        else:
            # Exclude password field from update
            data.pop('password', None)
            # Update user object with new values
            users.objects(user_id=idx).update(**data)
            # Get updated user object and exclude password field
            userwithoutpassword = users.objects.exclude('password','verified').get(user_id=idx)
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
        elif user.verified==False:
            return jsonify({"error": "Not verified, Cant Delete!"})
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
        
        if user.verified==False:
            return jsonify({"error": "Not verified, Cant Update!"})
        
        user.set_password(data['new_password'])
        user.save()
        
        return {'message': 'User password updated successfully'}, 200
    
@ns.route('/users/reverify')
class Reverify(Resource):
    def post(self):
        # Get request data from payload
        data=api.payload
        user=users.objects(email=data['email']).first()
        if not user:
            return {'message': 'Invalid User'}, 401
        else:
            emailid=data['email']
            token = serializer.dumps(emailid, salt='email-verification') 
            # create verification URL with token
            verification_url = f'http://localhost:8000/verify_email/{token}'
            # create message and send email
            message = Message('Verify Your Email', recipients=[emailid])
            message.body = f'Click the following link to verify your email: {verification_url}'
            mail.send(message)
            return {'message': 'Please click on the Verification Link Sent to mail'}, 200
        
@ns.route('/forgot_password')
class ForgotPassword(Resource):
    def post(self):
        # Get request data from payload
        data = api.payload
        user = users.objects(email=data['email']).first()
        if not user:
            return {'message': 'Invalid User'}, 401
        else:
            # Generate password reset token
            token = serializer.dumps(data, salt='password-reset')
            # Create password reset URL with token
            reset_url = f'http://localhost:8000/reset_password/{token}'
            # Create message and send email
            message = Message('Reset Your Password', recipients=[data['email']])
            message.body = f'Click the following link to reset your password: {reset_url}'
            mail.send(message)
            return {'message': 'Please check your email for password reset instructions'}, 200        
    
@ns.route('/login')
class Login(Resource):
    def post(self):
        # Get request data from payload
        data=api.payload
        user=users.objects(email=data['email']).first()
        
        if not user or user.verified==False or not user.get_password(data['password']):
            return {'message': 'Invalid credentials'}, 401
        
        else:
            # Create access token for user
            access_token = create_access_token(identity=str(user.user_id))
            return {'access_token': access_token}, 200

#BLOCKLIST = set()

@ns.route('/signout')
class SignOut(Resource):
    @jwt_required() # add this if you're using JWT for authentication
    def post(self):
        # Delete access token from client-side
        #jti = get_jwt()['jti']
        #BLOCKLIST.add(jti)
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

# define an endpoint to verify email
@app.route('/verify_email/<token>', methods=['GET'])
def verify_email(token):
    try:
        email = serializer.loads(token, salt='email-verification', max_age=3600)
        user=users.objects(email=email).first()
        if user:
            user.verified=True
            user.save()
        return jsonify({'message': 'Your account is been Verified now!'}), 200
    except SignatureExpired:
        return jsonify({'message': 'Verification link has expired.'}), 400
    except BadSignature:
        return jsonify({'message': 'Invalid verification link.'}), 400
    
    # define an endpoint to verify email and password
@app.route('/reset_password/<token>', methods=['GET'])
def reset_password(token):
    try:
        data = serializer.loads(token, salt='password-reset', max_age=3600)
        user=users.objects(email=data['email']).first()
        if user:
            user.set_password(data['new_password'])
            user.save()
        return jsonify({'message': 'Your account Password is been Updated now!'}), 200
    except SignatureExpired:
        return jsonify({'message': 'Verification link has expired.'}), 400
    except BadSignature:
        return jsonify({'message': 'Invalid verification link.'}), 400