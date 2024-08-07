import json
from flask import Flask, render_template, request, redirect, flash, url_for, session
from datetime import datetime


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


def filter_future_competitions(competitions):
    current_date = datetime.now()
    future_competitions = [
        competition
        for competition in competitions
        if datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S") > current_date
    ]
    return future_competitions


@app.route("/")
def index():
    return render_template("index.html", clubs=clubs)


@app.route("/showSummary", methods=["GET", "POST"])
def showSummary():
    if request.method == "POST":
        email = request.form.get("email")
        if not email:
            return render_template("index.html", error="Email is required"), 400

        club = next((club for club in clubs if club["email"] == email), None)
        if club is None:
            return render_template("index.html", error="Email not found"), 400

        session["email"] = request.form["email"]
        session["club"] = club  # Stocker le club dans la session
    else:
        if "email" not in session:
            return redirect(url_for("index"))

        club = session.get("club")
        if not club:
            return redirect(url_for("index"))
    future_competitions = filter_future_competitions(competitions)
    return render_template(
        "welcome.html",
        club=club,
        clubs=clubs,
        competitions=future_competitions,
        session=session,
    )


@app.route("/book/<competition>/<club>")
def book(competition, club):
    if "email" not in session:
        return redirect(url_for("index"), code=401)
    foundClub = [c for c in clubs if c["name"] == club][0]
    future_competitions = filter_future_competitions(competitions)

    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    print(foundCompetition)
    if foundClub and foundCompetition:
        if foundCompetition in future_competitions:
            return render_template(
                "booking.html", club=foundClub, competition=foundCompetition
            )
        else:
            flash("This competition is no longer current")
            return redirect(url_for("showSummary"))
    else:
        flash("Something went wrong-please try again")
        return redirect(url_for("showSummary"))


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    if request.form["places"]:
        placesRequired = int(request.form["places"])

        if "past_purchase" not in session:
            session["past_purchase"] = {}
        if competition["name"] not in session["past_purchase"]:
            session["past_purchase"][competition["name"]] = 0

        if (
            placesRequired > 12
            or (session["past_purchase"][competition["name"]] + placesRequired) > 12
        ):
            flash("You not authorize to get more 12 places per competition")
        elif int(competition["numberOfPlaces"]) < placesRequired:
            flash("Not enough places available for the quantity you requested.")
        elif (int(club["points"]) - placesRequired) < 0:
            flash("Not enough points available.")
        else:
            competition["numberOfPlaces"] = (
                int(competition["numberOfPlaces"]) - placesRequired
            )
            club["points"] = str(int(club["points"]) - placesRequired)
            session["past_purchase"][competition["name"]] += placesRequired
            session["club"] = club
            flash("Great-booking complete!")
    else:
        flash("Please complete the number places.")
    return redirect(url_for("showSummary"))


@app.route("/logout")
def logout():
    session.pop("email", None)
    return redirect(url_for("index"))
