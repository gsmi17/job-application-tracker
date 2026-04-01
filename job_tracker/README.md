# Job Application Tracker

A full-stack web application for tracking job applications, built with Flask, MySQL, and a modern but colorful UI.

## Features
- **Dashboard** — stats overview
- **Companies** — full CRUD with industry, location, notes
- **Jobs** — full CRUD with salary ranges, skill requirements (JSON), job type
- **Applications** — full CRUD with status workflow, cover letter tracking, interview notes
- **Contacts** — full CRUD with LinkedIn integration
- **Job Match** — enter your skills, see ranked job matches with % match and missing skills

## Tech Stack
- **Backend**: Python and Flask
- **Database**: MySQL
- **Frontend**: HTML/CSS

## Setup

### 1. Install dependencies
pip install -r requirements.txt

### 2. Create the database
mysql -u root -p < schema.sql

### 3. Configure database credentials
Edit `database.py` — update:
python
user = 'YOUR USER'
password='YOUR_PASSWORD'

### 4. Go to the job_tracker folder, run the app and visit: http://localhost:5000
python app.py

## Project Structure

job_tracker/
├── app.py              # Flask routes + logic
├── schema.sql          # DB creation script
├── requirements.txt    # Python packages
├── AI_USAGE.md         # GenAI documentation
├── README.md
├── templates/          # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── companies.html
│   ├── jobs.html
│   ├── applications.html
│   ├── contacts.html
│   └── job_match.html
└── static/
    └── style.css       # Full design system

## Database Schema
- companies — stores company info
- jobs — job listings with JSON skill requirements
- applications — tracks each application with status workflow
- contacts — networking contacts per company
