from flask import Flask, render_template, g, redirect, request
import re
import yaml

app = Flask(__name__)

@app.before_request
def load_users():
    with open("data/users.yaml", 'r') as file:
        g.users = yaml.safe_load(file)

def comma_seperated(interest_list):
    return (", ".join(interest.capitalize() for interest in interest_list)
            if interest_list
            else "No interests")

app.jinja_env.filters['comma_seperated'] = comma_seperated

@app.route("/user/<user_name>")
def user(user_name):

    user_info = g.users.get(user_name)

    return render_template("user.html",
                           user_title=user_name,
                           user_info=user_info,
                           users=g.users)

@app.template_global()
def display_users():

    total_interests = sum((len(info['interests'])
                           for name, info
                           in g.users.items()))
    
    return (
        f"There are {len(g.users)} users " +
        f"with a total of {total_interests} " +
        f"interests"
        )

@app.route("/")
def index():

    return render_template("home.html",
                           users=g.users)


if __name__ == "__main__":
    app.run(debug=True, port=5000)