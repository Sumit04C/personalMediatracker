from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'


#Create SQLAlchemy instance
db = SQLAlchemy(app)

#Models 
class Volumes(db.Model): #change Profile to Book 
    id = db.Column(db.Integer, primary_key=True)
    series_name = db.Column(db.String(30), unique=False, nullable=False)
    volume_number = db.Column(db.Integer, nullable=False)
    volume_type = db.Column(db.String(20), unique=False, nullable=False )

    def __repr__(self):
        return f"Name : {self.series_name}, Age: {self.volume_number}"

#renders index page 
@app.route('/')
def index():
    volumes = Volumes.query.all()
    return render_template('index.html', volumes=volumes)
    # how does profiles=profiles work?

@app.route('/add_data')
def add_data():
    return render_template('add_book.html')

@app.route('/add', methods=["POST"])
def volume():
    series_name = request.form.get("series_name")
    volume_number = request.form.get("volume_number")
    volume_type = request.form.get("volume_type")

    if series_name != '' and volume_type != '' and volume_number is not None:
        p = Volumes(series_name=series_name, volume_number=volume_number, volume_type=volume_type)
        db.session.add(p)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')
    

@app.route('/delete/<int:id>')
def erase(id):
    data = db.session.get(Volumes, id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context(): #Needed for DB operations 
        db.create_all() #Creates the database and tables
    app.run(debug=True)