# PROJECT TITLE: Dentist Portal App
#### Video Demo: https://youtu.be/MdI25k_HHrQ

## Table of Contents
- [Project Description](#project-description)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Installation Guide](#installation-guide)
- [Project Structure](#project-structure)
- Future Roadmaps

#### Description
The Dentist Portal App is a Flask-based web application designed to modernize dental appointment management by connecting patients with dentists seamlessly. This project eliminates the traditional hassles of clinic visits, enabling patients to book appointments, view dental services, and manage their oral health remotely.

Key Objectives
1.  Accessibility: Patients in remote areas can connect with dentists without travel.

2.  Transparency: Clear pricing and dentist ratings empower informed decisions.

3.  Efficiency: Reduces clinic wait times through digital scheduling.

Workflow
1.  Landing Page: Introduces the app’s value proposition, top-rated dentists, and booking steps.

2.  Registration/Login: Secure authentication using password hashing.

3.  Dashboard: Central hub for appointment tracking and health tips.

4.  Booking: Patients select services, dentists, and time slots in a streamlined interface.

## Features
For Patients
    User Accounts
        Secure registration with email validation (future scope).
        Password encryption via Werkzeug.
    Appointment Management
        Book, view, and track appointments with status updates (e.g., "Confirmed").
        Disabled past dates to prevent invalid bookings.
    Dentist Profiles
        Browse specialists by ratings (e.g., ★ 4.9) and specialties (e.g., Orthodontics).
        Dentist images and detailed service descriptions.
    Oral Health Resources
        Dashboard includes brushing/flossing tips and dietary advice.

For Dentists (Future Scope)
    Calendar integration for availability management.


## Technologies Used

### Backend
- Python 3: Core programming language.
- Flask: Lightweight framework for routing and templating.
- SQLAlchemy: ORM for database interactions.
- SQLite: Development database (easily upgradable to PostgreSQL).

### Frontend
- HTML5/Jinja2: Dynamic templating for reusable components (e.g., base.html).
- CSS3: Responsive design with Flexbox/Grid (dashboard.css, booking.css).
- JavaScript: Date validation and DOM manipulation.
- Jinja2 Templating
- Font Awesome: Icons for UI enhancements.

### Security
- Session Management: Flask sessions for user authentication.
- Password Hashing: generate_password_hash and check_password_hash from Werkzeug.

### Additional Libraries
- Werkzeug (Password hashing)
- Font Awesome (Icons)

## Installation

1. **Clone the repository**:
   git clone https://github.com/green001-fullstack/dentist-portal-app.git
   cd dentist-portal-app

2.  **Set up a virtual environment**:
    python -m venv venv
    source venv/bin/activate

3.  **Install dependencies**:
    pip install -r requirements.txt

4.  **Initialize the database**:
     from app import db, app
     with app.app_context():
         db.create_all()
         exit()
5.   **Run the application**:
    python app.py
    Access the app:
    Open your browser and navigate to http://localhost:5000

## Project Structure
dentist-portal-app/
├── app.py                # Flask application entry point
├── static/               # Static assets
│   ├── css/              # Stylesheets (e.g., dashboard.css)
│   ├── js/               # JavaScript files
│   └── images/           # Dentist photos/hero images
├── templates/            # Jinja2 templates
│   ├── base.html         # Parent template
│   ├── book.html         # Booking form
│   ├── dashboard.html    # User dashboard with appointments
│   ├── homepage.html     # Landing page
│   ├── login.html        # Login form
│   └── register.html     # Registration form
└── requirements.txt      # Dependencies (Flask, SQLAlchemy)

## Future Roadmap
Implement two-factor authentication

Add calendar sync with Google/Outlook

Develop patient dental history tracking

Create admin dashboard

Integrate telemedicine features
