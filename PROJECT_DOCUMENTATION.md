# Smart Typing Tester - Project Documentation

## Introduction

Smart Typing Tester is a web application that helps a person measure typing
speed and accuracy. The user types a predefined passage while the application
tracks time, correct characters, and typing errors. A result is saved after
each completed test so that the user can compare future practice sessions.

## Problem Statement

Typing speed and accuracy are difficult to measure manually because a person
must watch the clock and count mistakes at the same time. A small application
can perform these calculations consistently and provide immediate feedback
while the user practices.

## Objectives

The objectives of this project are to:

1. Measure typing speed in words per minute.
2. Measure typing accuracy.
3. Detect typing errors while the user is typing.
4. Allow customizable test length, time, and difficulty.
5. Store previous results in a database.
6. Help users practice typing and observe improvement.

## Technologies Used

- **Python:** Main programming language.
- **Flask:** Lightweight Python web framework for routing and templates.
- **SQLite:** Local database for test history.
- **HTML:** Page structure.
- **CSS:** Layout, colors, and responsive styling.
- **JavaScript:** Timer, live comparison, counters, and result submission.

## Functional Requirements

1. The system must show a home page and navigation.
2. The user must be able to select difficulty, paragraph length, time, or enter a Custom Passage.
3. Easy passages must never exceed 2 sentences; Medium passages must never exceed 5 sentences; Hard passages provide paragraph-length text with punctuation and numbers.
4. Passages are dynamically calibrated to match both the selected paragraph length and time limit (30s, 60s, 120s).
5. Passage trimming must preserve complete sentence boundaries and never cut text mid-sentence.
5. The custom passage feature must allow users to paste/type custom text, validating for non-empty input and safe size limits.
6. The system must pass custom passages to the typing test via Flask session without exposing raw text in the URL.
7. The timer must start when the user begins typing.
8. The application must compare typed text with the passage character by character.
9. Incorrect characters must be highlighted immediately while typing.
10. WPM, accuracy, errors, and character counts must update live.
11. Anti-paste protection must remain active for the typing area while allowing pasting into the custom passage input field on setup.
12. The test must finish when time reaches zero or the passage is complete.
13. Completed results must be stored in SQLite.
14. The result page must show final statistics and allow repeating custom passages on "Practice Again".
15. The history page must show previous results and summary performance metrics.

## Non-Functional Requirements

- The interface should be easy to use.
- Live values should update quickly.
- The layout should work on smaller screens.
- SQLite should reliably store results locally.
- The code should be divided into understandable files.
- Normal users should see friendly messages instead of Python stack traces.

## System Workflow

```text
Home
  ↓
Test Configuration
  ↓
Select Difficulty / Length / Time
  ↓
Start Test
  ↓
Real-Time Typing Analysis
  ↓
Test Ends
  ↓
Calculate Result
  ↓
Save to Database
  ↓
Display Result
  ↓
History / Practice Again
```

## Database Design

The `tests` table stores one record for each completed typing test. The `id`
column uniquely identifies a record. The `date_time` column records when the
test was completed. The remaining columns store the final statistics and the
settings used for that session.

The database is local SQLite because it is small, does not require a separate
database server, and is suitable for a single-user college project.

## Algorithms and Formulas

### WPM Algorithm

The browser counts characters that match the same position in the original
passage. It divides the correct character count by 5 to estimate words, then
divides by the elapsed time in minutes:

```text
WPM = (correct characters / 5) / minutes
```

### Accuracy Algorithm

The browser counts correct and incorrect typed characters. It calculates:

```text
Accuracy = (correct characters / total typed characters) × 100
```

When the total typed character count is zero, the application avoids division
by zero and shows 100% accuracy before typing begins.

### Error Detection

JavaScript loops over the typed text. For each position:

- If the typed character matches the passage character, it is correct.
- If it does not match, it is incorrect.
- Characters not typed yet remain pending.

The passage is displayed as separate HTML spans so these states can receive
different CSS colors.

## File Responsibilities

- `app.py`: Creates the Flask app and handles page and result routes.
- `database.py`: Creates the SQLite table and performs database queries.
- `passages.py`: Stores difficulty-based passages and chooses a suitable one.
- `templates/`: Contains the HTML pages rendered by Flask.
- `static/css/style.css`: Contains page styling and responsive rules.
- `static/js/script.js`: Contains timer, comparison, statistics, and save logic.

## Testing Checklist

The following checks should be performed:

1. Start the application.
2. Open the home page.
3. Test easy, medium, and hard difficulty.
4. Test short, medium, and long paragraph lengths.
5. Test the 30, 60, and 120 second time options.
6. Confirm that the timer begins with typing.
7. Confirm that correct and incorrect characters are highlighted.
8. Confirm that WPM and accuracy update during typing.
9. Complete a passage and verify the result page.
10. Allow a timer to reach zero and verify completion.
11. Confirm that the result is stored in SQLite.
12. Open history and confirm that the new result is listed.
13. Confirm that best score values are shown.
14. Click Practice Again and verify that a different passage is selected when possible.
15. Restart the application and verify that history remains available.

## Future Scope

Possible future improvements include user accounts, more passages,
leaderboards, detailed analytics, translations, and multiplayer tests. These
are not required for the current college-level version.