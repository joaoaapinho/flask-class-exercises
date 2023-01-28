from flask import Flask, render_template, request

import csv

app = Flask(__name__)


@app.route("/")
def index():
    
    users_list = []

    with open("data/users.csv","r") as file:
        reader = csv.reader(file,delimiter = ",")
        found_user = None
        for row in reader: 
            users_list.append({

            'user_id': row[0],
            'birth_date': row[1],
            'user_name': row[2] +" "+ row[3],
            'email': row[4]
        })

        num = len(users_list)

    #request.args.get('page') retrieves the value of a specific query string in the url 
    #request.args is ~ dictionary in which the get allows us to retrieve the value of a specific key
    # in this case by retriving the value of key 'page' it will tell the server what page the user is requesting
    page = int(request.args.get('page', 1))

    #setting a limit of 30 links per page
    per_page = 30

    # marks the index of the first user I will display 
    # E.g., For the first page (1-1) * 30 = 0 
    start = (page - 1) * per_page
    
    # marks the index of the last user I will display
    # E.g., For the first page (0)+ 30 = 30
    end = start + per_page

    # slicing the users_list to only show the users with indexes from start to end
    users_list = users_list[start:end]

    # In order for the function to don't assume the number_of_users as a positional argument
    # I need to pass it as named arguments (add arguments to functions )
    return render_template("index.html", users_list = users_list, number_of_users=num, page = page, per_page = per_page)

@app.route("/login")
def login_form():
    return render_template("login.html")


@app.route("/handle-login", methods = ["POST"])
def handle_login():
    username = request.form["username"]
    password = request.form["password"]

    return "OK"

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/<user_id>")
def user_specific (user_id):
    with open("data/users.csv","r") as file:
        found_user = None
        reader = csv.reader(file,delimiter = ",")
        for row in reader:
            if row[0] == user_id:
                found_user = row
                user_name = row[2] + " " + row[3]
                user_birth = row[1]
                user_email = row[4]
    if found_user:
        return render_template ("user_id.html", user_name = user_name,user_birth = user_birth, user_email = user_email)
    else:
        return "User not found"


app.run(port=8080, debug=True)