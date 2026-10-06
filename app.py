"""Smart Typing Tester - a simple Flask typing practice application."""

import os
from pathlib import Path

from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for

from database import (
    get_connection,
    get_history,
    get_result,
    get_summary,
    initialize_database,
    save_result,
)
from passages import DIFFICULTIES, LENGTHS, TIME_OPTIONS, choose_passage


PROJECT_DIR = Path(__file__).resolve().parent
DATABASE_PATH = PROJECT_DIR / "typing_tester.db"

app = Flask(__name__)
app.secret_key = os.environ.get(
    "SESSION_SECRET", "smart-typing-tester-development-secret"
)
app.config["JSON_SORT_KEYS"] = False


def validate_configuration(form_data):
    """Validate choices from the setup form including optional custom passage."""
    difficulty = form_data.get("difficulty", "medium").lower()
    paragraph_length = form_data.get("paragraph_length", "medium").lower()
    time_limit = form_data.get("time_limit", "60").lower()
    custom_passage = form_data.get("custom_passage", "").strip()

    if difficulty not in DIFFICULTIES:
        return None, "Please choose an available difficulty."

    # If user provided custom text or chose custom length mode
    if paragraph_length == "custom" or custom_passage:
        paragraph_length = "custom"
        if not custom_passage:
            return None, "Please enter or paste text for your custom passage."
        if len(custom_passage) > 5000:
            return None, "Custom passage is too long. Please limit text to 5,000 characters."

    if paragraph_length not in LENGTHS:
        return None, "Please choose a valid paragraph length."

    try:
        seconds = int(time_limit)
    except (TypeError, ValueError):
        return None, "Please choose a valid time limit."
    if seconds not in TIME_OPTIONS:
        return None, "Please choose an available time limit."

    return {
        "difficulty": difficulty,
        "paragraph_length": paragraph_length,
        "time_limit": seconds,
        "custom_passage": custom_passage if paragraph_length == "custom" else "",
    }, None


@app.route("/")
def index():
    """Show the landing page."""
    summary = get_summary(DATABASE_PATH)
    return render_template("index.html", summary=summary)


@app.route("/setup", methods=["GET", "POST"])
def setup():
    """Show and validate typing test configuration."""
    if request.method == "POST":
        settings, error = validate_configuration(request.form)
        if error:
            flash(error, "error")
            return render_template(
                "setup.html",
                difficulties=DIFFICULTIES,
                lengths=LENGTHS,
                time_options=TIME_OPTIONS,
                form_data=request.form,
            )

        if settings["paragraph_length"] == "custom":
            session["custom_passage"] = settings["custom_passage"]
            return redirect(
                url_for(
                    "test",
                    difficulty=settings["difficulty"],
                    paragraph_length="custom",
                    time_limit=settings["time_limit"],
                    is_custom="1",
                )
            )

        session.pop("custom_passage", None)
        return redirect(
            url_for(
                "test",
                difficulty=settings["difficulty"],
                paragraph_length=settings["paragraph_length"],
                time_limit=settings["time_limit"],
            )
        )

    return render_template(
        "setup.html",
        difficulties=DIFFICULTIES,
        lengths=LENGTHS,
        time_options=TIME_OPTIONS,
        form_data=request.args,
    )


@app.route("/test")
def test():
    """Select a passage and display the live typing test."""
    difficulty = request.args.get("difficulty", "medium").lower()
    paragraph_length = request.args.get("paragraph_length", "medium").lower()
    time_limit = request.args.get("time_limit", "60")
    is_custom = request.args.get("is_custom") == "1" or paragraph_length == "custom"

    if difficulty not in DIFFICULTIES:
        flash("Choose your test settings before starting.", "error")
        return redirect(url_for("setup"))

    try:
        seconds = int(time_limit)
        if seconds not in TIME_OPTIONS:
            raise ValueError
    except (TypeError, ValueError):
        flash("Choose your test settings before starting.", "error")
        return redirect(url_for("setup"))

    if is_custom:
        passage = session.get("custom_passage", "").strip()
        if not passage:
            flash("No custom passage was found. Please enter text for your passage.", "error")
            return redirect(url_for("setup"))
        paragraph_length = "custom"
    else:
        if paragraph_length not in LENGTHS:
            flash("Choose your test settings before starting.", "error")
            return redirect(url_for("setup"))
        exclude = request.args.get("exclude", "")
        passage = choose_passage(
            difficulty, paragraph_length, time_limit=seconds, exclude=exclude
        )

    settings = {
        "difficulty": difficulty,
        "paragraph_length": paragraph_length,
        "time_limit": seconds,
        "is_custom": is_custom,
    }

    return render_template("test.html", passage=passage, settings=settings)


@app.post("/save-result")
def create_result():
    """Save the final client-side calculation to SQLite."""
    payload = request.get_json(silent=True) or {}
    required_fields = [
        "wpm",
        "accuracy",
        "errors",
        "correct_chars",
        "incorrect_chars",
        "time_taken",
        "difficulty",
        "paragraph_length",
    ]
    if any(field not in payload for field in required_fields):
        return jsonify({"error": "The result is missing required information."}), 400

    try:
        result = {
            "wpm": max(0, round(float(payload["wpm"]), 1)),
            "accuracy": max(0, min(100, round(float(payload["accuracy"]), 1))),
            "errors": max(0, int(payload["errors"])),
            "correct_chars": max(0, int(payload["correct_chars"])),
            "incorrect_chars": max(0, int(payload["incorrect_chars"])),
            "time_taken": max(1, int(payload["time_taken"])),
            "difficulty": str(payload["difficulty"]).lower(),
            "paragraph_length": str(payload["paragraph_length"]).lower(),
        }
    except (TypeError, ValueError):
        return jsonify({"error": "The result contains invalid numbers."}), 400

    if result["difficulty"] not in DIFFICULTIES:
        return jsonify({"error": "The result contains an invalid difficulty."}), 400
    if result["paragraph_length"] not in LENGTHS:
        return jsonify({"error": "The result contains an invalid paragraph length."}), 400

    result_id = save_result(DATABASE_PATH, result)
    return jsonify({"id": result_id, "redirect": url_for("result", result_id=result_id)})


@app.route("/result/<int:result_id>")
def result(result_id):
    """Display a completed test."""
    test_result = get_result(DATABASE_PATH, result_id)
    if test_result is None:
        flash("That result could not be found.", "error")
        return redirect(url_for("history"))
    return render_template("result.html", result=test_result)


@app.route("/result")
def result_index():
    """Support the simple /result route while linking to a specific result."""
    result_id = request.args.get("id", type=int)
    if result_id:
        return redirect(url_for("result", result_id=result_id))
    return redirect(url_for("history"))


@app.route("/history")
def history():
    """Display previous tests and summary statistics."""
    return render_template(
        "history.html",
        history=get_history(DATABASE_PATH),
        summary=get_summary(DATABASE_PATH),
    )


@app.errorhandler(404)
def not_found(_error):
    """Show a friendly page instead of a Flask error page."""
    return render_template("error.html", message="The page you requested was not found."), 404


@app.errorhandler(500)
def server_error(_error):
    """Keep database or server errors understandable for normal users."""
    return (
        render_template(
            "error.html",
            message="Something went wrong while loading this page. Please try again.",
        ),
        500,
    )


def start_app():
    initialize_database(DATABASE_PATH)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    start_app()