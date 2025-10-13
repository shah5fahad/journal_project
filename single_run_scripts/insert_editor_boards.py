import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main_app.extensions import app, db
from main_app.models import EditorBoard, JournalMaster

# Flask app context ke andar database access karte hain
with app.app_context():
    # Multiple journals ke liye editors add karna
    journals_data = [
        {
            "journal_id": "001",
            "editors": [
                {
                    "name": "Dr Usha Chouhan",
                    "designation": " Editor-in-Chief (EIC), Professor, Department of Mathematics, Bioinformatics and Computer Applications, Maulana Azad National Institute of Technology (MANIT), Bhopal, India",
                    "link": "chouhanu@manit.ac.in",
                    "quote": "Leading with vision and expertise at MANIT Bhopal, Dr. Chouhan brings excellence to CIBDI's editorial leadership.",
                    "code": "01",
                },
                {
                    "name": "Dr Rahul Verma",
                    "designation": "Research Scientist Florida International University, Florida, United States",
                    "link": "rverma@fiu.edu",
                    "quote": "CIBDI offers a credible platform for impactful international research dissemination.",
                    "code": "01",
                },
                {
                    "name": "Prof. Mohan Kumar Patel",
                    "link": "mohanpatel@mpu.ac.in",
                    "designation": "Professor Department of Computer Science Engineering MPU University, Bhopal, MP, India",
                    "quote": "CIBDI's focus on computational sciences and engineering applications makes it a valuable platform for innovative research.",
                    "code": "01",
                },
                {
                    "name": "Dr Harengiri Gosai",
                    "link": "harengiri.gosai@indrashiluniversity.edu.in",
                    "designation": "Professor Department of Bioscience, School of Science Indrashil University, Rajpur, Gujrat, India",
                    "quote": "CIBDI's interdisciplinary approach bridges the gap between biosciences and data innovation, creating new research opportunities.",
                    "code": "01",
                },
                {
                    "name": "Dr Shreya Sharma",
                    "link": "shreya.sharmacsaids@galgotiacollege.edu",
                    "designation": "Assistant Professor Galgotias College of Engineering and Technology, GALGOTIAS UNIVERSITY, Greater Noida, Uttar Pradesh, India",
                    "quote": "It's a great honor to be associated with a journal that values translational science and interdisciplinary advancement.",
                    "code": "01",
                },
                {
                    "name": "Dr Ramachandra Merugu",
                    "link": "ramchandra@mguniversity.ac.in",
                    "designation": "Associate Professor Department of Biotechnology Mahatma Gandhi University, Nalgonda, Hyderabad, India",
                    "quote": "CIBDI encourages young researchers to showcase their work and fosters interdisciplinary collaboration at the global level.",
                    "code": "01",
                },
                {
                    "name": "Dr Nitin Dhimole",
                    "link": "dhimolenitin22@gmail.com",
                    "designation": "Professor Department of Computer Science and Engineering SCOPE Global Skills University, Bhopal, MP, India",
                    "quote": "CIBDI's focus on skill development and practical applications in computer science makes it a unique platform for academic and industry collaboration.",
                    "code": "01",
                },
                {
                    "name": "Dr Pankaj Dipankar",
                    "link": "",
                    "designation": "National Institute of Nursing Research, Research Scientist, National Institutes of Health (NIH), Bethesda, MD, United States",
                    "quote": "",
                    "code": "02",
                }
            ]
        },
        {
            "journal_id": "002",
            "editors": [
                {
                    "name": "Dr. Manoj Kumar Tembhre",
                    "designation": "Editor-in-Chief (EIC), Senior Scientist, Cardiac Biochemistry, AIIMS New Delhi, India",
                    "link": "https://www.aiims.edu/index.php/en/2014-12-17-09-43-36/2014-12-17-09-48-16",
                    "quote": "Leading with vision and expertise at the All India Institute of Medical Sciences, Dr. Tembhare brings excellence to CRIN's editorial leadership.",
                    "code": "01"
                },
                {
                    "name": "Dr. Shweta Katiyar",
                    "designation": "Assistant Professor, Sarojini Naidu Govt Girls PG College, Bhopal (MP), India",
                    "link": "",
                    "quote": "Proud to support CRIN's mission of fostering academic growth across multidisciplinary domains.",
                    "code": "01"
                },
                {
                    "name": "Dr. Rahul Verma",
                    "designation": "Research Scientist, Florida International University, Florida, USA",
                    "link": "https://www.linkedin.com/in/rahul-verma-71013b233",
                    "quote": "CRIN offers a credible platform for impactful international research dissemination.",
                    "code": "01"
                },
                {
                    "name": "Dr. Anil Sarsavan",
                    "designation": "Senior Program Manager, Foundation For Ecological Security (FES), India",
                    "link": "https://in.linkedin.com/in/anil-sarsavan-41742765",
                    "quote": "CRIN’s focus on sustainability and ecological relevance makes it a unique and much-needed platform for modern research.",
                    "code": "01"
                },
                {
                    "name": "Dr. Rajdeep Jaswal",
                    "designation": "Research Scientist, USDA-ARS, North Dakota State University, USA",
                    "link": "https://www.linkedin.com/in/rajdeep-jaswal-32166210a/?originalSubdomain=in",
                    "quote": "It’s a great honor to be associated with a journal that values translational science and interdisciplinary advancement.",
                    "code": "01"
                },
                {
                    "name": "Dr Ravi Prasad Mukku",
                    "designation": "Research Scientist, Department of Biomedical and Clinical Sciences (BKV), Division of Molecular Medicine and Virology (MMV), Linköping University (LIU), USA",
                    "link": "https://www.linkedin.com/in/ravi-prasad-68092b91/?originalSubdomain=in",
                    "quote": "CRIN encourages young researchers to showcase their work and fosters interdisciplinary collaboration at the global level.",
                    "code": "01"
                },
                {
                    "name": "Dr. Niharika Bhawsar",
                    "designation": "Assistant Professor, Department of Biotechnology, PM College of Excellence, Govt. Narmada College, Narmadapuram, MP, India",
                    "link": "https://www.linkedin.com/in/dr-niharika-bhawsar-a51269a9/?originalSubdomain=in",
                    "quote": "",
                    "code": "02"
                },
                {
                    "name": "Dr Jitendra Malviya",
                    "designation": "Assistant Professor, Department of Microbiology, Barkatullah University, Bhopal, MP, India",
                    "link": "https://orcid.org/0000-0001-7501-0121",
                    "quote": "",
                    "code": "02"
                },
                {
                    "name": "Dr Aswani Mishra",
                    "designation": "Prof. Department of Pharmaceutical Science, NINM, Indore, MP , India",
                    "link": "https://in.linkedin.com/in/dr-ashwani-mishra-41042754",
                    "quote": "",
                    "code": "02"
                },
                {
                    "name": "Dr Naveen Vishwakarma",
                    "designation": "Assistant Professor, HOD, Department of Botany, PMCOP, Govt Auto. PG College, Chhindwara, MP, India",
                    "link": "https://in.linkedin.com/in/naveen-vishwakarma-bb59b7211",
                    "quote": "",
                    "code": "02"
                },
                {
                    "name": "Dr. Sivaiah Budala",
                    "designation": "Animal Biochemistry, ICAR-NDRI, Bengaluru, Karnataka, INDIA",
                    "link": "",
                    "quote": "",
                    "code": "02"
                },
                {
                    "name": "Dr Kuldeep Lakhera",
                    "designation": "Faculty of Botany, Veerangana Rani Durgava Govt. College, Tirodi, Balaghat, MP, India",
                    "link": "",
                    "quote": "",
                    "code": "02"
                },
                {
                    "name": "Dr RK Choudhary",
                    "designation": "Assistant Professor, Sha-Shib Science & Management College, Sha-Shib Group of Institutions, Bhopal, MP, India",
                    "link": "",
                    "quote": "",
                    "code": "02"
                },
                {
                    "name": "Dr Yogesh Badkhene",
                    "designation": "Publication Head, Department of Training and Skills Development, Curevita Research Pvt Ltd, Bhopal, MP, India",
                    "link": "",
                    "quote": "",
                    "code": "02"
                },
                {
                    "name": "Dr Nisar Ahmad Ganie",
                    "designation": "Faculty, Department of Zoology, Government College Raghogarh, Guna (MP), India",
                    "link": "",
                    "quote": "",
                    "code": "02"
                }
            ]
        },
        {
            "journal_id": "003", 
            "editors": [
                {
                    "name": "Dr Mohhabat Singh Jamra",
                    "designation": "Editor in chief (EIC), Livestock Production and Management, Assistant Professor, College of Veterinary Science and Animal Husbandry, Nanaji Deshmukh Veterinary Science University (NDVSU), Mhow, Indore, Madhya Pradesh 453446, India",
                    "link": "",
                    "quote": "Driving innovation in livestock sciences, Dr. [Name] leads LPM with expertise and dedication at NDVSU Mhow.",
                    "code": "01"
                },
                {
                    "name": "Dr Rajdeep Jaswal",
                    "designation": "Research Scientist, North Dakota State University, US Department of Agriculture (USDA) Agricultural Research Service (ARS), Fargo, USA",
                    "link": "",
                    "quote": "Driving innovation and agricultural research excellence at North Dakota State University and USDA-ARS, Fargo, USA.",
                    "code": "01"
                },
                {
                    "name": "Dr Anita Kerketta",
                    "designation": "Assistant Professor, Dept. of Vegetable Science, College of Horticulture & Research Station, Sankara, Patan-Durg-491111, Mahatma Gandhi University of Horticulture and Forestry (MGUVV), Durg, Chhattisgarh, India",
                    "link": "",
                    "quote": "Driving innovation in horticultural sciences, Dr Anita Kerketta brings expertise and leadership from MGUVV Durg to the editorial forefront.",
                    "code": "01"
                },
                {
                    "name": "Dr Neeraj Shrivastava",
                    "designation": "Associate Professor, Amity Institute of Microbial Technology (AIMT), Amity University, Noida, UP, India",
                    "link": "",
                    "quote": "Driving innovation and expertise at Amity University, Dr Neeraj Shrivastava strengthens AIMT's academic and research leadership.",
                    "code": "01"
                },
                {
                    "name": "Dr Amit Kumar Jha",
                    "designation": "Assistant Professor, Department of Animal Genetics and Breeding, College of Veterinary Science & Animal Husbandry, Rewa-486001 (M.P.), India",
                    "link": "",
                    "quote": "Advancing innovation in animal genetics and breeding, bringing academic excellence from CVSc & AH, Rewa",
                    "code": "01"
                },
                {
                    "name": "Dr Dinesh Kumar",
                    "designation": "Assistant Professor cum Junior Scientist, Department of Animal Nutrition, College of Veterinary Science and Animal Husbandry, Birsa Agricultural University, Kanke, Ranchi, 834006, India",
                    "link": "",
                    "quote": "Driving innovation in animal nutrition, Dr. Dinesh Kumar advances research and excellence at Birsa Agricultural University.",
                    "code": "01"
                },
                {
                    "name": "Dr Kuldeep Kumar Verma",
                    "designation": "Assistant Professor & Asst. Exam In-charge (PGS), Dept. of Livestock Production Management, Faculty of Veterinary & Animal Sciences, IAS, Rajiv Gandhi South Campus, BHU, Barkachha, Mirzapur-231001, UP, India.",
                    "link": "",
                    "quote": "Advancing veterinary and animal sciences education at BHU, Dr Kuldeep Kumar Verma drives innovation and excellence in livestock production management.",
                    "code": "01"
                },
                {
                    "name": "Dr HC Verma",
                    "designation": "Assistant Professor, Department of Veterinary Extension Education, Narendra Deva University of Agriculture and Technology (NDUAT), Kumarganj, Ayodhya, UP, India",
                    "link": "",
                    "quote": "Driving innovation and expertise at NDUAT Ayodhya, Dr HC Verma advances Veterinary Extension Education with impactful leadership.",
                    "code": "01"
                },
                {
                    "name": "Dr Ankur Sharma",
                    "designation": "Subject Matter Specialist (Animal Biotechnology), ICAR-IIVR-KVK, Deoria (UP), India",
                    "link": "",
                    "quote": "Driving innovation in Animal Biotechnology at ICAR-IIVR-KVK, Deoria, Dr Ankur Sharma advances research excellence and expertise.",
                    "code": "01"
                },
                {
                    "name": "Dr Surendra Jangara",
                    "designation": "Associate Prof., Department of Chemistry & Biochemistry, School of Basic Sciences & Research, Sharda University, Greater Noida, Ruhallapur, Uttar Pradesh 201310, India",
                    "link": "",
                    "quote": "Advancing scientific innovation at Sharda University, Dr. Surendra Jangara drives excellence in Chemistry and Biochemistry research and education",
                    "code": "01"
                },
                {
                    "name": "Dr Neeraj Kumar Gupta",
                    "designation": "Prof & Head, School of Agriculture Science, LNCT University, Bhopal, India",
                    "link": "",
                    "quote": "Guiding agricultural innovation at LNCT University, Bhopal, Dr. Neeraj Kumar Gupta drives excellence in research and leadership.",
                    "code": "01"
                },
                {
                    "name": "Dr Lalit Kumar Verma",
                    "designation": "Sam Higginbottom University of Agriculture, Technology, and Sciences (SHUATS), Prayagraj, UP, India.",
                    "link": "",
                    "quote": "",
                    "code": "02"
                }
            ]
        },
        {
            "journal_id": "004",
            "editors": [
                {
                    "name": "Dr. Anil Sarsavan",
                    "designation": "Editor-in-Chief (EIC), Senior Program Manager, Foundation For Ecological Security (FES), India",
                    "link": "https://in.linkedin.com/in/anil-sarsavan-41742765",
                    "quote": "Leading knowledge initiatives at FES India, the Editor-in-Chief and Senior Program Manager drives ecological security with expertise, strategy, and vision.",
                    "code": "01"
                },
                {
                    "name": "Dr. Manohar Pawar",
                    "designation": "Editor-in-Chief (EIC), Senior Program Manager, Foundation For Ecological Security (FES), India",
                    "link": "https://www.linkedin.com/in/manoohar-pawar-5ab8b1a1/?originalSubdomain=in",
                    "quote": "Guiding FES India with strategic insight, the Editor-in-Chief brings excellence to ecological security and editorial leadership.",
                    "code": "01"
                },
                {
                    "name": "Dr. Vipin Vyas",
                    "designation": "Professor, Department of Bioscience, Barkatullah University, Bhopal, Madhya Pradesh, India",
                    "link": "https://www.linkedin.com/in/vipin-vyas-04832619/?originalSubdomain=in",
                    "quote": "Expert in River Ecology, Aquatic Biodiversity, and Sustainable Aquaculture, focusing on freshwater ecosystem conservation and eco-friendly aquaculture practices.",
                    "code": "01"
                },
                {
                    "name": "Dr. Girdhari Lal Verma",
                    "designation": "Senior Program Manager, Foundation for Ecological Security (FES), India",
                    "link": "",
                    "quote": "Expertise in ecosystem restoration, natural resource management, rural livelihoods, and sustainable development.",
                    "code": "01"
                },
                {
                    "name": "Dr. Krishnendra Singh Nama",
                    "designation": "Senior Research Biologist, The Society for Conservation of Historical and Ecological Resources (SCHER), Kota, Rajasthan, India",
                    "link": "",
                    "quote": "Dedicated to ecological research, biodiversity conservation, and sustainable management of natural and cultural resources.",
                    "code": "01"
                },
                {
                    "name": "Dr Ritu Chaudhary",
                    "designation": "Professor, Department of Biotechnology, Indrusthli University, Rajpur, Gujrat, India.",
                    "link": "",
                    "quote": "Dedicated to biological research, biodiversity conservation, and sustainable management of natural and cultural resources.",
                    "code": "01"
                },
                {
                    "name": "Dr. Niharika Bhawsar",
                    "designation": "Assistant Professor, Department of Biotechnology, PM College of Excellence, Govt. Narmada College, Narmadapuram, MP, India",
                    "link": "https://www.linkedin.com/in/dr-niharika-bhawsar-a51269a9/?originalSubdomain=in",
                    "quote": "",
                    "code": "02"
                },
                {
                    "name": "Dr Jitendra Malviya",
                    "designation": "Assistant Professor, Department of Microbiology, Barkatullah University, Bhopal, MP, India",
                    "link": "https://orcid.org/0000-0001-7501-0121",
                    "quote": "",
                    "code": "02"
                },
                {
                    "name": "Dr Aswani Mishra",
                    "designation": "Prof. Department of Pharmaceutical Science, NINM, Indore, MP , India",
                    "link": "https://in.linkedin.com/in/dr-ashwani-mishra-41042754",
                    "quote": "",
                    "code": "02"
                },
                {
                    "name": "Dr Kuldeep Lakhera",
                    "designation": "Faculty of Botany, Veerangana Rani Durgava Govt. College, Tirodi, Balaghat, MP, India",
                    "link": "",
                    "quote": "",
                    "code": "02"
                },
                {
                    "name": "Dr Nisar Ahmad Ganie",
                    "designation": "Faculty, Department of Zoology, Government College Raghogarh, Guna (MP), India",
                    "link": "",
                    "quote": "",
                    "code": "02"
                },
                {
                    "name": "Dr. Shrikant Gangwar",
                    "designation": "Assistant Professor, Govt. Degree College, Timarni, Harda, Madhya Pradesh, India.",
                    "link": "",
                    "quote": "",
                    "code": "02"
                }
            ]
        },
        {
            "journal_id": "005",
            "editors": [
                {
                    "name": "Dr. Ritu Chaudhary",
                    "designation": "Editor-in-Chief (EIC)",
                    "quote": "Prof., Department of Medical Biotechnology, Indrashil University, Rajpur, Gujarat, India.",
                    "link": "",
                    "code": "01"
                },
                {
                    "name": "Dr. Ravi Prasad Mukku",
                    "designation": "Research Scientist",
                    "quote": "Department of Biomedical and Clinical Sciences (BKV), Division of Molecular Medicine and Virology (MMV), University of Michigan, USA.",
                    "link": "",
                    "code": "01"
                },
                {
                    "name": "Dr. Manoj Kumar Tembhre",
                    "designation": "Senior Scientist, Cardiac Biochemistry",
                    "quote": "All India Institute of Medical Sciences, New Delhi, India.",
                    "link": "https://www.aiims.edu/index.php/en/2014-12-17-09-43-36/2014-12-17-09-48-16",
                    "code": "01"
                },
                {
                    "name": "Dr. Anjali Jain",
                    "designation": "Professor",
                    "quote": "Pt. Khushilal Sharma Govt. (Auto) Ayurvedic College & Institute, Bhopal, MP, India.",
                    "link": "",
                    "code": "01"
                },
                {
                    "name": "Dr. Arpana Parihar",
                    "designation": "Scientist, Department of Translational Medicine",
                    "quote": "All India Institute of Medical Sciences, Bhopal, India.",
                    "link": "https://www.linkedin.com/in/drarpanaparihar/?originalSubdomain=in",
                    "code": "01"
                },
                {
                    "name": "Dr. Neeraj Shrivastava",
                    "designation": "Associate Professor",
                    "quote": "Amity Institute of Microbial Technology (AIMT), Amity University, Noida, UP, India.",
                    "link": "https://www.linkedin.com/in/dr-neeraj-shrivastava-95487640/?originalSubdomain=in",
                    "code": "01"
                },
                {
                    "name": "Dr. Akhilesh Kumar Singh",
                    "designation": "Director of Ayurveda & Dean of R&D",
                    "quote": "SAM Global University, Raisen, M.P., India. Ost. Doc. (CSIR, New Delhi), Ph.D. (Kaya Chikitsa), M.D. (Kaya Chikitsa), B.A.M.S., C.C.Y.P., Cert. in Multilingual Office Automation (C-DAC, GIST PACE)",
                    "link": "",
                    "code": "01"
                },
                {
                    "name": "Dr. Rohit Saluja",
                    "designation": "Prof. Department of Medical Biochemistry",
                    "quote": "All India Institute of Medical Sciences (AIIMS), Bibinagar, Hyderabad, Telangana, India.",
                    "link": "",
                    "code": "01"
                },
                {
                    "name": "Dr. Ashwin Kotnis",
                    "designation": "Prof. Department of Biochemistry",
                    "quote": "All India Institute of Medical Sciences, Bhopal, India.",
                    "link": "",
                    "code": "01"
                },
                {
                    "name": "Dr. Suyash Bhadoriya",
                    "designation": "MD (Internal Medicine), Assistant Professor",
                    "quote": "RKDF Medical College; Head of Department, Medicine, Shree Multispeciality Hospital, Bhopal, Madhya Pradesh, India.",
                    "link": "",
                    "code": "01"
                },
                {
                    "name": "Dr. Amit Singh",
                    "designation": "MD (Pulmonary Medicine)",
                    "quote": "Head of Pulmonary Department, Shree Multispeciality Hospital; Assistant Professor, People’s Medical College, People’s University, Bhopal, Madhya Pradesh, India.",
                    "link": "",
                    "code": "01"
                },
                {
                    "name": "Prof. R.N. Mishra",
                    "designation": "Pioneer in Mental Health through Palmistry",
                    "quote": "Former Director of Finance, Government of Madhya Pradesh. Now focused on holistic research in mind sciences and palmistry.",
                    "link": "",
                    "code": "01"
                },
                {
                    "name": "Dr. Ajay Haldar",
                    "designation": "Consultant Gynecologist & Endopelvic Surgeon",
                    "quote": "Bansal Hospital, Bhopal, Madhya Pradesh, India; Former Professor, Department of Obstetrics & Gynaecology, AIIMS Bhopal, India.",
                    "link": "",
                    "code": "01"
                },
                {
                    "name": "Dr. NP Tiwari",
                    "designation": "HistoPathologist",
                    "quote": "M.P. Birla Hospital and Priyambda Birla Cancer Hospital and Research Institute, Satna, India.",
                    "link": "",
                    "code": "01"
                },
                {
                    "name": "Dr. Neha Agnihotri",
                    "designation": "B.H.M.S., MD (Hom.)",
                    "quote": "Advisor, WeServe Organization, Delhi, India; Former Assistant Professor, Anushree Homeopathic Medical College & Hospital, Jabalpur, M.P., India.",
                    "link": "",
                    "code": "01"
                },
                {
                    "name": "Dr. Pratibha Thakur",
                    "designation": "Research Scientist",
                    "quote": "Research Scientist at the (ICMR-Department of Health Research), Department of Medicine, Indira Gandhi Medical College, Shimla",
                    "link": "",
                    "code": "02"
                },
                {
                    "name": "Dr Jitendra Singh",
                    "designation": "Professor",
                    "quote": "Professor, Department of Physiotherapy, LN Medical College, LNCT University, Bhopal, India",
                    "link": "",
                    "code": "02"
                },
                {
                    "name": "Dr Pankaj Dipankar",
                    "designation": "Research Scientist",
                    "quote": "Research Scientist, National Institutes of Health (NIH), Bethesda, United States",
                    "link": "",
                    "code": "02"
                },
                {
                    "name": "Dr. Bhanu Pratap Singh",
                    "designation": "MBBS, DNB (Orthopedics)",
                    "quote": "MBBS, DNB (Orthopedics), Gajra Raja Medical College and Jayarogya Hospital, Gwalior, India",
                    "link": "",
                    "code": "02"
                },
                {
                    "name": "Dr PK Dipankar",
                    "designation": "MBBS, MD",
                    "quote": "MBBS, MD, Department of Public Health and Medical Education, Govt of MP, India",
                    "link": "",
                    "code": "02"
                },
                {
                    "name": "Dr. Priyanshi Mahajan",
                    "designation": "BDS, MDS (Orthodontics)",
                    "quote": "BDS, MDS (Orthodontics), Dentist and Clinical Expert",
                    "link": "",
                    "code": "02"
                },
                {
                    "name": "Dr. Vanshika Jain",
                    "designation": "Senior Clinical Embryologist",
                    "quote": "Senior Clinical Embryologist, Cellsure Biotech & Research Centre, Mumbai, India",
                    "link": "",
                    "code": "02"
                }
            ]
        }
    ]

    total_inserted = 0
    total_skipped = 0

    for journal_info in journals_data:
        journal_id = journal_info["journal_id"]
        journal = JournalMaster.query.filter_by(journal_id=journal_id).first()

        if not journal:
            print(f" Journal with ID {journal_id} not found. Skipping...")
            continue
            
        print(f" Processing Journal: {journal.full_name} (ID: {journal_id})")

        # Har journal ke editors ko insert karein
        for editor_data in journal_info["editors"]:
            # Journal ID add karein
            editor_data["journal_id"] = journal.journal_id
            editor_data["journal"] = journal
            
            # Duplicate code check
            existing_editor = EditorBoard.query.filter_by(name=editor_data["name"], link=editor_data["link"], journal_id=editor_data["journal_id"]).first()
            if existing_editor:
                print(f" Editor with code {editor_data['code']} already exists — skipping insert.")
                total_skipped += 1
            else:
                # Add editor to database
                editor = EditorBoard(**editor_data)
                db.session.add(editor)
                total_inserted += 1
                print(f"Added: {editor_data['name']} ({editor_data['code']})")

    # Commit all changes
    db.session.commit()
    
    # Final summary
    print(f"\n Final Summary:")
    print(f" Successfully inserted: {total_inserted} editors")
    print(f" Skipped (duplicates): {total_skipped} editors")
    
    # Verification - sab editors dikhayein
    all_editors = EditorBoard.query.all()
    print(f"\n All editors in database ({len(all_editors)} total):")
    for editor in all_editors:
        print(f"→ {editor.code}: {editor.name} | {editor.designation} | Journal ID: {editor.journal_id}")