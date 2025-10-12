import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main_app.extensions import db, app
from main_app.models import ContactDetail, JournalMaster


contact_data = {
    "phone": "+91 79870 82627",
    "email": "infocvrb@curevita.org",
    "name": "Curevita Research Pvt Ltd",
    "address": "4/21 LIG, Informal Sector, Vidya Nagar, Bhopal, MP, India",
    "company_website": "https://curevita.org/",
    "youtube_url": "https://www.youtube.com/@curevitaresearch",
    "twitter": "https://x.com/curevitares?t=y7v5NGuSNIHXwTPs5jLNUw&s=08",
    "linkedin": "https://www.linkedin.com/company/curevita-research-pvt-ltd/",
    "instagram": "https://www.instagram.com/curevitaresearch/?igsh=MW1qOWMyaG1mdnRkOQ%3D%3D#", 
    "facebook": "https://www.facebook.com/Curevitaresearch?rdid=UzKVvwaxNBCMndkM&share_url=https%3A%2F%2Fwww.facebook.com%2Fshare%2F15L8uPdxqR%2F#",
}
with app.app_context():    
    journals = JournalMaster.query.all()
    for journal in journals:
        print(f" Processing Journal: {journal.full_name}")
        
        # Duplicate check
        existing_contact = ContactDetail.query.filter_by(journal=journal).first()
        if existing_contact:
            print(f" Contact for the journal {journal.short_name} already exists — skipping insert.")
        else:
            contact_data['journal_id'] = journal.id
            contact_data['journal'] = journal
            new_contact = ContactDetail(**contact_data)
            db.session.add(new_contact)
            db.session.commit()
            print(f" Contact for Journal ID {journal.id} inserted successfully!")

    # Final verification
    print(f"\n Final database status:")
    contacts = ContactDetail.query.all()
    print(f"Total contacts: {len(contacts)}")
    for c in contacts:
        print(f"→ {c.id}. {c.name} | {c.email} | Journal ID: {c.journal_id}")