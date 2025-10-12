from main_app.extensions import app, db
from main_app.models import ResearchPaper, JournalMaster

# Flask app context ke andar database access karte hain
with app.app_context():
    # Sample research papers data
    research_papers_data = [
        {   
            "main_heading": "Medical Research",
            "sub_heading": "Advanced Studies in Healthcare",
            "title": "Impact of Lifestyle Interventions on Type 2 Diabetes Management",
            "authors": "Dr. Rajesh Kumar, Dr. Priya Sharma, Prof. Amit Verma",
            "journal": "Curevita Research Journal",
            "volume": "12",
            "issue": "3",
            "year": 2024,
            "abstract": "This study examines the effectiveness of various lifestyle interventions in managing Type 2 Diabetes Mellitus. A randomized controlled trial was conducted with 200 participants over a period of 12 months. Results showed significant improvements in glycemic control and quality of life metrics in the intervention group compared to controls.",
            "pdf_filename": "diabetes_lifestyle_intervention_2024.pdf",
            "citation": "Kumar, R., Sharma, P., & Verma, A. (2024). Impact of Lifestyle Interventions on Type 2 Diabetes Management. Curevita Research Journal, 12(3), 45-62.",
            "image_filename": "diabetes_research.jpg",
            "journal_id": 1
        },
        {
            "main_heading": "Biomedical Innovation",
            "sub_heading": "Cutting-edge Medical Technologies",
            "title": "Development of Novel Nanoparticle-based Drug Delivery System for Cancer Therapy",
            "authors": "Dr. Sunil Mehta, Dr. Anjali Desai, Prof. Vikram Joshi",
            "journal": "Biomedical Research and Innovation",
            "volume": "8",
            "issue": "2",
            "year": 2024,
            "abstract": "This research presents a novel nanoparticle-based drug delivery system designed for targeted cancer therapy. The system demonstrates enhanced drug efficacy and reduced side effects in preclinical models. In vitro and in vivo studies confirm the potential for clinical applications in oncology.",
            "pdf_filename": "nanoparticle_cancer_therapy_2024.pdf",
            "citation": "Mehta, S., Desai, A., & Joshi, V. (2024). Development of Novel Nanoparticle-based Drug Delivery System for Cancer Therapy. Biomedical Research and Innovation, 8(2), 112-128.",
            "image_filename": "nanoparticle_research.jpg",
            "journal_id": 2
        },
        {
            "main_heading": "Clinical Medicine",
            "sub_heading": "Evidence-based Clinical Practices",
            "title": "Comparative Analysis of Surgical Techniques in Laparoscopic Cholecystectomy",
            "authors": "Dr. Neha Patel, Dr. Rohan Malhotra, Prof. Sanjay Kapoor",
            "journal": "Journal of Clinical Medicine Research",
            "volume": "15",
            "issue": "1",
            "year": 2023,
            "abstract": "This comparative study evaluates different surgical techniques in laparoscopic cholecystectomy procedures. The research analyzes outcomes from 150 patients across three surgical approaches, focusing on operative time, complication rates, and patient recovery metrics.",
            "pdf_filename": "laparoscopic_techniques_2023.pdf",
            "citation": "Patel, N., Malhotra, R., & Kapoor, S. (2023). Comparative Analysis of Surgical Techniques in Laparoscopic Cholecystectomy. Journal of Clinical Medicine Research, 15(1), 78-95.",
            "image_filename": "surgical_research.jpg",
            "journal_id": 3
        },
        {
            "main_heading": "Public Health",
            "sub_heading": "Community Health Initiatives",
            "title": "Effectiveness of Public Health Campaigns in Rural Vaccination Coverage",
            "authors": "Dr. Arjun Singh, Dr. Meera Reddy, Prof. Karthik Iyer",
            "journal": "Public Health Research International",
            "volume": "6",
            "issue": "4",
            "year": 2024,
            "abstract": "This study assesses the impact of targeted public health campaigns on vaccination coverage in rural communities. Data from 50 villages shows significant improvement in immunization rates following community-based awareness programs and mobile vaccination clinics.",
            "pdf_filename": "vaccination_coverage_2024.pdf",
            "citation": "Singh, A., Reddy, M., & Iyer, K. (2024). Effectiveness of Public Health Campaigns in Rural Vaccination Coverage. Public Health Research International, 6(4), 201-218.",
            "image_filename": "public_health_research.jpg",
            "journal_id": 4
        },
        {
            "main_heading": "Traditional Medicine",
            "sub_heading": "Ancient Healing Practices",
            "title": "Pharmacological Evaluation of Ayurvedic Formulations in Rheumatoid Arthritis Management",
            "authors": "Dr. Preeti Sharma, Dr. Mohan Das, Prof. Lakshmi Nair",
            "journal": "Journal of Traditional Medicine",
            "volume": "10",
            "issue": "2",
            "year": 2023,
            "abstract": "This research investigates the efficacy of traditional Ayurvedic formulations in managing rheumatoid arthritis symptoms. The study employs modern pharmacological methods to validate traditional knowledge and assess safety profiles of herbal preparations.",
            "pdf_filename": "ayurvedic_arthritis_2023.pdf",
            "citation": "Sharma, P., Das, M., & Nair, L. (2023). Pharmacological Evaluation of Ayurvedic Formulations in Rheumatoid Arthritis Management. Journal of Traditional Medicine, 10(2), 89-107.",
            "image_filename": "traditional_medicine_research.jpg",
            "journal_id": 5
        },
        {
            "main_heading": "Medical Research",
            "sub_heading": "Emerging Infectious Diseases",
            "title": "Genomic Surveillance of Emerging Viral Pathogens in Urban Populations",
            "authors": "Dr. Sameer Khan, Dr. Nisha Rao, Prof. Rajiv Menon",
            "journal": "Curevita Research Journal",
            "volume": "12",
            "issue": "4",
            "year": 2024,
            "abstract": "This genomic surveillance study tracks the evolution and spread of emerging viral pathogens in dense urban environments. The research provides insights into mutation patterns and potential targets for future therapeutic interventions.",
            "pdf_filename": "genomic_surveillance_2024.pdf",
            "citation": "Khan, S., Rao, N., & Menon, R. (2024). Genomic Surveillance of Emerging Viral Pathogens in Urban Populations. Curevita Research Journal, 12(4), 155-172.",
            "image_filename": "genomic_research.jpg",
            "journal_id": 1
        }
    ]

    total_inserted = 0
    total_skipped = 0
    journal_not_found = 0

    print(" Starting ResearchPaper data insertion...\n")

    for paper_data in research_papers_data:
        # Check if journal exists
        journal = JournalMaster.query.filter_by(id=paper_data["journal_id"]).first()
        
        if not journal:
            print(f" Journal with ID {paper_data['journal_id']} not found — skipping paper: {paper_data['title']}")
            journal_not_found += 1
            continue
        
        # Duplicate check - title ke basis par
        existing_paper = ResearchPaper.query.filter_by(title=paper_data["title"]).first()
        
        if existing_paper:
            print(f" Research paper with title '{paper_data['title'][:50]}...' already exists — skipping insert.")
            total_skipped += 1
        else:
            try:
                # Create new research paper entry
                new_paper = ResearchPaper(**paper_data)
                db.session.add(new_paper)
                db.session.commit()
                total_inserted += 1
                print(f" Successfully added: {paper_data['title'][:60]}...")
            except Exception as e:
                db.session.rollback()
                print(f" Error inserting paper '{paper_data['title'][:50]}...': {str(e)}")

    # Final summary
    print(f"\n ResearchPaper Insertion Summary:")
    print(f" Successfully inserted: {total_inserted} research papers")
    print(f" Skipped (duplicates): {total_skipped} papers")
    print(f" Journals not found: {journal_not_found} papers")
    
    # Database se current data show karein
    all_papers = ResearchPaper.query.all()
    print(f"\n Total research papers in database: {len(all_papers)}")
    
    if all_papers:
        print("\n Research Papers List:")
        for paper in all_papers:
            print(f"→ ID {paper.id}: {paper.title[:50]}... | Journal ID: {paper.journal_id}")
    else:
        print("No research papers found in database.")

print("\n ResearchPaper data insertion completed!")