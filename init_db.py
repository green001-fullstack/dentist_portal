from app import app, db
from models import User, Dentist, Service

with app.app_context():
    # Add sample dentists
    dentists = [
        Dentist(name="Oladimeji Emmanuel", specialty="Consultant Orthodontist", rating=4.9, image="emmanuel.jpg"),
        Dentist(name="Taki Pelumi", specialty="Consultant Oral and Maxillofacial Surgeon", rating=4.6, image="taki.jpg"),
        Dentist(name="Omisore Benjamin", specialty="Consultant Conservative Dentistry", rating=4.8, image="ben.jpg"),
        Dentist(name="Afolabi Abayomi", specialty="Consultant Community Dentistry", rating=4.6, image="afolabi.jpg")
    ]
    
    for dentist in dentists:
        db.session.add(dentist)
    
    # Add sample services
    services = [
        Service(name="Dental Checkup", description="Routine dental examination", price=5000, duration=30),
        Service(name="Teeth Cleaning", description="Professional teeth cleaning", price=8000, duration=45),
        Service(name="Tooth Extraction", description="Simple tooth extraction", price=15000, duration=30),
        Service(name="Root Canal", description="Root canal treatment", price=50000, duration=90),
        Service(name="Dental Filling", description="Tooth cavity filling", price=12000, duration=45),
        Service(name="Teeth Whitening", description="Professional teeth whitening", price=25000, duration=60)
    ]
    
    for service in services:
        db.session.add(service)
    
    db.session.commit()
    print("Database initialized with sample data!")