from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)

app.config["SECRET_KEY"] = "8685255d6d1bf3d2347b77a2edcf84e1ad70b57f4a496b3e549e4fc5fd3cd0e2"

USERS = {"loui": "loui"}


def is_logged_in():
    username = session.get("username")
    return username in USERS


# macht die Funktion is_logged_in in  Templates verfügbar
@app.context_processor
def inject_auth_helpers():
    return {"is_logged_in": is_logged_in}


@app.route("/")
def home():
    if not is_logged_in():
        return redirect(url_for("login"))
    return render_template("index.html")


@app.route("/login", methods=["GET"])
def login():
    if is_logged_in():
        return redirect(url_for("home"))
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if username in USERS and USERS[username] == password:
        session["username"] = username
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
