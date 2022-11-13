from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Bhlohass*76@localhost/our_users'

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Name %r>' % self.name
    
class UserForm(FlaskForm):
   
    name = StringField('Name:', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit') 
    
     
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/user/add', methods=['GET','POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
            
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        
        flash('User Added Successfully!')
    our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html', 
                           form=form, 
                           name =name, 
                           our_users=our_users)
    
@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        try:
            db.session.commit()
            flash('User Updated Successfully')
            return render_template('update.html',
                                   form = form,
                                   name_to_update = name_to_update)
        except:
            db.session.commit()
            flash('Look like there was a problem, please try again!')
            return render_template('update.html',
                                   form = form,
                                   name_to_update = name_to_update)
    else: 
        return render_template('update.html',
                                   form = form,
                                   name_to_update = name_to_update,
                                   id=id)

@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('User Deleted Successfully')
        our_users = Users.query.order_by(Users.date_added)
        return render_template('add_user.html',
                                form = form,
                                name=name,
                                our_users=our_users)
    except:
        flash('Look like there was a problem, delete a user!')
        return render_template('add_user.html',
                                form = form,
                                name=name,
                                our_users=our_users)   
   
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
 
