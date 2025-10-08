# journal_crud_master.py
from app import app, db, JournalMaster

def add_journal():
    with app.app_context():   # ✅ App context ke andar
        journal_id = input("Enter Journal ID (e.g. JRN001): ")
        full_name = input("Enter Full Name: ")
        short_name = input("Enter Short Name: ")
        domain_name = input("Enter Domain Name: ")
        url = input("Enter URL: ")
        hosting_provider = input("Enter Hosting Provider: ")
        issn = input("Enter ISSN: ")
        publisher = input("Enter Publisher: ")

        new_journal = JournalMaster(
            journal_id=journal_id,
            full_name=full_name,
            short_name=short_name,
            domain_name=domain_name,
            url=url,
            hosting_provider=hosting_provider,
            issn=issn,
            publisher=publisher
        )
        db.session.add(new_journal)
        db.session.commit()
        print("✅ Journal added successfully!")

def list_journals():
    with app.app_context():
        journals = JournalMaster.query.all()
        for j in journals:
            print(f"{j.id} | {j.journal_id} | {j.full_name}")

def main():
    while True:
        print("\n=== Journal CRUD Menu ====")
        print("1. Add Journal")
        print("2. List Journals")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_journal()
        elif choice == "2":
            list_journals()
        elif choice == "3":
            break
        else:
            print("Invalid choice, try again!")


if __name__ == "__main__":
    main()
