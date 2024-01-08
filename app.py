from flask import Flask, render_template, request, jsonify
import random
from constants import stadiums, leagues

app = Flask(__name__)

max_attempts = 3


@app.route("/")
def index():
    random_stadium = random.choice(list(stadiums.keys()))
    team_list = list(stadiums.values())
    team_list.sort()
    return render_template("groundle.html", stadium=random_stadium, teams=team_list)


@app.route("/check_guess", methods=["POST"])
def check_guess():
    user_guess = request.json.get("user_guess").strip()
    stadium_id = request.json.get("stadium_id")
    attempts = request.json.get("attempts")

    correct_team = stadiums[stadium_id]

    if user_guess == correct_team:
        return jsonify(
            {
                "feedback": f"Congratulations!",
                "correct_team": correct_team,
                "colour": "green",
            }
        )
    elif attempts == max_attempts:
        if leagues.get(user_guess) == leagues[correct_team]:
            return jsonify(
                {
                    "feedback": f"{user_guess} are the wrong team in the correct league.\nYou are now out of guesses.",
                    "correct_team": correct_team,
                    "colour": "orange",
                }
            )
        else:
            return jsonify(
                {
                    "feedback": f"{user_guess} are the wrong team and wrong league.\nYou are now out of guesses.",
                    "correct_team": correct_team,
                    "colour": "red",
                }
            )
    elif leagues.get(user_guess) == leagues[correct_team]:
        return jsonify(
            {
                "feedback": f"{user_guess} are the wrong team in the correct league. Try again!",
                "colour": "orange",
            }
        )
    else:
        return jsonify(
            {
                "feedback": f"{user_guess} are the wrong team and wrong league. Try again!",
                "colour": "red",
            }
        )


if __name__ == "__main__":
    app.run(debug=True)
