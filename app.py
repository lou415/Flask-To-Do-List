# beginning to write the most basic flask application you can. 
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
# creates an instance of the flask class: Flask().
# this handles the requests, routing, configs, etc.
# __name__ = constructor variable that holds the name of this .py file.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# initialize the database
db = SQLAlchemy(app)

# initialize a model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    # the nullable field makes it so a new task can't be created
    # and left blank. It's not nullable (not able to be null). 
    content = db.Column(db.String(200), nullable = False)
    completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return '<Task %r>' % self.id


# this is the route definition.
@app.route('/', methods = ['POST', 'GET'])
# when the main web address is visited, Flask runs the index
# function, then the func tells the browser to display the 
# string.
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content = task_content) # type: ignore
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding the task to the db. Try again."
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks = tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting that task."

@app.route('/update/<int:id>', methods=["GET", "POST"])
def update(id):
    task_to_update = Todo.query.get_or_404(id)
    if request.method == "POST":
        task_to_update.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating the task.'
    else:
        return render_template('update.html', task = task_to_update)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)