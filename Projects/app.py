from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed to use sessions

# Predefined users
users = {
    "owner1": "owner@2025",
    "user": "user@2024"
}

# Mapping recipe numbers to filenames
recipes = {
    "1": "Berry_shake.txt",
    "2": "Banana_pancakes.txt",
    "3": "Kaju_paneer.txt",
    "4": "ChickenDryRoast.txt",
    "5": "Carrot_Halva.txt",
    "6": "Egg_fried_rice.txt"
}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["username"] = username
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid username or password.")
    return render_template("login.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    if "username" not in session:
        return redirect(url_for("login"))

    content = ""
    if request.method == "POST":
        choice = request.form.get("choice")
        filename = recipes.get(choice)

        if filename:
            filepath = os.path.join(os.path.dirname(__file__), filename)
            try:
                with open(filepath, "r") as f:
                    content = f.read()
            except FileNotFoundError:
                content = "Recipe file not found!"
        else:
            content = "Invalid choice!"
    return render_template("index.html", content=content)

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
