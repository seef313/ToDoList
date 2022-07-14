'''
Key Features:

User sign up/sign in

Create, edit, and delete to-dos

Set due-dates for to-dos

Ability to order to-dos

Marking to-dos as complete
'''
import models
from flask import Flask, redirect, url_for, render_template, request
from models import db, ToDO

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '\x14B~^\x07\xe1\x197\xda\x18\xa6[[\x05\x03QVg\xce%\xb2<\x80\xa4\x00'
app.config['DEBUG'] = True

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
db.create_all()


todo = models.ToDO(db.Model)

#print(tasks)
@app.route("/")
def index():
    '''
    Home page
    ''' 
    #tasks = models.ToDO(db.Model)

    tasks = models.ToDO(db.Model).query.all()
    return render_template('index.html',tasks=tasks)
    #return "Hello World"



@app.route('/task', methods=['POST'])
def add_task():
    item = request.form['item']
    if not item:
        return 'Error'
    new_task = ToDO(item)
    db.session.add(new_task)    
    db.session.commit()
    return redirect('/')


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = ToDO.query.get(task_id)
    if not task:
        return redirect('/')

    db.session.delete(task)
    db.session.commit()
    return redirect('/')


@app.route('/done/<int:task_id>')
def resolve_task(task_id):
    task = ToDO.query.get(task_id)

    if not task:
        return redirect('/')
    if task.done:
        task.done = False
    else:
        task.done = True

    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(port=3000)