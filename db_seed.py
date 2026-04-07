from app import create_app
from models import db, User, Disease, Report, AlertThreshold
from datetime import datetime, timedelta
import random

app = create_app()

def seed_db():
    with app.app_context():
        print("🌱 Seeding database...")
        db.drop_all()
        db.create_all()

        # 1. Create Admin
        admin = User(username='admin', email='admin@surveillance.gov', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)

        # 2. Create Doctors/Users
        doc1 = User(username='dr_smith', email='smith@hospital.com', role='user')
        doc1.set_password('password')
        doc2 = User(username='dr_jones', email='jones@clinic.org', role='user')
        doc2.set_password('password')
        db.session.add_all([doc1, doc2])
        db.session.commit()

        # 3. Create Diseases
        diseases = [
            Disease(name='COVID-19', category='viral', is_notifiable=True),
            Disease(name='Dengue Fever', category='viral', is_notifiable=True),
            Disease(name='Malaria', category='parasitic', is_notifiable=True),
            Disease(name='Cholera', category='bacterial', is_notifiable=True),
            Disease(name='Typhoid', category='bacterial', is_notifiable=False)
        ]
        db.session.add_all(diseases)
        db.session.commit()

        # 4. Create Alerts
        alerts = [
            AlertThreshold(disease='COVID-19', location='Mumbai', threshold=50),
            AlertThreshold(disease='Dengue Fever', location='Delhi', threshold=20),
            AlertThreshold(disease='Cholera', location='', threshold=5) # Global
        ]
        db.session.add_all(alerts)

        # 5. Create Sample Reports
        cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad']
        severities = ['mild', 'moderate', 'severe', 'critical']
        statuses = ['pending', 'verified', 'rejected']
        
        disease_names = [d.name for d in diseases]
        
        for i in range(50):
            r = Report(
                user_id=random.choice([doc1.id, doc2.id]),
                patient_name=f"Patient {i}",
                age=random.randint(5, 85),
                disease=random.choice(disease_names),
                symptoms="Fever, cough, fatigue",
                severity=random.choice(severities),
                location_city=random.choice(cities),
                location_state="State",
                report_date=(datetime.utcnow() - timedelta(days=random.randint(0, 30))).date(),
                status=random.choice(statuses)
            )
            db.session.add(r)
        
        db.session.commit()
        print("✅ Database seeded successfully!")
        print("👤 Admin Login -> User: admin | Pass: admin123")
        print("🩺 User Login  -> User: dr_smith | Pass: password")

if __name__ == '__main__':
    seed_db()
