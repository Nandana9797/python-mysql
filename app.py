from flask import Flask, render_template, request
import mysql.connector
import os

app = Flask(__name__)


def get_db():
    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"]
    )


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        name = request.form["name"]

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO users (name) VALUES (%s)",
            (name,)
        )

        db.commit()

        cursor.close()
        db.close()

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("index.html", users=users)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)