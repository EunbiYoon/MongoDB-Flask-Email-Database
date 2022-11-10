#flask
from flask import Flask, request, render_template, jsonify, Response

#mongo
from random import randint
from flask_pymongo import PyMongo 


#forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email
import email_validator
class ContactForm(FlaskForm):
    name=StringField('NAME',validators=[DataRequired('A full name is required'),Length(min=5, max=30)])
    email=StringField('EMAIL',validators=[DataRequired('A correct email is required'),Email()])
    message=TextAreaField('MESSAGE',validators=[DataRequired('A message is required'),Length(min=5, max=500)])
    submit=SubmitField('SEND')

#flask
app=Flask(__name__)
app.config["SECRET_KEY"]="c54c76d0f1643a531b2109e24933bc59c20a3e06ab23d096"

#mongo
app.config["MONGO_URI"]="mongodb+srv://eunbiyoon:Ella135!@mydatabase.zrjfktg.mongodb.net/FlaskTutorial?retryWrites=true&w=majority"
mongo=PyMongo()
mongo.init_app(app)
db=mongo.db

#flask
@app.route("/",methods=["POST","GET"])
@app.route("/home",methods=["POST","GET"])
def hello_world():
    form=ContactForm()
    if request.method=="POST":

        #mongo
        name=form.name.data
        email=form.email.data
        message=form.message.data

        db.clients.insert_one({
            'clientid':randint(0,1000000),
            'clientname':name,
            'clientemail':email,
            'clientmessage':message
        })
        
        #flask
        print(name,email,message)
        form.name.data, form.email.data, form.message.data="","",""
        return render_template("index.html",form=form, success=True)
    return render_template("index.html",form=form)


@app.route("/project")
def project():
    return render_template("project.html")

@app.route("/components")
def components():
    return render_template("components.html")

#mongo
@app.route("/database", methods=["GET"])
def database():
    # clients=db.client.find_one() --> filter
    clients=db.clients.find()
    output=[{'id':client['clientid'], 'name':client['clientname'], 'email':client['clientemail'], 'message':client['clientmessage']} for client in clients]
    return jsonify({'output' : output})


#flask
if __name__ =="__main__":
    app.run()