import os, json, random
from flask import Flask, render_template, redirect, url_for, request
from models import db,Blog,Author,Tag,RoundType,Round
from forms import BlogForm

TEMPLATE_DIR = os.path.join("..", "templates")
STATIC_DIR = os.path.join("..", "static")

app = Flask(__name__, template_folder = TEMPLATE_DIR, static_folder = STATIC_DIR)

SECRET_KEY = "hlsdgsf-sldjkeb67593"
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)

# Home Page
@app.route('/')
def home():
    return render_template('home.j2', title = '')

# Listing the blogs
@app.route('/blogs')
def blogList():
    # tags should always include all distinct company name (do it while inserting in database)
    # Published at should store time gap
    # Only need to send these columns.
    blogs = [{'id': '3434', 'title' : 'First blog',
        'content' :  'hello my name is blah blah blah, welcome to blah blah blah',
        'published_at': '2 days ago', 'tags': ['google', 'facebook', 'help', 'hello', 'bye', 'hehe', 'wtf', 'last'],
        'author': 'thelethalcode'},
        {'id': '3434', 'title' : 'Second Blog',
        'content' :  'hello my name is blah blah blah, welcome to blah blah blah',
        'published_at': '2 days ago', 'tags': ['google', 'facebook', 'help', 'hello', 'bye', 'hehe'],
        'author': 'fugazi'}]

    allTags = ['google', 'facebook', 'help', 'hello', 'wtf', 'blah', 'fugazi', 'lethalcode']
    return render_template('allblogs.j2', title = 'Blogs', blogs = blogs, allTags = allTags)

@app.route('/blog')           ## get single blog having given id
def blog():
    blog_id = request.args.get('blog_id')
    blog = {
        'id': '3434', 'title' : 'Second Blog',
        'content' :  'hello my name is blah blah blah, welcome to blah blah blah',
        'shortlisting_content' : 'shortlisting rounds were easy aF',
        'shortlisting_rounds' : [{'company_name' : 'google', 'content': 'Idk it was usual'}, {'company_name' : 'uber', 'content': 'Idk it was usual'}],
        'interview_content' : 'yeah, the usual stuff but they ask a shitload of crap too',
        'interview_rounds': [{'company_name' : 'facebook', 'content': 'Idk it was usual'}, {'company_name' : 'nutanix', 'content': 'Idk it was usual'}],
        'published_at': '2 days ago', 'tags': ['google', 'facebook', 'help', 'hello', 'bye', 'hehe', 'wtf', 'last'],
        'author': 'thelethalcode'
    }
    if(blog_id == '3434'):
        return render_template('blog.j2', title = blog['title'], blog = blog)
    else :
        return 'Error'

@app.route('/login')
def login():
    pass

@app.route('/signup')
def signup():
    pass

@app.route('/submitBlog',methods = ['POST','GET'])
def submitBlog():    
    blog_form  = BlogForm()   
    if(blog_form.addInterview.data):
        blog_form.interview_rounds.append_entry()
        return render_template('blogform.j2',blog_form = blog_form)
    if(blog_form.addShortListing.data):
        blog_form.shortlisting_rounds.append_entry()
        return render_template('blogform.j2',blog_form = blog_form)
    if(blog_form.addTag.data):
        blog_form.tags.append_entry()
        return render_template('blogform.j2',blog_form = blog_form)
    if(blog_form.validate_on_submit()):       
        #First make all tags unique
        tags = [str(x) for x in set(blog_form.tags)]       
        author_id = random.randint(0,1000000000000)
        author = Author(id = author_id,name = str(blog_form.author))                   
        db.session.add(author)   
        db.session.commit()        
        blog_data = Blog(
            id = int(blog_form.id.data),
            title = str(blog_form.title.data),
            content = str(blog_form.content.data),            
            author = author_id
        )                    
        db.session.add(blog_data)    
        db.session.commit()  
        Tags = []        
        for tag in tags:
            Tags.append(Tag(name = tag,blog = int(blog_form.id.data)))   
        for tag in Tags:
            db.session.add(tag)
        for round in blog_form.shortlisting_rounds:
            current_round = Round(
                round_type = RoundType.shortlisting,
                company_name = str(round.company_name.data),
                content = str(round.content.data),
                blog = int(blog_form.id.data)
            )
            db.session.add(current_round)
        for round in blog_form.interview_rounds:
            current_round = Round(
                round_type = RoundType.interview,
                company_name = str(round.company_name.data),
                content = str(round.content.data),
                blog = int(blog_form.id.data)
            )
            db.session.add(current_round)            
        db.session.commit()                       
        return 'Success'#Some front end editing can be done here
    print(blog_form.errors)
    return render_template('blogform.j2',blog_form = blog_form)#TODO

if __name__ == '__main__':
    db.create_all()
    app.debug = True
    app.run("0.0.0.0", port = 8000)
