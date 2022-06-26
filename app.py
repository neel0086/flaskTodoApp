import re
from turtle import title
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_BINDS'] = {
    'todologin': 'sqlite:///todologin.db',
    'todocomment':  'sqlite:///todocomment.db',
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Todo(db.Model):
    sr_no = db.Column(db.Integer, primary_key = True)
    todo_user = db.Column(db.String(500), nullable = False)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sr_no} - {self.title}"

class Todocomment(db.Model):
    __bind_key__ = 'todocomment'
    
    sr_no = db.Column(db.Integer, primary_key = True)
    todo_id = db.Column(db.Integer, nullable = False)
    todo_user = db.Column(db.String(500), nullable = False)
    todo_admin = db.Column(db.String(20), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class Todologin(db.Model):
    __bind_key__ = 'todologin'
    sr_no = db.Column(db.Integer, primary_key = True)
    
    todo_user = db.Column(db.String(20), nullable = False)
    passw = db.Column(db.String(500), nullable = False)
    

    # def __repr__(self) -> str:
    #     return f"{self.sr_no} - {self.desc}"

@app.route("/" ,methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        passw = request.form['pass']
        data = Todologin.query.filter_by(todo_user=username, passw=passw).first()
        if data is not None:
            session['logged_in'] = True
            session['user'] = data.todo_user
            return redirect(data.todo_user+'/home')
        else:
            return render_template('login.html')
        # todolog = Todologin(todo_user=username, passw=passw)
        # db.session.add(todolog)
        # db.session.commit()  
    else:
        return render_template('login.html')

@app.route("/register" ,methods=['GET','POST'])
def register():
    
    if request.method == 'POST':
        try:
            utodo=Todologin(todo_user=request.form['username'], passw=request.form['pass'])
            db.session.add(utodo)
            db.session.commit()
            return redirect(url_for('login'))
        except:
            return render_template('register.html', message="User Already Exists")
    else:
        
        return render_template('register.html')
@app.route("/<username>/home" ,methods=['GET','POST'])
def home(username):
    # print(mssg)
    user = session['user']
    if request.method == 'POST':
        print(9)
        todo_user = user
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc, todo_user=todo_user)
        db.session.add(todo)
        db.session.commit()
    else:
        allTodo = Todo.query.filter_by(todo_user=username).all()
        return render_template('index.html', allTodo=allTodo,utodo=username ,flag=(user==username))



@app.route('/<username>/delete/<int:sr_no>')
def delete(sr_no,username):
    if username!=session['user']:
        return render_template('errorpage.html')
    else:
        todo = Todo.query.filter_by(sr_no=sr_no).first()
        db.session.delete(todo)
        db.session.commit()
        return redirect('/'+username+'/home')

@app.route('/<username>/update/<int:sr_no>', methods=['GET', 'POST'])
def update(sr_no,username):
    if username!=session['user']:
        return render_template('errorpage.html')
    else:
        if request.method=='POST':
            title = request.form['title']
            desc = request.form['desc']
            todo = Todo.query.filter_by(sr_no=sr_no).first()
            todo.title = title
            todo.desc = desc
            db.session.add(todo)
            db.session.commit()
            return redirect('/'+username+'/home')
            
        todo = Todo.query.filter_by(sr_no=sr_no).first()
        return render_template('update.html', todo=todo)

@app.route('/<username>/comment/<int:sr_no>', methods=['GET', 'POST'])
def comment(sr_no,username):
    user = session['user']
    if request.method=='POST':
        desc = request.form['desc']
        todo_user = user
        todo1 = Todocomment(desc=desc, todo_id = sr_no, todo_user=todo_user,todo_admin=username)
        db.session.add(todo1)
        db.session.commit()
        
    # todo = Todo.query.filter_by(todo_user=username,sr_no=sr_no).first()
    comments = Todocomment.query.filter_by(todo_admin=username,todo_id=sr_no).all()
    obj=[username,sr_no]
    print(user)
    return render_template('comment.html', session_user=obj,s_user=user, comments=comments)

@app.route('/<username>/comment/<int:sr_no>/delete/<int:csr_no>', methods=['GET', 'POST'])
def comment_delete(sr_no,username,csr_no):
    user = session['user']
    
    todo = Todocomment.query.filter_by(sr_no = csr_no,todo_id=sr_no, todo_admin=username, todo_user=user).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/'+username+'/comment'+'/'+str(sr_no))



if __name__ == '__main__':
    app.secret_key = "SecretCantBeSecret:;lol"
    app.run(debug=True,port=8000)