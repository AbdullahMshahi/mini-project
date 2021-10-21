from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Project.db"
app.config['SECRET_KEY'] = '123456789'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Project(db.Model):
  SerialNo = db.Column(db.Integer, primary_key=True)
  title =db.Column(db.String(200), nullable=False)
  desc =db.Column(db.String(500), nullable=False)
  date_creating =db.Column(db.DateTime, default=datetime.utcnow)
 
#   def __repr__(self) -> str:
#      return f"{self.serialNo} -{self.tittle}"


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method =='POST': 
       title = request.form['title']
       desc =request.form['desc']
       project = Project(title=title, desc=desc)
       db.session.add(project)
       db.session.commit()
    allproject= Project.query.all()
    print("running")
    return render_template('Index.html', allproject=allproject)
  #retrun'Hello world!'


@app.route('/Show')
def products():
    allproject = Project.query.all()
    print(allproject)

    return 'This is products page'

@app.route('/delete/<int:SerialNo>')
def Delete(SerialNo):
    project = Project.query.get(SerialNo)
    db.session.delete(project)
    db.session.commit()

    return redirect(url_for("hello_world"))

@app.route('/update/<int:SerialNo>', methods=['GET', 'POST'])
def Update(SerialNo):
    allproject= Project.query.filter(Project.SerialNo == SerialNo).first() 
    print(allproject)
    if request.method=='POST':
       title = request.form['title']
       desc = request.form['desc']
       allproject.title = title
       allproject.desc = desc
       db.session.commit()
       return redirect('/')
    return render_template('update.html', allproject=allproject)

if __name__ == "__main__":
    app.run(debug=True)