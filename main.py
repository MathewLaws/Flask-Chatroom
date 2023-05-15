from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for, session
from os import path
from flask_socketio import join_room, leave_room, send, SocketIO

app = Flask(__name__)
app.config["SECRET_KEY"] = "%*£fijdsjf38533463473%3fes£$%^£%"
socketio = SocketIO(app)

messages = []

@app.route("/", methods=["GET", "POST"])
def home():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")

        if not username:
            return render_template("home.html", error="Please enter a valid name.")

        session["username"] = username

        return redirect(url_for("chatroom"))

    return render_template("home.html")


@app.route("/chatroom", methods=["GET", "POST"])
def chatroom():
    try:
        if session["username"]:
            return render_template("chatroom.html", username=session.get("username"), messages=messages)
    except:
        return redirect(url_for("home"))

@socketio.on("message")
def message(data):
    
    content = {
        "name": session.get("username"),
        "message": data["data"]
    }
    send(content, to=1)
    messages.append(content)

@socketio.on("connect")
def connect(auth):
    name = session.get("username")
    
    join_room(1)
    send({"name": name, "message": "has entered the room"}, to=1)
    messages.append({"name": name, "message": "has entered the room"})

@socketio.on("disconnect")
def disconnect():
    name = session.get("username")
    leave_room(1)
    
    send({"name": name, "message": "has left the room"}, to=1)
    messages.append({"name": name, "message": "has left the room"})


if __name__ == "__main__":
    socketio.run(app, debug=True)
