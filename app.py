'''here ill give edit and add and delete  and upload too posts option for the admin'''
from flask import Flask, render_template , request, session, redirect, send_from_directory, url_for, Response, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, text
import json
from datetime import datetime #ill use this to pass current date in the form
# from flask_mail import Mail #using to send email
# notification//////
from flask_mailman import Mail, EmailMessage #using to send email notification
from flask_ckeditor import CKEditor

import os
from werkzeug.utils import secure_filename
import math

'''we can use the json file here to add our own parameters'''
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(BASE_DIR, "config.json")
print(f"CONFIG_PATH:{config_path}")
with open(config_path,'r') as c: #reading from json file the urls
    params = json.load(c)['params']

local_server = params["local_server"]
app = Flask(__name__)
app.secret_key = 'supersecretkey' #kuch bhi rakh skte ho
app.config['UPLOAD_FOLDER'] = params['upload_location']
#setting up email notification////
mail = Mail()
app.config["MAIL_SERVER"]= "smtp.fastmail.com"
app.config["MAIL_PORT"]= 465
app.config["MAIL_USERNAME"]= params['mail-user']
app.config["MAIL_PASSWORD"]=params['mail-password']
app.config["MAIL_USE_TLS"]= False
app.config["MAIL_USE_SSL"]= True
mail.init_app(app)

app.config['CKEDITOR_SERVE_LOCAL'] = True   # serve local JS
app.config['CKEDITOR_HEIGHT'] = 400         # default height
app.config['CKEDITOR_FILE_UPLOADER'] = 'uploader'  # upload endpoint

# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_HOST_USER = "tanmayakumarnaik2003@gmail.com"
# EMAIL_HOST_PASSWORD = 'xidjjstjrizbznuy'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
# mail = Mail(app)

# app.config.update(
#     MAIL_SERVER = 'smtp.gmail.com',
#     MAIL_PORT = '465', #587,465
#     MAIL_USER_SSL = True,
#     MAIL_USER_TLS = False,
#     MAIL_USERNAME = 'tanmayakumarnaik@gmail.com',
#     MAIL_PASSWORD ='xidjjstjrizbznuy'
# )
# mail = Mail(app)
#-----------------------------------------#

#----------connecting to the sqlachemy database--------#
if (local_server):
    app.config["SQLALCHEMY_DATABASE_URI"] = params['local_uri']#'mysql://root:@localhost/deploid'
    # app.config[""]
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['prod_uri']#"mysql://root:@localhost/deploid"

db = SQLAlchemy(app)
ckeditor = CKEditor(app)
#--------------------------------------#
class Contacts(db.Model):
    '''
    sno,name,phone_num,msg,date,email
    '''
    sno= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_no = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(20), nullable=False)

class Posts(db.Model):
    '''
    sno,name,phone_num,msg,date,email
    '''
    sno= db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tag_line = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500), nullable=False, default="Tan's Bloppost")
    date =  db.Column(db.DateTime, default=datetime.now())
    last_modified = db.Column(db.DateTime, nullable=True)
    img_file = db.Column(db.String(120), nullable=True)

def get_blog_posts():
    query = text("SELECT slug, date FROM posts")
    result = db.session.execute(query)
    return [{"slug": row.slug, "lastmod": row.date.date().isoformat()} for row in result]


# Define restricted URLs that should not be included in the sitemap
EXCLUDED_ROUTES = {'/dashboard', '/uploader', '/logout'}

# Sitemap route
@app.route('/sitemap.xml')
def sitemap():
    pages = []

    # Add static pages
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            url = url_for(rule.endpoint, _external=True)
            if rule.rule not in EXCLUDED_ROUTES:
                pages.append({"loc": url, "lastmod": datetime.now().date().isoformat()})

    # Add dynamic blog posts
    for post in get_blog_posts():
        url = url = url_for('post_route', post_slug=post['slug'], _external=True)
        pages.append({"loc": url, "lastmod": post["lastmod"]})

    # Render XML template
    sitemap_xml = render_template("sitemap_template.xml", pages=pages)
    return Response(sitemap_xml, mimetype="application/xml")

@app.route("/robots.txt")
def robots_txt():
    return send_from_directory(app.static_folder, "robots.txt", mimetype="text/plain")

#added ads.txt
@app.route('/ads.txt')
def ads_txt():
    return send_from_directory(app.static_folder, 'ads.txt', mimetype='text/plain')

# Load Browser Favorite Icon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/logout")
def logout():
    if 'user' in session and session['user'] == params['admin_name']:
        session.pop('user')
    return redirect('/dashboard')

#here we can upload file to the params['upload_location'] in config.json///
@app.route("/uploader",methods=['GET','POST'])
def uploader():
    if 'user' in session and session['user'] == params['admin_name']:
        if (request.method == 'POST'):
            f = request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
            # Return JSON for CKEditor to insert image
            url = url_for('static', filename=f"uploads/{f.filename}")
            return {"uploaded": 1, "fileName": f.filename, "url": url}

@app.route("/delete/<string:sno>",methods=['GET','POST'])
def delete(sno):
    if 'user' in session and session['user'] == params['admin_name']:
        posts = Posts.query.filter_by(sno=sno).first()
        db.session.delete(posts)
        db.session.commit()
    return redirect('/dashboard')

#here i can edit delete or add the posts in the db from the webpage//////////
@app.route("/edit/<string:sno>",methods=['GET','POST'])
def edit(sno):
    if 'user' in session and session['user'] == params['admin_name']:
        print(f"inside edit: {sno}")
        if request.method == "POST":
            box_title = request.form.get('title')
            tagline = request.form.get('tline')
            description = request.form.get('description')
            slug = request.form.get('slug')
            content = request.form.get('content')
            img_file = request.form.get('img_file')
            date = datetime.now()
            # print(posts.sno)

            if sno == '0': #adding post at /edit/0
                post = Posts(title = box_title, slug=slug, content=content, tag_line=tagline,description=description, img_file=img_file, date=date)
                db.session.add(post)
                db.session.commit()
            else:
                post = Posts.query.filter_by(sno=sno).first()
                post.title = box_title
                post.slug = slug
                post.content = content
                post.tag_line = tagline
                post.description = description
                post.img_file = img_file
                post.last_modified = date
                db.session.commit()
                return redirect('/edit/'+sno)
        if (sno != 0):
            posts = Posts.query.filter_by(sno=sno).first()
        # print(posts.sno)
        return render_template('edit.html', params=params, posts=posts, sno=sno)
    else:
        return "ADMIN needs to login"

# http://127.0.0.1:5000/dashboard
@app.route("/dashboard",methods=['GET','POST'])
def dashboard():
    if 'user' in session and session['user'] == params['admin_name']: #if user is already in session render the dashboard.html
        posts = Posts.query.all()
        return render_template('dashboard.html',params = params, posts=posts)
    if (request.method == 'POST'): #post request to admin login
        username = request.form.get('uname')
        # print(username)
        password = request.form.get('pass')
        # print(password)
        if (username == params['admin_name'] and password == params['admin_password']): #if credentials are true let the admin in and render dashboard.html
            #set a session variable
            session['user'] = username #shows the current session
            posts = Posts.query.all()
            return render_template('dashboard.html',params = params, posts=posts)
        else:
            return "WRONG CREDENTIALS"
    else:
        # print("wrong pass")
        return render_template('login.html',params= params) #if credentials are false or not logged in yet keep him on the login.html

# http://127.0.0.1:5000
@app.route("/")
def home():
    '''------------------///////////////////pagination////////////--------------------'''
    posts = Posts.query.order_by(desc(Posts.date)).all()
    last = math.ceil(len(posts)/int(params['no_of_posts']))
    page = request.args.get('page')
    if (not str(page).isnumeric()):
        page = 1
    page = int(page)
    posts = posts[(page-1)*int(params['no_of_posts']):(page-1)*int(params['no_of_posts'])+ int(params['no_of_posts'])]
    if page == 1:
        prev = "#"
        next = "/?page=" + str(page+1)
    elif page == last:
        prev = "/?page=" + str(page-1)
        next = "#"
    else:
        prev = "/?page=" + str(page-1)
        next = "/?page=" + str(page+1)

    return render_template('index.html',params= params,posts=posts, prev=prev, next=next)#params=params passing data mentioned in config.json to be used for the link in <a href>
#------------------------------------------------------------------------------------------#

# http://127.0.0.1:5000/about

@app.route("/blog/<string:post_slug>",methods=['GET'])
# https://www.codewithharry.com/videos/web-dev-using-flask-and-python-1/ , "/web-dev-using-flask-and-python-1/" HERE THIS IS A SLUG
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first() #fetching data form dbms as a dictionary, i have used this to show in post.html
    if not post:
        abort(404)  # Return proper 404 instead of 500
    return render_template('post.html',params= params,post=post)#params=params passing data mentioned in config.json

@app.route("/about")
def about():
    return render_template('about.html',params= params) #params=params passing data mentioned in config.json

# http://127.0.0.1:5000/bootstrap
@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    sendStatus = {'val': 0}
    if (request.method == 'POST'):
        '''add entry to the database'''
        ##fetching entries
        name = request.form.get('name') #'''in quotes are the name of the <input class> in contact.html <form> section'''
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        ##adding to database
        '''
        sno,name,phone_num,msg,date,email
        '''
        entry = Contacts(name=name,phone_no = phone, msg=message, email=email, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        print("Message sent to admin.")
        sendStatus['val'] = 1

        # try:
        #     msg = EmailMessage(
        #     "Message from DEPLOID",
        #     f"{name}\n{message}\n{phone}\n{email}",
        #     params['mail-user'],
        #     [params['mail-receiver']]
        #     )
        #     msg.send()
        # except:
        #     print("FAILED TO SEND EMAIL TO ADMIN.")

        # mail.send_message('New message from'+ name,
        #                   sender='tanmayakumarnaik2003@gmail.com',
        #                   recipients = ["tancannonrobotics@gmail.com"],
        #                   body = message + "\n" + phone + "\n" + email)
        # return render_template('index.html',params=params)
    return render_template('contact.html',params= params, sendStatus = sendStatus)#params=params passing data mentioned in config.json

# Custom 404 error handler
@app.errorhandler(404)
def notFound(request):
    return render_template("404.html", params=params)

# Custom 500 error handler (optional for server errors)
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html", params=params), 500

if __name__ == "__main__":
    app.run(debug=params['app_debug_mode'])
