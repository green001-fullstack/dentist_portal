from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dentist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    appointments = db.relationship('Appointment', backref='user', lazy=True)

class Dentist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float)
    image = db.Column(db.String(200))
    appointments = db.relationship('Appointment', backref='dentist', lazy=True)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    duration = db.Column(db.Integer)  # in minutes

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    dentist_id = db.Column(db.Integer, db.ForeignKey('dentist.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='Pending')
    service = db.relationship('Service', backref='appointments')

# Create database tables
with app.app_context():
    db.create_all()

    if Service.query.count() == 0:
        sample_services = [
            Service(name='Teeth Cleaning', description='Basic teeth cleaning', price=100.00, duration=30),
            Service(name='Filling', description='Cavity filling', price=150.00, duration=45),
            Service(name='Root Canal', description='Root canal treatment', price=300.00, duration=60),
            Service(name='Dental Checkup', description='Regular dental examination', price=80.00, duration=20)
        ]
        db.session.bulk_save_objects(sample_services)
        db.session.commit()

    if Dentist.query.count() == 0:
        sample_dentists = [
            Dentist(name='Dr. Bolarinwa', specialty='Orthodontics', rating=4.8, image='https://via.placeholder.com/150'),
            Dentist(name='Dr. Taki', specialty='General Dentistry', rating=4.5, image='https://via.placeholder.com/150'),
            Dentist(name='Dr. Omisore', specialty='Pediatric Dentistry', rating=4.9, image='https://via.placeholder.com/150'),
            Dentist(name='Dr. Afolabi', specialty='Endodontics', rating=4.6, image='https://via.placeholder.com/150')
        ]
        db.session.bulk_save_objects(sample_dentists)
        db.session.commit()    

# Routes
@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.fullname
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    print("Register route accessed!")
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))
        
        # Create new user
        new_user = User(
            fullname=fullname,
            email=email,
            password=generate_password_hash(password, method='pbkdf2:sha256'),
            phone=phone
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! Please login', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    
    # Get user's upcoming appointments
    user_id = session['user_id']
    today = datetime.today().date()

    upcoming_appointments = Appointment.query.filter(Appointment.user_id == user_id, Appointment.status =='Confirmed', Appointment.date >= today).order_by(Appointment.date, Appointment.time).all()
    
    return render_template('dashboard.html', user_name=session['user_name'], appointments=upcoming_appointments)

@app.route('/book', methods=['GET', 'POST'])
def book():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Process booking form
        service_id = request.form.get('service_id')
        dentist_id = request.form.get('dentist_id')
        date_str = request.form.get('date')
        time_slot = request.form.get('time_slot')
        notes = request.form.get('notes')
        
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            # Check if slot is available
            existing = Appointment.query.filter_by(
                dentist_id=dentist_id,
                date=date,
                time=time_slot,
                status='Confirmed'
            ).first()
            
            if existing:
                flash('That time slot is already booked. Please choose another.', 'danger')
            else:
                new_appointment = Appointment(
                    user_id=session['user_id'],
                    dentist_id=dentist_id,
                    service_id=service_id,
                    date=date,
                    time=time_slot,
                    notes=notes,
                    status='Confirmed'
                )
                
                db.session.add(new_appointment)
                db.session.commit()
                flash('Appointment booked successfully!', 'success')
                return redirect(url_for('dashboard'))
        
        except ValueError:
            flash('Invalid date format', 'danger')
    
    # Get available services and dentists for dropdowns
    services = Service.query.all()
    dentists = Dentist.query.all()
    
    return render_template('book.html', services=services, dentists=dentists)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)