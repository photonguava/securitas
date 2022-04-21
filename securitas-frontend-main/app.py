from flask import Flask,url_for,render_template,session,redirect,request
from authlib.integrations.flask_client import OAuth
from flask_sqlalchemy import SQLAlchemy
from configparser import ConfigParser
import requests
import docker
client = docker.from_env()

parser = ConfigParser()
parser.read('config.ini')

app = Flask(__name__)
app.secret_key = parser.get('APP','SECRET_KEY')
oauth = OAuth(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = parser.get('APP','SQLALCHEMY_DATABASE_URI')
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024

STAGING_URL = "http://localhost:8000"
STAGING_USERNAME = 'Likhith'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(150))
    audits = db.relationship('Audit', backref='user')

class Audit(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



google = oauth.register(
    name='google',
    client_id=parser.get('GOOGLE','CLIENT_ID'),
    client_secret=parser.get('GOOGLE','CLIENT_SECRET'),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)

"""
Google Oauth Implementation
"""
@app.route('/login')
def login():
    if 'email' in session:
        return redirect('/challenges')
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)



# OAUTH AUTH CALLBACK
@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    # do something with the token and profile
    registration_check = User.query.filter_by(email = user_info['email']).first()
    if registration_check:
        session['email'] = user_info['email']
        return redirect('/')
    else:
        user = User(
            name=user_info['name'],
            email = user_info['email'],
        )
        db.session.add(user)
        db.session.commit()
        session['email'] = user_info['email']
        return redirect('/')


@app.route('/')
def home():
    if "email" in session:
        return render_template('index.html',email=session['email'])
    else:
        return redirect(url_for('login'))


@app.route('/start',methods=["GET","POST"])
def start_project():
    """
    Intermediary screen to start a new project for the user
    """
    if request.method == "POST":
        return render_template('start_proj.html',scope=request.form['scope'])
    return render_template('start_proj.html',email=session['email'])

@app.route('/initiate_project',methods=["GET","POST"])
def initiate_project():
    """
    Make request to create a project and create project for current user.
    """
    project_details_dict = {'scope':request.form['scope'],'app_name':request.form['appname']}
    data = requests.post(STAGING_URL+"/projects",json = project_details_dict)
    client.containers.run('photonguava/scanner',environment=["project_id="+data.text,"target="+request.form['scope']],detach=True)
    return redirect(url_for('projects'))

    

@app.route('/projects')
def projects():
    """
    Display list of all projects with links to said projects
    """
    if "email" in session:
        data = requests.get(STAGING_URL+"/projects")
        print(data.json()[0])
        return render_template('projects.html',data = data.json(),email=session['email'])
    else:
        return redirect(url_for('login'))

@app.route('/project/<int:id>')
def project(id):
    """
    Display list of all vulnerabilities
    """
    data = requests.get(STAGING_URL+'/projects/'+str(id)+'/'+"vulnerabilities")
    print(data.json())
    return render_template('project.html',data = data.json(),email=session['email'])

@app.route('/vulnerability/<int:id>')
def vulnerability(id):
    """
    Display vulnerability details
    """
    data = requests.get(STAGING_URL+"/vulnerabilities/"+str(id))
    return render_template('vuln.html',vuln = data.json())

@app.route('/selenium')
def selenium():
    return "Selenium Test"

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)