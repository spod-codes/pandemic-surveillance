from app import create_app
from models import db, User, Disease, Report
from datetime import datetime, timedelta
import random

app = create_app()

WORLD_CITIES = [
    {"city": "New York", "lat": 40.7128, "lon": -74.0060},
    {"city": "Los Angeles", "lat": 34.0522, "lon": -118.2437},
    {"city": "Toronto", "lat": 43.6510, "lon": -79.3470},
    {"city": "Mexico City", "lat": 19.4326, "lon": -99.1332},
    {"city": "Sao Paulo", "lat": -23.5505, "lon": -46.6333},
    {"city": "Buenos Aires", "lat": -34.6037, "lon": -58.3816},
    {"city": "Bogota", "lat": 4.7110, "lon": -74.0721},
    {"city": "Lima", "lat": -12.0464, "lon": -77.0428},
    {"city": "London", "lat": 51.5074, "lon": -0.1278},
    {"city": "Paris", "lat": 48.8566, "lon": 2.3522},
    {"city": "Berlin", "lat": 52.5200, "lon": 13.4050},
    {"city": "Madrid", "lat": 40.4168, "lon": -3.7038},
    {"city": "Rome", "lat": 41.9028, "lon": 12.4964},
    {"city": "Cairo", "lat": 30.0444, "lon": 31.2357},
    {"city": "Lagos", "lat": 6.5244, "lon": 3.3792},
    {"city": "Johannesburg", "lat": -26.2041, "lon": 28.0473},
    {"city": "Nairobi", "lat": -1.2921, "lon": 36.8219},
    {"city": "Tokyo", "lat": 35.6762, "lon": 139.6503},
    {"city": "Beijing", "lat": 39.9042, "lon": 116.4074},
    {"city": "Mumbai", "lat": 19.0760, "lon": 72.8777},
    {"city": "Delhi", "lat": 28.7041, "lon": 77.1025},
    {"city": "Bangkok", "lat": 13.7563, "lon": 100.5018},
    {"city": "Jakarta", "lat": -6.2088, "lon": 106.8456},
    {"city": "Seoul", "lat": 37.5665, "lon": 126.9780},
    {"city": "Dubai", "lat": 25.2048, "lon": 55.2708},
    {"city": "Riyadh", "lat": 24.7136, "lon": 46.6753},
    {"city": "Istanbul", "lat": 41.0082, "lon": 28.9784},
    {"city": "Sydney", "lat": -33.8688, "lon": 151.2093},
    {"city": "Melbourne", "lat": -37.8136, "lon": 144.9631},
    {"city": "Auckland", "lat": -36.8485, "lon": 174.7633}
]

def generate_mega_data():
    with app.app_context():
        # First count how many exist
        current_count = Report.query.count()
        target = 183760
        needed = target - current_count
        
        if needed <= 0:
            print(f"Database already has {current_count} entries.")
            return

        print(f"🌍 Database currently has {current_count} records. Generating {needed} more...")
        
        users = User.query.filter_by(role='user').all()
        diseases = Disease.query.all()
        disease_names = [d.name for d in diseases]
        user_ids = [u.id for u in users]
        severities = ['mild', 'mild', 'mild', 'moderate', 'moderate', 'severe', 'critical']
        statuses = ['verified', 'verified', 'pending', 'rejected']
        
        CHUNK_SIZE = 5000
        reports_chunk = []
        
        for i in range(needed):
            city_data = random.choice(WORLD_CITIES)
            
            # Spread out around the globe via lat/lon bounds
            # up to ~110km radius from city centers
            lat_offset = random.uniform(-1.0, 1.0)
            lon_offset = random.uniform(-1.0, 1.0)
            
            disease = random.choice(disease_names)
            # Regional logic
            if city_data['lat'] > 30 and disease in ['Malaria', 'Dengue Fever', 'Ebola Virus Disease', 'Yellow Fever', 'Lassa Fever']:
                # Deflect tropical diseases in Europe/NA
                disease = random.choice(['COVID-19', 'Influenza (Novel Strain)', 'Tuberculosis', 'Measles', 'Polio'])
                
            report = Report(
                user_id=random.choice(user_ids),
                patient_name=f"Patient_X_{random.randint(10000, 999999)}",
                age=random.randint(1, 95),
                disease=disease,
                symptoms="Global mass surveillance record",
                severity=random.choice(severities),
                location_city=city_data['city'],
                location_country="Global",
                latitude=city_data['lat'] + lat_offset,
                longitude=city_data['lon'] + lon_offset,
                report_date=(datetime.utcnow() - timedelta(days=random.randint(0, 730))).date(), # Over last 2 years
                status=random.choice(statuses)
            )
            reports_chunk.append(report)
            
            if len(reports_chunk) >= CHUNK_SIZE:
                db.session.bulk_save_objects(reports_chunk)
                db.session.commit()
                print(f"📦 Committed {CHUNK_SIZE} ... (Progress: {i+1}/{needed})")
                reports_chunk = []
                
        if reports_chunk:
            db.session.bulk_save_objects(reports_chunk)
            db.session.commit()
            
        final_count = Report.query.count()
        print(f"✅ Operations complete! Total incident reports in DB: {final_count:,}")

if __name__ == '__main__':
    generate_mega_data()
