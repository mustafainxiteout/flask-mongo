#Importing necessary libraries
from application import app,db,api,jwt,mail,serializer
from flask import render_template, jsonify, json, redirect, flash, url_for, request
from application.models import users,courses
from flask_restx import Resource,fields
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_jwt_extended import create_access_token,jwt_required,get_jwt

#Creating a namespace for our API
ns = api.namespace('users', description='Users')

# Define the expected payload using the 'fields' module
user_model = ns.model('User', {
    'name': fields.String(required=True, description='enter your name'),
    'email': fields.String(required=True, description='enter your email id'),
    'password': fields.String(required=True, description='enter your password')
})

login_model = ns.model('Login', {
    'email': fields.String(required=True, description='enter your email id'),
    'password': fields.String(required=True, description='enter your password')
})

password_model = ns.model('Password', {
    'password': fields.String(required=True, description='enter your password')
})

forgot_password_model = ns.model('ForgotPassword', {
    'email': fields.String(required=True, description='enter your email id'),
    'new_password': fields.String(required=True, description='enter your new password')
})

update_password_model = ns.model('UpdatePassword', {
    'old_password': fields.String(required=True, description='enter your old password'),
    'new_password': fields.String(required=True, description='enter your new password')
})

reverify_model = ns.model('Reverify', {
    'email': fields.String(required=True, description='enter your email id')
})

course_model = ns.model('Course', {
    'courseID': fields.String(required=True, description='enter your courseID'),
    'title': fields.String(required=True, description='enter your title'),
    'description': fields.String(required=True, description='enter your description'),
    'credits': fields.Integer(required=True, description='enter your credits'),
    'term': fields.String(required=True, description='enter your term')
})


@ns.route('')
class GetAndPostUser(Resource):
    def get(self):
        # Get all users and exclude password field
        return jsonify(users.objects.exclude('password','verified'))
    
    @ns.expect(user_model)  # Use the 'expect' decorator to specify the expected payload
    def post(self):
        # Get request data from payload
        data=api.payload
        #increment user_id+1 and generate it automatically
        max_user_id = users.objects.aggregate({"$group": {"_id": None, "max_user_id": {"$max": "$user_id"}}}).next().get("max_user_id")
        userid = max_user_id + 1
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
            # Render the email template with the verify URL
            html_body = render_template('verify_email.html', verify_url=verification_url, subject='Verify your account', button='VERIFY ACCOUNT',content='We are happy you signed up for Inxiteout. To start exploring Courses App, please confirm your email address.',caption='Didn’t create account')
            # create message and send email
            message = Message('Verify Your Email', recipients=[emailid])
            message.html = html_body
            mail.send(message)
            return {'message': 'Please click on the Verification Link Sent to mail'}, 200
        elif users.objects(email=data['email']).first():
            return {'message': 'User Account already register'}, 401
        else:
            return {'message': 'Error occured'}, 401

    
@ns.route('/<idx>')
class GetUpdateDeleteUser(Resource):
    def get(self,idx):
        # Get user object by user_id and exclude password field
        user = users.objects.exclude('password').get(user_id=idx)
        # Serialize user object to JSON
        user_json = json.loads(user.to_json())
        return jsonify(user_json)
    
    @ns.expect(user_model)  # Use the 'expect' decorator to specify the expected payload
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
    
    @ns.expect(password_model)  # Use the 'expect' decorator to specify the expected payload
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
    
@ns.route('/<idx>/updatepassword')
class UpdateUserpassword(Resource):
    @ns.expect(update_password_model)  # Use the 'expect' decorator to specify the expected payload
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
    
@ns.route('/reverify')
class Reverify(Resource):
    @ns.expect(reverify_model)  # Use the 'expect' decorator to specify the expected payload
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
            # Render the email template with the reverify URL
            html_body = render_template('verify_email.html', verify_url=verification_url, subject='Verify your account',button='VERIFY ACCOUNT',content='We are happy you signed up for Inxiteout. To start exploring Courses App, please confirm your email address.',caption='Didn’t create account')
            # create message and send email
            message = Message('Verify Your Email', recipients=[emailid])
            message.html = html_body
            mail.send(message)
            return {'message': 'Please click on the Verification Link Sent to mail'}, 200
        
@ns.route('/forgot_password')
class ForgotPassword(Resource):
    @ns.expect(forgot_password_model)  # Use the 'expect' decorator to specify the expected payload
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
            # Render the email template with the reverify URL
            html_body = render_template('verify_email.html', verify_url=reset_url, subject='Forgot your Password', button='RESET PASSWORD', content='We noticed that you have requested to reset your password for your Inxiteout account. To proceed with this request, please click on the password reset button below.', caption='Didn’t reset password')
            # Create message and send email
            message = Message('Reset Your Password', recipients=[data['email']])
            message.html = html_body
            mail.send(message)
            return {'message': 'Please check your email for password reset instructions'}, 200        
    
@ns.route('/login')
class Login(Resource):
    @ns.expect(login_model)  # Use the 'expect' decorator to specify the expected payload
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

#Creating a namespace for our API
ns2 = api.namespace('courses', description='Courses')

#Defining endpoints for getting and posting courses
@ns2.route('')
class GetAndPost(Resource):
    def get(self):
        return jsonify(courses.objects.all())
    
    @ns2.expect(course_model)  # Use the 'expect' decorator to specify the expected payload
    def post(self):
        data=api.payload
        course=courses(courseID=data['courseID'],title=data['title'],description=data['description'],credits=data['credits'],term=data['term'])
        course.save()
        return jsonify(courses.objects(courseID=data['courseID']))

#Defining endpoints for getting, updating and deleting courses by ID
@ns2.route('/<idx>')
class GetUpdateDelete(Resource):
    def get(self,idx):
        return jsonify(courses.objects(courseID=idx))
    
    @ns2.expect(course_model)  # Use the 'expect' decorator to specify the expected payload
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