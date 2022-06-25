import re
from turtle import title
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_BINDS'] = {
    'todocomment':  'sqlite:///todocomment.db',
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Todo(db.Model):
    sr_no = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sr_no} - {self.title}"

class Todocomment(db.Model):
    __bind_key__ = 'todocomment'
    sr_no = db.Column(db.Integer, primary_key = True)
    todo_id = db.Column(db.Integer, nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    

    def __repr__(self) -> str:
        return f"{self.sr_no} - {self.desc}"

@app.route("/" ,methods=['GET','POST'])
def hello_world():
    if request.method == 'POST':
        # print(request.form['title'])
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    print((allTodo))
    return render_template('index.html', allTodo=allTodo)

@app.route("/show")
def show_todo():
    
    return 'Hyy'

@app.route('/delete/<int:sr_no>')
def delete(sr_no):
    todo = Todo.query.filter_by(sr_no=sr_no).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:sr_no>', methods=['GET', 'POST'])
def update(sr_no):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sr_no=sr_no).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
        
    todo = Todo.query.filter_by(sr_no=sr_no).first()
    return render_template('update.html', todo=todo)

@app.route('/comment/<int:sr_no>', methods=['GET', 'POST'])
def comment(sr_no):
    
    if request.method=='POST':
        desc = request.form['desc']
        # todo = Todo.query.filter_by(sr_no=sr_no).first()
        todo1 = Todocomment(desc=desc, todo_id = sr_no)
        db.session.add(todo1)
        db.session.commit()
        # print(todo,99)
        # return redirect("/")
        
    todo = Todo.query.filter_by(sr_no=sr_no).first()
    comments = Todocomment.query.filter_by(todo_id=sr_no).all()
    return render_template('comment.html', todo=todo, comments=comments)

if __name__ == '__main__':
    app.run(debug=True,port=8000)