import os
from flask import (
    Flask,
    render_template,
    send_from_directory,
    flash,
    redirect,
    url_for,
    request,
    session,
    g,
)
from markdown import markdown
from cms.utils import (
    read_text_files,
)
from functools import wraps
import yaml

app = Flask(__name__)
app.secret_key = 'secret'

def require_user_signed_in(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if not user_signed_in():
            flash("You must be signed in to access these functions", "error")
            return redirect(url_for("sign_in", user=session['user']))
        return f(*args, **kwargs)
    return decorator

def load_users():
    user_path = os.path.join(get_data_path(), 'users.yaml')
    with open(user_path, 'r') as file:
        users = yaml.safe_load(file)
    return users

@app.before_request
def initialize_session():
    if 'user' not in session:
        session['user'] = {}

def edit_users(users, username, password):
    users.update({username:password})
    with open(f'{get_data_path()}/users.yaml', 'w') as file:
        yaml.dump(users, file)
    if username in users:
        flash("Users were added succesfully", 'success')

def user_signed_in():
    return ('admin' and 'secret' in session['user'].values())

def get_data_path():
    if app.config['TESTING']:
        return os.path.join(os.path.dirname(__file__), 'tests', 'data')
    else:
        return os.path.join(os.path.dirname(__file__), 'cms', 'data')

@app.route("/", methods=["GET", "POST"])
def index():
    data_dir = get_data_path()

    if request.method == 'POST':
        if not user_signed_in():
            flash("You must be signed in to delete documents", "error")
            return redirect("/")
        filename = request.form.get('filename')

        if filename:
            filepath = os.path.join(data_dir, filename)

            if os.path.exists(filepath):
                os.remove(filepath)
                flash(f"File {filename} was successfully deleted", "success")
            else:
                flash(F"{filename} was not found")
        return redirect('/')
    files = [os.path.basename(path) for path in os.listdir(data_dir)]
    return render_template('home.html', 
                           files=files,
                           user=session['user'])

@app.route("/<filename>")
def file_contents(filename):
    data_dir = get_data_path()
    file_path = os.path.join(data_dir, filename)

    if os.path.isfile(file_path):
        if filename.endswith('.md'):
            with open(file_path, 'r') as file:
                content = file.read()
            return render_template('contents.html', 
                                   contents=markdown(content),
                                   filename=filename)
        else:
            return render_template('contents.html',
                                   contents=read_text_files(file_path, filename),
                                   filename=filename)
    else:
        flash(f"{filename} does not exist.", "error")
        return redirect(url_for('index'))

@app.route("/<filename>/edit")
@require_user_signed_in
def edit_file(filename):
    data_dir = get_data_path()
    file_path = os.path.join(data_dir, filename)

    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            contents = file.read()
        return render_template('edit_page.html', filename=filename, contents=contents)
    else:
        flash(f"{filename} does not exist.", "error")
        return redirect(url_for('index'))


@app.route("/<filename>", methods=['POST'])
@require_user_signed_in
def save_file(filename):
    data_dir = get_data_path()
    file_path = os.path.join(data_dir, filename)

    content = request.form['content']
    with open(file_path, 'w') as file:
        file.write(content)

    flash(f"{filename} has been updated.", "success")
    return redirect(url_for('file_contents', filename=filename))

@app.route("/create_document", methods=["GET", "POST"])
@require_user_signed_in
def create_document():
    data_dir = get_data_path()

    if request.method == "POST":
        filename = request.form.get('file-name', "").strip() + '.txt'

        if not filename:
            flash("Please enter a document title")
            return render_template("create.html")
        os.makedirs(data_dir, exist_ok=True)
        file_path = os.path.join(data_dir, filename)

        if os.path.exists(file_path):
            flash(f"{filename} already exists")
            return render_template('create.html')
        
        with open(file_path, 'w') as file:
            file.write('')
        flash(f"{filename} was created successully!", "success")
        return redirect("/")
    return render_template('create.html')

@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        edit_users(session['user'], username, password)
        session.modified = True

        if (username != 'admin' or password != 'secret'):
            flash("Invalid username or password", "error")
            return render_template('sign_in.html', user=session['user'])
        flash("You have successfully logged in", "success")
        return redirect("/")
    
    return render_template('sign_in.html', user=session['user'])

@app.route("/sign_out", methods=['POST'])
def sign_out():
    session.clear()
    session.modified = True
    flash("Successfully logged out", "success")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, port=5003) 