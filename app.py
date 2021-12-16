import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

from datetime import datetime
import datetime as dt

from pytz import timezone
from calendar import monthrange

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

current_month = datetime.now().month
current_year = datetime.now().year
current_month_first_weekday = monthrange(current_year, current_month)[0] + 1
current_month_num_days = monthrange(current_year, current_month)[1]

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def account():
    
    user_id = session["user_id"]
    name = db.execute("SELECT username FROM users WHERE id = ?", user_id)[0]['username']
    
    created_events = db.execute("SELECT event_name, event_id FROM events WHERE event_creator_id = ?", user_id) 
    joined_events = db.execute("SELECT event_name, event_id FROM events WHERE event_id IN (SELECT DISTINCT event_id FROM event_availability WHERE user_id = ?)", user_id)
    
    return render_template("account.html", name = name, created_events = created_events, joined_events = joined_events)

@app.route("/display" , methods=["POST"])
@login_required
def display():
    if request.method == "POST":
        event_id = request.form.get("selected_event")
        event_locations = db.execute("SELECT location FROM event_locations WHERE event_id = ?", event_id)
        event_name = db.execute("SELECT event_name FROM events WHERE event_id = ?", event_id)[0]['event_name']
        event_dates = db.execute("SELECT date FROM event_dates WHERE event_id = ?", event_id)
        loc_availability = db.execute("SELECT location, COUNT(*) AS num_available FROM location_availability WHERE event_id = ? GROUP BY event_id, location", event_id)

        start_time = db.execute("SELECT start_time FROM events WHERE event_id = ?", event_id)[0]["start_time"]
        end_time = db.execute("SELECT end_time FROM events WHERE event_id = ?", event_id)[0]["end_time"]

        time_diff = end_time - start_time

        availability = db.execute("SELECT t3.date||','||t2.hour AS date_hour, t3.num_available FROM events t1 JOIN hours_24 t2 JOIN (SELECT event_id, date, time, COUNT(*) AS num_available FROM event_availability WHERE event_id = ? GROUP BY event_id, date, time ORDER BY event_id, date, time) t3 ON t1.event_id = t3.event_id AND t2.hour = t3.time WHERE t2.hour >= t1.start_time AND t2.hour < t1.end_time AND t1.event_id = ?", event_id, event_id)
        
        joined_users = db.execute("SELECT username FROM users WHERE id IN (SELECT DISTINCT user_id FROM event_availability WHERE event_id = ?)", event_id)

        joined_users_num = db.execute("SELECT COUNT(DISTINCT user_id) AS num FROM event_availability WHERE event_id = ?", event_id)[0]["num"]

        return render_template("display.html", loc_availability = loc_availability, event_locations = event_locations, event_id=event_id, event_name = event_name, event_dates = event_dates, start_time = start_time, end_time = end_time, time_diff = time_diff, availability = availability, joined_users=joined_users, joined_users_num=joined_users_num)

@app.route("/delete" , methods=["POST"])
@login_required
def delete():
    if request.method == "POST":
        user_id = session["user_id"]
        created_events = db.execute("SELECT event_name, event_id FROM events WHERE event_creator_id = ?", user_id) 
        joined_events = db.execute("SELECT event_name, event_id FROM events WHERE event_id IN (SELECT DISTINCT event_id FROM event_availability WHERE user_id = ?)", user_id)

        return render_template("delete.html", created_events = created_events, joined_events = joined_events)

@app.route("/delete2" , methods=["POST"])
@login_required
def delete2():
    if request.method == "POST":
        user_id = session["user_id"]
        created_events = db.execute("SELECT event_name, event_id FROM events WHERE event_creator_id = ?", user_id) 
        joined_events = db.execute("SELECT event_name, event_id FROM events WHERE event_id IN (SELECT DISTINCT event_id FROM event_availability WHERE user_id = ?)", user_id)
        total_events_count = len(created_events) + len(joined_events)
        for i in range(total_events_count):
            if i < len(created_events):
                if request.form.get("event_" + str(i)):
                    selected_id = request.form.getlist("event_" + str(i))[0]
                    db.execute("DELETE FROM events WHERE event_id = ?", selected_id)
                    db.execute("DELETE FROM event_dates WHERE event_id = ?", selected_id)
                    db.execute("DELETE FROM event_availability WHERE event_id = ?", selected_id)
            else:
                if request.form.get("event_" + str(i)):
                    selected_id = request.form.getlist("event_" + str(i))[0]
                    db.execute("DELETE FROM event_availability WHERE user_id = ? AND event_id = ?", user_id, selected_id)
        
        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")
        
        # Given username
        given_username = request.form.get("username")

        # Ensure username does not already exist
        rows = db.execute("SELECT * FROM users WHERE username = ?", given_username)
        if len(rows) != 0:
            return apology("username already exists")

        # Ensure first password was submitted
        if not request.form.get("password") or not request.form.get("confirmation"):
            return apology("must provide password")

        # Ensure passwords match
        if request.form["password"] != request.form["confirmation"]:
            return apology("passwords must match")

        # Hash the user password
        password_hash = generate_password_hash(
            request.form.get("password"),
            method='pbkdf2:sha256'
        )


        # Insert data into database
        db.execute("INSERT INTO users (username, password) VALUES(?, ?)", given_username, password_hash)

        # Go back to homepage
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/changePassword", methods=["GET", "POST"])
@login_required
def changePassword():
    """Change password."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Ensure first password was submitted
        if not request.form.get("password"):
            return apology("must provide password")

        # Ensure second password was submitted
        if not request.form.get("password_again"):
            return apology("must provide password")

        # Ensure passwords match
        if request.form["password"] != request.form["password_again"]:
            return apology("passwords must match")

        # Hash the user password
        password_hash = generate_password_hash(
            request.form.get("password"),
            method='pbkdf2:sha256'
        )
        
        # Update users database
        db.execute("UPDATE users SET password = ? WHERE id = ?", password_hash, session["user_id"])

        # Go back to homepage
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("changePassword.html")

@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    """Create an event"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # check for errors like empty fields
        if not request.form.get("dates"):
            return apology("must provide dates")

        dates = request.form.get("dates")
        event_dates = dates.split(",")

        if (len(event_dates) > 7):
            return apology("cannot select more than seven dates")
        
        if not request.form.get("start_time"):
            return apology("must provide start time")
        
        if not request.form.get("end_time"):
            return apology("must provide end time")
        
        if not request.form.get("name"):
            return apology("must provide event name")

        if not request.form.get("loc_1"):
            return apology("must fill out at least first location")

        # define variables
        event_name = request.form.get("name")
        event_creator_id = session["user_id"]
        start_time = int(request.form.get("start_time"))
        if (request.form.get("meridian-start") == "pm"):
            start_time += 12
        end_time = int(request.form.get("end_time"))
        if (request.form.get("meridian-end") == "pm"):
            end_time += 12
        if (end_time <= start_time):
            return apology("must provide end time happening after start time")
        loc_1 = request.form.get("loc_1").replace("`", "")

        
        
        
        # insert data into database
        rows = db.execute("SELECT event_id FROM events WHERE event_creator_id = ? AND event_name = ?", session["user_id"], event_name)

        if len(rows) != 0:
            return apology("event already exists")

        db.execute("INSERT INTO events (event_name, event_creator_id, start_time, end_time) VALUES(?, ?, ?, ?)", event_name, event_creator_id, start_time, end_time)

        id = db.execute("SELECT event_id FROM events WHERE event_creator_id = ? AND event_name = ?", session["user_id"], event_name)
        event_id = id[0]["event_id"]

        # insert locations into database if entered
        db.execute("INSERT INTO event_locations (event_id, location) VALUES(?, ?)", event_id, loc_1)

        if request.form.get("loc_2"):
            loc_2 = request.form.get("loc_2").replace("`", "")
            if loc_2 == loc_1:
                return apology("locations must be unique")
            db.execute("INSERT INTO event_locations (event_id, location) VALUES(?, ?)", event_id, loc_2)
        if request.form.get("loc_3"):
            loc_3 = request.form.get("loc_3").replace("`", "")
            if loc_3 == loc_2 or loc_3 == loc_1:
                return apology("locations must be unique")
            db.execute("INSERT INTO event_locations (event_id, location) VALUES(?, ?)", event_id, loc_3)

        # insert days into database
        for day in event_dates:
            db.execute("INSERT INTO event_dates (event_id, date) VALUES(?, ?)", event_id, day)

        return render_template("event_code.html", event_id = event_id)
        
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        current_month = datetime.now().month
        current_year = datetime.now().year
        current_month_first_weekday = monthrange(current_year, current_month)[0] + 1
        current_month_num_days = monthrange(current_year, current_month)[1]
        return render_template("create.html", current_month = current_month, current_year = current_year, current_month_first_weekday = current_month_first_weekday, current_month_num_days = current_month_num_days)


@app.route("/set_month", methods=["POST"])
@login_required
def set_month():
    current_month = int(request.form.get("month"))
    current_year = int(request.form.get("year"))
    current_month_first_weekday = monthrange(current_year, current_month)[0] + 1
    current_month_num_days = monthrange(current_year, current_month)[1]
    return render_template("create.html", current_month = current_month, current_year = current_year, current_month_first_weekday = current_month_first_weekday, current_month_num_days = current_month_num_days)



@app.route("/join", methods=["GET", "POST"])
@login_required
def join():
    """Join an event"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        event_id = request.form.get("code")
        event_dates = db.execute("SELECT date FROM event_dates WHERE event_id = ?", event_id)

        if not event_dates:
                return apology("must provide valid code")

        event_locations = db.execute("SELECT location FROM event_locations WHERE event_id = ?", event_id)
        days_num = len(event_dates)
        start_time = db.execute("SELECT start_time FROM events WHERE event_id = ?", event_id)[0]["start_time"]
        end_time = db.execute("SELECT end_time FROM events WHERE event_id = ?", event_id)[0]["end_time"]

        time_diff = end_time - start_time

        return render_template("schedule.html", event_id=event_id, event_dates = event_dates, event_locations = event_locations, days_num = days_num, start_time = start_time, end_time = end_time, time_diff = time_diff)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("join.html")


@app.route("/schedule", methods=["POST"])
@login_required
def schedule():
    """Update availability for an event"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # define variables
        event_id = request.form.get("event_id")
        event_name = db.execute("SELECT event_name FROM events WHERE event_id = ?", event_id)[0]['event_name']
        event_locations = db.execute("SELECT location FROM event_locations WHERE event_id = ?", event_id)
        event_length = len(event_locations)
        event_dates = db.execute("SELECT date FROM event_dates WHERE event_id = ?", event_id)
        user_id = session["user_id"]
        
        # clear previous entries
        db.execute("DELETE FROM location_availability WHERE event_id = ? AND user_id = ?", event_id, user_id)
        db.execute("DELETE FROM event_availability WHERE event_id = ? AND user_id = ?", event_id, user_id)
        
        # retrieve all availabilities entered
        avail_times = request.form.get("times")
        if not avail_times:
            return apology("must provide when available")
        avail_locs = request.form.get("locs")
        if not avail_locs:
            return apology("must provide purrferred locations")

        locs = avail_locs.split("`")
        times = avail_times.split(" ")

        # update database with new availabilities
        for loc in locs:
            db.execute("INSERT INTO location_availability (event_id, user_id, location) VALUES(?, ?, ?)", event_id, user_id, loc)

        for time in times:
            x = time.split(",")
            date = x[0]
            hour = x[1]
            db.execute("INSERT INTO event_availability (event_id, user_id, date, time) VALUES(?, ?, ?, ?)", event_id, user_id, date, hour)
        
        # define variables to input into HTML template
        user_id = session["user_id"]
        name = db.execute("SELECT username FROM users WHERE id = ?", user_id)[0]['username']
    
        created_events = db.execute("SELECT event_name, event_id FROM events WHERE event_creator_id = ?", user_id) 
        joined_events = db.execute("SELECT event_name, event_id FROM events WHERE event_id IN (SELECT DISTINCT event_id FROM event_availability WHERE user_id = ?)", user_id)
        
        flash("Congrats! Your availability has been updated for event "+ event_name +"!")
        return render_template("account.html", name = name, created_events = created_events, joined_events = joined_events)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)