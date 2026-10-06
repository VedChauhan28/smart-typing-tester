# Smart Typing Tester

Smart Typing Tester is a simple college-level Python project that measures typing
speed, accuracy, errors, and practice history. It uses Flask for the web server,
SQLite for saving completed tests, and vanilla JavaScript for the live typing
experience.

## Objective

The application gives a user a short typing exercise and calculates:

- Words per minute (WPM)
- Accuracy percentage
- Total errors
- Correct and incorrect characters
- Time taken
- Best performance and previous test history

The project is intentionally straightforward so that each part can be understood
and explained during a college viva.

## Features

- A home page with a short explanation of the project
- Test setup for short, medium, long, or custom user passages
- Custom passage feature allowing users to practice with their own text
- 30, 60, or 120 second time limits
- Easy (max 2 sentences), Medium (max 5 sentences), and Hard (paragraph-style) predefined passages
- Time-calibrated passage scaling optimizing passage length for 30s, 60s, and 120s sessions
- Sentence-boundary trimming so text is never cut mid-sentence
- Timer that starts with the first typed character
- Character-by-character highlighting while typing
- Live WPM, accuracy, error, and character counts
- Automatic completion when time ends or the passage is finished
- SQLite storage for completed tests
- Result screen with practice-again (repeating custom passage or selecting new predefined passage)
- History table with best speed, best accuracy, lowest errors, and total tests
- A small WPM performance chart using Chart.js
- Friendly validation and error messages

## Technology Used

- Python
- Flask
- SQLite
- HTML and Jinja templates
- CSS
- Vanilla JavaScript
- Chart.js through a small CDN script on the history page

## Project Structure

```text
smart-typing-tester/
├── app.py                 # Flask routes and application startup
├── database.py            # SQLite table creation and queries
├── passages.py            # Predefined passages and selection logic
├── typing_tester.db      # Created automatically on first run
├── requirements.txt
├── README.md
├── PROJECT_DOCUMENTATION.md
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── setup.html
│   ├── test.html
│   ├── result.html
│   ├── history.html
│   └── error.html
└── static/
    ├── css/style.css
    └── js/script.js
```

## Installation and Running

From the `smart-typing-tester` directory:

```bash
pip install -r requirements.txt
python app.py
```

Open the local address shown by Flask. In Replit, the project uses the `PORT`
environment variable automatically and can be started by the configured run
command.

## How the Typing Test Works

1. The user chooses a paragraph length, time limit, and difficulty.
2. Flask selects one predefined passage from `passages.py`.
3. The browser displays each passage character in a separate span.
4. JavaScript starts the timer when the user types the first character.
5. Every input event compares typed characters with the original passage.
6. Correct characters become green and incorrect characters become highlighted.
7. The timer stops when it reaches zero or the user completes the passage.
8. The final values are sent to Flask as JSON.
9. Flask saves the result in `typing_tester.db` and opens the result page.

## Calculations

### WPM

```text
WPM = (correct characters / 5) / time in minutes
```

Five characters are treated as one standard word. Only correctly typed
characters contribute to the speed score.

### Accuracy

```text
Accuracy = (correct characters / total typed characters) × 100
```

If no text has been typed, the live screen shows 100% accuracy and 0 WPM.

## Database

The database is created automatically by `database.py` when the app starts. It
contains one table called `tests`:

| Column | Purpose |
| --- | --- |
| `id` | Unique result number |
| `date_time` | Date and time of completion |
| `wpm` | Typing speed |
| `accuracy` | Accuracy percentage |
| `errors` | Incorrect typed characters |
| `correct_chars` | Correct typed characters |
| `incorrect_chars` | Incorrect typed characters |
| `time_taken` | Seconds used |
| `difficulty` | Easy, medium, or hard |
| `paragraph_length` | Short, medium, or long |

## Screenshots

The running application preview can be used as the project screenshot for a
college report. The main screens are the home page, setup page, live test,
result page, and history page.

## Future Improvements

- More predefined passages
- User accounts and separate profiles
- Leaderboards
- More detailed analytics
- Passages in multiple languages
- Multiplayer typing tests

These ideas are intentionally not implemented in this beginner-friendly
version.