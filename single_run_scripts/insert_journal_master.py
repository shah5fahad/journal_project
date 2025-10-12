import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main_app.extensions import db, app
from main_app.models import JournalMaster


with app.app_context():
    journals_data = [
        {
            "journal_id": "001",
            "full_name": "Curevita Innovation of BioData Intelligence",
            "short_name": "CIBDI",
            "contact_email": "infocvrb@curevita.org",
            "url": "cibdi",
            "about": "International peer-reviewed journal Publishing cutting-edge research in medical technology, healthcare innovations, and clinical advancements."
        },
        {
            "journal_id": "002",
            "full_name": "Curevita Research International Nexus",
            "short_name": "CRIN",
            "contact_email": "infocvrb@curevita.org",
            "url": "crin",
            "about": "A multidisciplinary journal connecting global research across scientific domains and collaborations."
        },
        {
            "journal_id": "003",
            "full_name": "Frontiers of Agri & Animal Innovation",
            "short_name": "FAAI",
            "contact_email": "infocvrb@curevita.org",
            "url": "faai",
            "about": "International peer-reviewed journal advancing research in agricultural sciences, animal husbandry, and sustainable farming practices."
        },
        {
            "journal_id": "004",
            "full_name": "Frontiers in Environmental Revolutionary Innovation",
            "short_name": "FERI",
            "contact_email": "infocvrb@curevita.org",
            "url": "feri",
            "about": "International peer-reviewed journal advancing research in ecology, vitality sciences, environmental health, and sustainable innovation."
        },
        {
            "journal_id": "005",
            "full_name": "Frontiers of Health Innovations and Medical Advances",
            "short_name": "FHIMA",
            "contact_email": "infocvrb@curevita.org",
            "url": "fhim",
            "about": "International peer-reviewed journal Publishing cutting-edge research in medical technology, healthcare innovations, and clinical advancements."
        }
    ]

    total_inserted = 0
    total_skipped = 0

    print(" Starting JournalMaster data insertion...\n")
    for journal_info in journals_data:
        # Duplicate check - journal_id ke basis par
        existing_journal = JournalMaster.query.filter_by(journal_id=journal_info["journal_id"]).first()
        
        if existing_journal:
            print(f" Journal with ID '{journal_info['journal_id']}' already exists — skipping insert.")
            total_skipped += 1
        else:
            try:
                # Create new journal entry
                new_journal = JournalMaster(**journal_info)
                db.session.add(new_journal)
                db.session.commit()
                total_inserted += 1
                print(f" Successfully added: {journal_info['full_name']} ({journal_info['journal_id']})")
            except Exception as e:
                db.session.rollback()
                print(f" Error inserting {journal_info['journal_id']}: {str(e)}")

    # Final summary
    print(f"\n JournalMaster Insertion Summary:")
    print(f" Successfully inserted: {total_inserted} journals")
    print(f" Skipped (duplicates): {total_skipped} journals")
    
    # Database se current data show karein
    all_journals = JournalMaster.query.all()
    print(f"\n Total journals in database: {len(all_journals)}")
    
    if all_journals:
        print("\n Journal List:")
        for journal in all_journals:
            print(f"→ {journal.journal_id}: {journal.full_name} ")
    else:
        print(" No journals found in database.")

print("\n JournalMaster data insertion completed!")