from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = "8685255d6d1bf3d2347b77a2edcf84e1ad70b57f4a496b3e549e4fc5fd3cd0e2"


class Character:
    def __init__(self, name):
        self.name = name

class User:
    def __init__(self, username, password, chars,  wins, losses):
        self.username = username
        self.password = password
        self.characters = chars
        self.wins = wins
        self.losses = losses

USERS = {
    "brian": User("brian", "brian", [Character("A")], 12, 1),
    "tobi": User("tobi", "tobi", [Character("A")], 8, 4),
    "loui": User("loui", "loui", [Character("A")], 6, 4),
}

def current_user():
    username = session.get("username")
    return USERS.get(username)

def is_logged_in():
    return current_user() is not None

# macht die Funktion is_logged_in und current_user in  Templates verfügbar
@app.context_processor
def inject_context():
    return {
        "is_logged_in": is_logged_in,
        "current_user": current_user
    }


@app.route("/")
def home():
    if not is_logged_in():
        return redirect(url_for("login"))
    return render_template("home.html")


@app.route("/login", methods=["GET"])
def login():
    if is_logged_in():
        return redirect(url_for("home"))
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():

    username = request.form.get("username", "")
    password = request.form.get("password", "")

    user = USERS.get(username)

    if user and user.password == password:
        session["username"] = user.username
        return redirect(url_for("home"))

    return render_template("login.html", error="Nutzername oder Passwort falsch")


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/characters")
def characters():
    if not is_logged_in():
        return redirect(url_for("login"))
    return render_template("characters.html")
