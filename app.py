from cs50 import SQL
from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from helpers import login_required, apology
from werkzeug.security import check_password_hash, generate_password_hash

# Application Configuration 
app = Flask(__name__)

# Template Config
app.config["TEMPLATES_AUTO_RELOAD"] = True

#  Session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Database 
db  = SQL("sqlite:///habits.db")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return apology("missing fields", 400)

        if password != confirmation:
            return apology("passwords do not match", 400)

        hash_pw = generate_password_hash(password)

        try:
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                username, hash_pw
            )
        except:
            return apology("username already exists", 400)

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid credentials", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/habits", methods = ["GET", "POST"])
@login_required
def habits():
    user_id = session["user_id"]
    if request.method == "POST":
        name = request.form.get("name")
        frequency = request.form.get("frequency")
        preferred_time = request.form.get("preferred_time")
        importance = request.form.get("importance")    
        if not name or not frequency or not preferred_time or not importance:
            return apology("missing habit data", 400)
    
        db.execute(
            """
            INSERT INTO habits (user_id, name, frequency, preferred_time, importance)
            VALUES (?, ?, ?, ?, ?)
            """,
            user_id, name, frequency, preferred_time, importance
        )

        return redirect("/habits")
    
    habits = db.execute( "SELECT * FROM habits WHERE user_id = ?",user_id)
    return render_template("habits.html", habits = habits)   


@app.route("/log/<int:habit_id>", methods=["GET", "POST"])
@login_required
def log_failure(habit_id):
    user_id = session["user_id"]

    # Ensure habit belongs to logged-in user
    habit = db.execute(
        "SELECT * FROM habits WHERE id = ? AND user_id = ?",
        habit_id, user_id
    )

    if len(habit) != 1:
        return apology("invalid habit", 403)

    if request.method == "POST":
        reason = request.form.get("reason")
        note = request.form.get("note")

        if not reason:
            return apology("missing failure reason", 400)

        db.execute(
            """
            INSERT INTO failures (habit_id, date, reason, note)
            VALUES (?, DATE('now'), ?, ?)
            """,
            habit_id, reason, note
        )

        return redirect("/habits")

    return render_template("log_failure.html", habit=habit[0])


@app.route("/history")
@login_required
def history():
    user_id = session["user_id"]

    rows = db.execute(
        """
        SELECT habits.name, failures.date, failures.reason, failures.note
        FROM failures
        JOIN habits ON failures.habit_id = habits.id
        WHERE habits.user_id = ?
        ORDER BY failures.date DESC
        """,
        user_id
    )

    return render_template("history.html", rows=rows)


@app.route("/analytics")
@login_required
def analytics():
    user_id = session["user_id"]

    habits = db.execute(
        "SELECT id, name FROM habits WHERE user_id = ?",
        user_id
    )

    failures_per_habit = db.execute(
    """
    SELECT
        habits.name,
        COUNT(failures.id) AS count
    FROM habits
    LEFT JOIN failures ON failures.habit_id = habits.id
    WHERE habits.user_id = ?
    GROUP BY habits.id
    ORDER BY count DESC
    """,
    user_id
    )


    reasons = db.execute(
        """
        SELECT failures.reason, COUNT(*) AS count
        FROM failures
        JOIN habits ON failures.habit_id = habits.id
        WHERE habits.user_id = ?
        GROUP BY failures.reason
        ORDER BY count DESC
        """,
        user_id
    )


    return render_template(
    "analytics.html",
    failures_per_habit=failures_per_habit,
    reasons=reasons,
)

@app.route("/delete/<int:habit_id>", methods=["POST"])
@login_required
def delete_habit(habit_id):
    user_id = session["user_id"]

    # Ensure habit belongs to user
    habit = db.execute(
        "SELECT id FROM habits WHERE id = ? AND user_id = ?",
        habit_id, user_id
    )
    if not habit:
        return apology("invalid habit", 403)

    # Delete dependent failures first
    db.execute("DELETE FROM failures WHERE habit_id = ?", habit_id)

    # Delete habit
    db.execute("DELETE FROM habits WHERE id = ?", habit_id)

    return redirect("/habits")


@app.route("/summary")
@login_required
def summary():
    user_id = session["user_id"]

    total = db.execute(
        """
        SELECT COUNT(*) AS count
        FROM failures
        JOIN habits ON failures.habit_id = habits.id
        WHERE habits.user_id = ?
        AND failures.date >= DATE('now', '-7 days')
        """,
        user_id
    )[0]["count"]

    top_reason = db.execute(
        """
        SELECT failures.reason, COUNT(*) AS count
        FROM failures
        JOIN habits ON failures.habit_id = habits.id
        WHERE habits.user_id = ?
        AND failures.date >= DATE('now', '-7 days')
        GROUP BY failures.reason
        ORDER BY count DESC
        LIMIT 1
        """,
        user_id
    )

    return render_template(
        "summary.html",
        total=total,
        top_reason=top_reason[0]["reason"] if top_reason else None
    )