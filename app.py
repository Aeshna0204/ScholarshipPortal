from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///scholarshipinfo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Info(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    sch_name=db.Column(db.String(20),nullable=False)
    sch_type=db.Column(db.String(20),nullable=False)
    sch_desc=db.Column(db.String(200),nullable=False)
    deadline=db.Column(db.String(15),nullable=False)
    
    def __repr__(self) -> str:
        return f"{self.sno}-{self.sch_name}"

@app.route("/",methods=['GET','POST'])
def index():
    aeshna_object=Info.query.all()
    return render_template('index.html',bhavik_object=aeshna_object)

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        email_id=request.form['aeshna']
        passcode=request.form['jain']
        if email_id=='aeshnajain20760@acropolis.in' and passcode=='internship':
            return redirect('/admin')

    return render_template('login.html')
    
@app.route("/admin",methods=['GET','POST'])
def admin():
    if request.method=='POST':
        sch_name_obtained_from_form=request.form['sch_name']
        sch_type_obtained_from_form=request.form['sch_type']
        deadline_obtained_from_form=request.form['deadline']
        sch_desc=request.form['sch_desc']
        aeshna_object=Info(sch_name=sch_name_obtained_from_form,sch_type=sch_type_obtained_from_form,deadline=deadline_obtained_from_form,sch_desc=sch_desc)    
        db.session.add(aeshna_object)
        db.session.commit()
    
    list__=Info.query.all()
    return render_template('/admin.html',list__=list__)
    
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        sch_name=request.form['sch_name']
        sch_type = request.form['sch_type']
        deadline=request.form['deadline']
        _object_ = Info.query.filter_by(sno=sno).first()
        _object_.sch_name = sch_name
        _object_.sch_type=sch_type
        _object_.deadline=deadline
        db.session.add(_object_)
        db.session.commit()
        return redirect("/admin")
        
    anobject = Info.query.filter_by(sno=sno).first()
    return render_template('update.html', anobject=anobject)

@app.route('/delete/<int:sno>', methods=['GET', 'POST'])
def delete(sno):
    todo = Info.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/admin")

if __name__=="__main__":
    app.run(debug=True,port=5050)