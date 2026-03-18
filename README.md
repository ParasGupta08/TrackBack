# TrackBack
#### Video Demo:  <https://www.youtube.com/watch?v=GdDaqKalhBo>
#### Description

TrackBack is a failure-based habit tracking web application built as a final project for CS50.

Most habit trackers focus on success. TrackBack instead focuses on understanding failure.
Users log missed habits along with reasons, allowing them to identify patterns and root causes
behind habit breakdowns using simple, explainable analytics.

---

## Features

### Authentication
- User registration and login
- Secure password hashing
- Session-based authentication

### Habit Management
- Create habits with frequency, preferred time, and importance level
- Delete habits safely (associated failures are deleted first)
- Habits are sorted by number of failures so problem habits appear first

### Failure Logging
- Log habit failures with a reason and optional note
- Confirmation prompt prevents accidental logging

### History
- Displays all logged failures with habit name, date, reason, and notes

### Analytics
- Failures per Habit: shows which habits fail most often
- Failure Reasons: shows the most common causes of failure
- Analytics are generated using SQL aggregation (`COUNT`, `GROUP BY`)

### Weekly Summary
- Text-based summary of failures from the last 7 days
- Shows total failures and most common reason

### User Experience
- Empty-state messages guide users when no data exists
- Clean interface using Bootstrap and the Inter font

---

## Technology Stack

- Backend: Python, Flask
- Database: SQLite
- Frontend: HTML, Jinja, Bootstrap 5
- Styling: Custom CSS
- Authentication: Flask sessions, Werkzeug password hashing

---

## Project Structure
```
TrackBack/
├── app.py
├── helpers.py
├── habits.db
├── requirements.txt
│
├── static/
│   └── styles.css
│
└── templates/
    ├── layout.html
    ├── index.html
    ├── login.html
    ├── register.html
    ├── habits.html
    ├── log_failure.html
    ├── history.html
    ├── analytics.html
    ├── summary.html
    └── apology.html
```

# TrackBack

#### Video Demo:  <PUT YOUR VIDEO URL HERE>

#### Description:

TrackBack is a failure-based habit tracking web application built as my final project for CS50.  
Most habit-tracking applications focus primarily on success — whether a habit was completed or not. This project intentionally takes a different approach by focusing on **failure analysis**. The goal of TrackBack is to help users understand *why* habits fail, not just *when* they fail, by logging missed habits along with contextual reasons and analyzing those patterns over time.

The core idea behind this project is that behavioral improvement often comes from understanding root causes rather than simply tracking streaks. By storing failures as individual events and aggregating them using simple, explainable analytics, the application encourages reflection and self-awareness rather than punishment or gamification.

---

### Functionality Overview

The application allows users to register and log in using a secure, session-based authentication system. Passwords are hashed using Werkzeug before being stored in the database. Once logged in, users can create habits by providing a habit name, frequency, preferred time of day, and an importance level. These habits are stored in the database and displayed on the main habits page.

Users can log a failure for any habit by selecting a predefined reason (such as distraction, fatigue, or poor planning) and optionally adding a note for additional context. Before a failure is logged, the application prompts for confirmation to prevent accidental submissions. Each failure is stored as a separate database record, preserving a complete historical timeline.

The application includes a `history page` that displays all logged failures for the current user, including the habit name, date, reason, and any notes. This page is implemented using a SQL JOIN between the habits and failures tables to avoid data duplication and ensure relational integrity.

An `analytics page` provides two key insights: **Failures per Habit** and **Failure Reasons**. These analytics are generated using SQL aggregation functions such as COUNT and GROUP BY. Rather than using machine learning or complex prediction models, the project intentionally relies on transparent, rule-based analytics that are easy to explain and verify.

A weekly `summary page` provides a text-based overview of failures from the past seven days, including the total number of failures and the most common failure reason during that period.

---

### File Structure and Responsibilities

The main Flask application logic resides in `app.py`. This file defines all routes, handles database queries, manages sessions, and coordinates interactions between templates and data.

The `helpers.py` file contains reusable helper functions, including `login_required` for route protection and `apology` for standardized error handling.

The SQLite database file, `habits.db`, stores all application data across three normalized tables: users, habits, and failures. This design prevents data redundancy and supports one-to-many relationships between users and habits, and between habits and failures.

The `templates/` directory contains all HTML files rendered by Flask using Jinja. These templates are dynamic and include conditional logic and loops to display user-specific data. The `layout.html` file serves as a base template, while other files such as `habits.html`, `history.html`, and `analytics.html` extend it.

The `static/` directory contains static assets. In this project, it includes a single `styles.css` file used to apply custom styling and typography. The Inter font is used to create a clean, modern interface, while Bootstrap provides layout structure and responsive components.

The `requirements.txt` file lists all Python dependencies required to run the project.

---

### Design Decisions

One major design decision was to store failures as independent records instead of embedding failure data directly within habits. This approach preserves historical accuracy and enables time-based analysis without overwriting previous data.

Another deliberate choice was to avoid machine learning or external APIs. While predictive features could be added, the project prioritizes clarity, explainability, and reliability. All analytics are derived from deterministic SQL queries, which makes the system easier to debug and explain.

The user interface was kept intentionally minimal. Bootstrap utility classes were used wherever possible to maintain consistency and avoid unnecessary custom CSS. Empty-state messages were added throughout the application to guide users when no data is available.

---

### Conclusion

TrackBack is a focused, user-centric application that demonstrates core computer science concepts taught in CS50, including web development, database design, authentication, and data analysis. By emphasizing failure analysis over success tracking, the project offers a unique perspective on habit formation while remaining technically sound, explainable, and intentionally scoped.
