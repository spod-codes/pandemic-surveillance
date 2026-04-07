from app import create_app
from models import db, Disease

app = create_app()

NEW_DISEASES = [
    ("Polio", "viral", True),
    ("Ebola Virus Disease", "viral", True),
    ("Zika Virus Disease", "viral", True),
    ("Yellow Fever", "viral", True),
    ("Rabies", "viral", True),
    ("Measles", "viral", True),
    ("Mumps", "viral", False),
    ("Rubella", "viral", True),
    ("Hepatitis A", "viral", True),
    ("Hepatitis B", "viral", True),
    ("Hepatitis C", "viral", True),
    ("HIV/AIDS", "viral", True),
    ("Influenza (Novel Strain)", "viral", True),
    ("Avian Influenza (H5N1)", "viral", True),
    ("Marburg Virus Disease", "viral", True),
    ("Lassa Fever", "viral", True),
    ("Mpox (Monkeypox)", "viral", True),
    ("Rift Valley Fever", "viral", True),
    ("Chikungunya", "viral", False),
    ("Norovirus", "viral", False),
    ("Rotavirus", "viral", False),
    ("West Nile Virus", "viral", True),
    ("Hantavirus Pulmonary Syndrome", "viral", True),
    
    ("Tuberculosis", "bacterial", True),
    ("Anthrax", "bacterial", True),
    ("Plague (Pneumonic)", "bacterial", True),
    ("Plague (Bubonic)", "bacterial", True),
    ("Diphtheria", "bacterial", True),
    ("Tetanus", "bacterial", True),
    ("Pertussis (Whooping Cough)", "bacterial", True),
    ("Syphilis", "bacterial", True),
    ("Gonorrhea", "bacterial", False),
    ("Chlamydia", "bacterial", False),
    ("Lyme Disease", "bacterial", False),
    ("Legionnaires' Disease", "bacterial", True),
    ("Meningococcal Disease", "bacterial", True),
    ("Typhus", "bacterial", True),
    ("Leprosy (Hansen's Disease)", "bacterial", True),
    ("Leptospirosis", "bacterial", False),
    ("Salmonellosis", "bacterial", False),
    ("Shigellosis", "bacterial", False),
    ("Campylobacteriosis", "bacterial", False),
    ("Brucellosis", "bacterial", True),
    ("Q Fever", "bacterial", True),
    
    ("Chagas Disease", "parasitic", False),
    ("Leishmaniasis", "parasitic", False),
    ("Toxoplasmosis", "parasitic", False),
    ("Schistosomiasis", "parasitic", False),
    ("Giardiasis", "parasitic", False),
    ("Cryptosporidiosis", "parasitic", False),
    
    ("Candidiasis (Invasive)", "fungal", False),
    ("Aspergillosis", "fungal", False)
]

def add_more_diseases():
    with app.app_context():
        print(f"🔬 Adding {len(NEW_DISEASES)} new pathogens to the Surveillance Registry...")
        
        added_count = 0
        for name, category, notifiable in NEW_DISEASES:
            # Check if disease already exists
            existing = Disease.query.filter_by(name=name).first()
            if not existing:
                pathogen = Disease(name=name, category=category, is_notifiable=notifiable)
                db.session.add(pathogen)
                added_count += 1
                
        db.session.commit()
        print(f"✅ Successfully registered {added_count} new diseases in the database!")

if __name__ == '__main__':
    add_more_diseases()
