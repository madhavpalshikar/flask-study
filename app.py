from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# setup app
app = Flask(__name__)

# sql lite setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# sqlite:/// - three slashes relative path
# sqlite://// - four slashes absolute path

# initializing databse
db = SQLAlchemy(app)

# create db model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<task %r>' % self.id


# setup routes
@app.route('/', methods=['POST','GET']) 
def index():  # defining function for that route
    if request.method == 'POST':
        task_content = request.form['content'] # retriving post data from request
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a issue!'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)
    

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a issue!'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a issue!'
    else:
        return render_template('update.html', task=task)

@app.route('/hello')
def helloWorld():
    return "Hello World"

if __name__ == '__main__':
    app.debug = True # monitor the changes in development
    app.run(host = '127.0.0.1', port = 5000)
