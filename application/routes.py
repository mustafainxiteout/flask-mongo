#Importing necessary libraries
from application import app,db,api
from flask import render_template, jsonify
from application.models import courses
from flask_restx import Resource

#Creating a namespace for our API
ns = api.namespace('api', description='My API')

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
    return render_template("index.html",login=False)