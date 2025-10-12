import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main_app.extensions import app, db
from main_app.models import JournalMaster, ResearchPaper


with app.app_context():
    research_papers_data = [
        {
            "main_heading": "Water Quality Research",
            "sub_heading": "Assessment of Narmada River during COVID-19 Lockdown",
            "title": "Assessment of Water Quality of Narmada River in COVID-19 Pandemic",
            "authors": "Manohar Pawar, Kaleem Shah, and Seema Dhurvey",
            "volume": "1",
            "issue": "1",
            "year": 2025,
            "abstract": "In the present study, the quality of the surface water of the Narmada River (Mandla, Madhya Pradesh) was investigated. Mandla is situated in the eastern part of Madhya Pradesh, part Gondwana tract, a forest-dominated upper valley, and the plateau of the Maikal Hill Ranges. Recently, Mandla has experienced unregulated development activities and rapid population growth in recent decades, both of which have had negative impacts on its ecosystem and environment. Seven sample sites of the Narmada River and its tributaries were selected and water was collected and they were analyzed for a total of five different parameters. The observed data were analyzed using a portable multi-parameter and DO meter. We have undertaken water quality assessments for the Narmada River in Mandla City and its tributaries in the upper catchment area (Surpan, Matiyari, Halon Banjar, and Gour River). During the lockdown, the water quality of the Narmada River in Mandla City has been significantly improved in pH, DO, and TDS physicochemical properties. The study will help set up a baseline for river pollution in Mandla City. It will also help generate awareness among the decision-makers, media, and general public about the water quality in the river Narmada and the contribution of its tributaries to its health.",
            "pdf_filename": "crin/Paper_No_CRIN001.pdf",
            "citation": "Pawar Manohar, Shah Kaleem, and Dhurvey Seema. (2025). Assessment of Water Quality of Narmada River in COVID-19 pandemic and comparison with water quality of its tributaries in Mandla, Madhya Pradesh. Curevita Research International Nexus (CIRN), 1, 1-9.",
            "image_filename": "default_paper_bg.jpg",
            "journal_id": "002",
            "is_archive": True
        },
        {
            "main_heading": "Entomological Research",
            "sub_heading": "First Record of Leaf Beetle Platypria erinaceus from Rajasthan, India",
            "title": "Leaf Beetle Platypria erinaceus (Fabricius, 1801) First Record from Rajasthan, India",
            "authors": "Anil Sarsavan, Manohar Pawar, Satish Kumar Sharma",
            "volume": "1",
            "issue": "1",
            "year": 2025,
            "abstract": "The leaf beetle Platypria erinaceus is reported for the new addition to the fauna of Rajasthan state, India. Although it is also distributed from other parts of Asia, including India, this study confirms the beetle's presence in Chhalwa village, Udaipur district, Rajasthan, significantly expanding its known distribution within the country. Globally, Platypria erinaceus has garnered attention for its reported potential as a biological control agent against Ziziphus maurtitana, an invasive plant species in certain parts of the world. The beetles were observed on the extremities of the Indian jujube plant (Ziziphus nummularia) in a pasture land dominated by perennial grasses. This record extends the known range of P. erinaceus in India considerably westward, as previous records were primarily from southern, northern and eastern regions of India. Despite its specialized feeding behavior, Platypria erinaceus has not been reported to cause crop damage in India. However, its host specificity has been strategically utilized in other regions, particularly as a biological control agent against invasive Ziziphus mauritiana in Australia.",
            "pdf_filename": "crin/Paper_No_CRIN002.pdf",
            "citation": "Sarsavan Anil, Pawar Manohar, Sharma Satish Kumar. (2025). Leaf Beetle Platypria erinaceus (Fabricius, 1801) First Record from Rajasthan, India. Curevita Research International Nexus (CIRN), Volume 1, Issue 1, 10–15.",
            "image_filename": "default_paper_bg.jpg",
            "journal_id": "002",
            "is_archive": True
        },
        {
            "main_heading": "Biotechnology Research",
            "sub_heading": "Genetic Fidelity Assessment of Micropropagated Glycyrrhiza glabra L. using RAPD Markers",
            "title": "Assessment of Genetic Fidelity of In vitro Micropropagated Plants of Glycyrrhiza glabra L. using Random Amplified Polymorphic DNA Technique (RAPD)",
            "authors": "Yogesh Badkhane, Sourav Datta, A.S. Yadav, Souvika Bakshi",
            "volume": "1",
            "issue": "1",
            "year": 2025,
            "abstract": "Random amplified polymorphic DNA (RAPD) markers were employed to determine the genetic fidelity of Glycyrrhiza glabra L. plantlets multiplied through in vitro micropropagation technique. Twenty RAPD primers were screened, of which 16 primers generated a total of 605 clear, distinct and reproducible bands. Out of 605 bands, 429 (70.91%) were monomorphic and 176 (29.09%) were polymorphic. The similarity values amongst the plants varied from 0.788 to 1.000. A UPGMA dendrogram constructed to show genetic similarity among 11 plants (10 micropropagated and 1 mother plant) revealed 98% similarity among them. Glycyrrhiza glabra L., commonly known as liquorice or sweet wood, is an important medicinal plant cultivated for its rhizomes containing glycyrrhizin, which is 50 times sweeter than sugar. Maintaining genetic similarity is one of the major concerns in tissue culture techniques, and this study demonstrates that RAPD markers are effective tools for assessing genetic fidelity. The present study exhibited successful application of the RAPD marker technique for molecular profiling and assessment of the genetic fidelity of micropropagated plants of Glycyrrhiza glabra L., confirming the clonal stability and reliability of the propagation protocol for this important medicinal species.",
            "pdf_filename": "crin/Paper_No_CRIN003.pdf",
            "citation": "Badkhane Yogesh, Datta Sourav, Yadav A.S., Bakshi Souvika. (2025). Assessment of Genetic Fidelity of In vitro Micropropagated Plants of Glycyrrhiza glabra L. using Random Amplified Polymorphic DNA Technique (RAPD). Curevita Research International Nexus (CIRN), Volume 1, Issue 1, 16–34.",
            "image_filename": "default_paper_bg.jpg",
            "journal_id": "002",
            "is_archive": True
        },
        {
            "main_heading": "Environmental Research",
            "sub_heading": "Impacts of Mining Activities on Groundwater in Tiroid Region, Balaghat District",
            "title": "Impacts of Mining Activities on the Physicochemical Properties of Groundwater in Tiroid Region Balaghat District: A Comprehensive Review",
            "authors": "Kuldeep Lakhera",
            "volume": "1",
            "issue": "1",
            "year": 2025,
            "abstract": "This review paper explores the relationship between mining activities and the physicochemical properties of groundwater in the Tiroid region of Balaghat District, Madhya Pradesh. Mining operations have profound implications on the quality and availability of groundwater resources, disturbing parameters such as pH, metal concentrations, and overall water chemistry. The paper examines the diverse mechanisms through which mining activities alter groundwater characteristics, including acid mine drainage, leaching of heavy metals, and subsidence-related impacts. The study highlights significant environmental concerns, showing how coal mining often exposes sulfur-bearing rocks leading to acidic drainage that mobilizes heavy metals, threatening both human health and aquatic ecosystems. Research from various Indian mining regions demonstrates that water in these areas frequently becomes unsuitable for domestic and industrial use without proper treatment. The paper concludes with an evaluation of potential mitigation strategies, emphasizing the need for sustainable mining practices, effective water management, and regular environmental monitoring to safeguard this vital water source for the region's population and ecosystems.",
            "pdf_filename": "crin/Paper_No_CRIN004.pdf",
            "citation": "Lakhera Kuldeep. (2025). Impacts of Mining Activities on the Physicochemical Properties of Groundwater in Tiroid Region Balaghat District: A Comprehensive Review. Curevita Research International Nexus (CIRN), Volume 1, Issue 1, 35–41.",
            "image_filename": "default_paper_bg.jpg",
            "journal_id": "002",
            "is_archive": True
        },
        {
            "main_heading": "Hydrological Research",
            "sub_heading": "Spatiotemporal Analysis of Groundwater Levels in Ujjain City (2022–2025)",
            "title": "Spatiotemporal Analysis of Groundwater Levels in Ujjain City: 2022 to 2025",
            "authors": "Ishwar Sharma, Harish Vyas, D.M. Kumawat",
            "volume": "1",
            "issue": "1",
            "year": 2025,
            "abstract": "This study investigates the trends and variations in groundwater levels across Wards 1 to 20 of Ujjain city from 2022 to 2025. Primary and secondary data collected from piezometers and municipal records were analyzed to understand seasonal fluctuations and long-term decline. The results indicate significant depletion in groundwater levels in highly populated and tourism-centric zones, especially near religious hubs like Mahakal Lok. The research reveals that wards near religious centers experienced the sharpest decline, with water levels reaching 13 meters below ground level (mbgl) by 2025. Seasonal recharge during monsoons proved temporary and insufficient to compensate for high withdrawal rates throughout the year. The paper emphasizes the urgent need for effective water management practices, especially rainwater harvesting and aquifer recharge, to ensure sustainable groundwater use in these wards. Recommendations include strict regulation of private borewells and rehabilitation of traditional water structures to mitigate the growing water crisis in this historically significant city.",
            "pdf_filename": "crin/Paper_No_CRIN005.pdf",
            "citation": "Sharma Ishwar, Vyas Harish, Kumawat D.M. (2025). Spatiotemporal Analysis of Groundwater Levels in Ujjain City: 2022 to 2025. Curevita Research International Nexus (CIRN), Volume 1, Issue 1, 42–47.",
            "image_filename": "default_paper_bg.jpg",
            "journal_id": "002",
            "is_archive": True
        },
        {
            "main_heading": "AI and Deep Learning Research",
            "sub_heading": "AI and Deep Learning for Anemia Prediction",
            "title": "A Comprehensive Review on Using Artificial Intelligence and Deep Learning to Predict Anemia in Humans",
            "authors": "Shreya Sharma",
            "volume": "1",
            "issue": "1",
            "year": 2025,
            "abstract": "Anemia, a global health concern affecting over 2 billion people, is traditionally diagnosed through invasive and resource-intensive blood tests. These methods can be a hassle, expensive, and sometimes impossible to access, especially in low resource settings. This review paper synthesizes key research on how Artificial Intelligence (AI) and Deep Learning (DL) are transforming diagnostics by developing non-invasive, accessible, and scalable alternatives. Instead of drawing blood, AI models are being trained to analyze subtle physiological changes. The research in this domain primarily focuses on leveraging visual and physiological data that can be captured easily, often with a smartphone.",
            "pdf_filename": "cibdi/CIBDI_Paper_ID_01.pdf",
            "citation": "Sharma Shreya. (2025). A Comprehensive Review on Using Artificial Intelligence and Deep Learning to Predict Anemia in Humans. Curevita Innovation of BioData Intelligence (CIBDI), Volume 1, Issue 1, 1–8.",
            "image_filename": "default_paper_bg.jpg",
            "journal_id": "001",
            "is_archive": True
        },
        {
            "main_heading": "Data Science",
            "sub_heading": "Data Science integrates statistics, computing, and domain expertise to derive insights from data.",
            "title": "Data Science: An Emerging Interdisciplinary Field",
            "authors": "Nitin Kumar Dhimole",
            "volume": "1",
            "issue": "1",
            "year": 2025,
            "abstract": "Data Science is an interdisciplinary domain that combines statistical analysis, computer science, and domain expertise to extract meaningful insights from structured and unstructured data. The rapid expansion of big data and artificial intelligence has positioned Data Science as a crucial field for innovation, research, and business decision-making. This paper explores the fundamentals, applications, challenges, and future directions of Data Science.",
            "pdf_filename": "cibdi/CIBDI_Paper_ID_02.pdf",
            "citation": "Dhimole Nitin Kumar. (2025). Data Science: An Emerging Interdisciplinary Field. Curevita Innovation of BioData Intelligence (CIBDI), Volume 1, Issue 1, 9–12.",
            "image_filename": "default_paper_bg.jpg",
            "journal_id": "001",
            "is_archive": True
        },
        {
            "main_heading": "Machine Learning",
            "sub_heading": "Machine Learning enables systems to learn from data without explicit programming",
            "title": "A Comprehensive Study on Machine Learning: Concepts, Applications, Challenges, and Future Directions",
            "authors": "Vinod Kumar Sharma",
            "volume": "1",
            "issue": "1",
            "year": 2025,
            "abstract": "Machine Learning (ML) has emerged as a transformative technology at the intersection of computer science, statistics, and artificial intelligence. It enables systems to learn patterns from data and improve performance without being explicitly programmed. This research paper provides an in-depth study of machine learning concepts, types, applications across industries, challenges, and future scope. The paper highlights how ML is shaping decision-making, automation, and innovation, while also discussing ethical and technical limitations.",
            "pdf_filename": "cibdi/CIBDI_Paper_ID_03.pdf",
            "citation": "Sharma Vinod Kumar. (2025). A Comprehensive Study on Machine Learning: Concepts, Applications, Challenges, and Future Directions. Curevita Innovation of BioData Intelligence (CIBDI), Volume 1, Issue 1, 13–16.",
            "image_filename": "default_paper_bg.jpg",
            "journal_id": "001",
            "is_archive": True
        },
        {
            "main_heading": "Internet of Things",
            "sub_heading": "IoT connects physical devices for seamless communication",
            "title": "The Internet of Things (IoT): Opportunities, Challenges, and Future Scope",
            "authors": "Priyadarshini Bharthare",
            "volume": "1",
            "issue": "1",
            "year": 2025,
            "abstract": "The Internet of Things (IoT) represents a technological revolution that enables physical devices to communicate and interact over the internet. This paper explores the architecture, applications, advantages, challenges, and future potential of IoT. With the increasing integration of Artificial Intelligence (AI), 5G, and edge computing, IoT is transforming industries, cities, and human life. The research also highlights security issues and the need for global standards for successful IoT adoption.",
            "pdf_filename": "cibdi/CIBDI_Paper_ID_04.pdf",
            "citation": "Bharthare Priyadarshini. (2025). The Internet of Things (IoT): Opportunities, Challenges, and Future Scope. Curevita Innovation of BioData Intelligence (CIBDI), Volume 1, Issue 1, 17–21.",
            "image_filename": "default_paper_bg.jpg",
            "journal_id": "001",
            "is_archive": True
        },
        {
            "main_heading": "Big Data",
            "sub_heading": "Big Data is transforming industries and society",
            "title": "Big Data: Challenges, Technologies, and Future Directions in Transforming Business Intelligence and Decision Making",
            "authors": "Sitesh Kumar Sinha",
            "volume": "1",
            "issue": "1",
            "year": 2025,
            "abstract": "The concept of Big Data refers to massive, complex, and rapidly growing datasets that cannot be handled using traditional database systems. Big Data provides organizations with the ability to extract meaningful insights, improve decision-making, and drive innovation. This paper explores the definition of Big Data, its characteristics, tools and technologies, applications across sectors, challenges, and future directions. The study concludes that Big Data, coupled with artificial intelligence (AI), machine learning (ML), and cloud computing, will revolutionize industries and society.",
            "pdf_filename": "cibdi/CIBDI_Paper_ID_05.pdf",
            "citation": "Sinha, Sitesh Kumar. (2025). Big Data: Challenges, Technologies, and Future Directions in Transforming Business Intelligence and Decision Making. Curevita Innovation of BioData Intelligence (CIBDI), Volume 1, Issue 1, 22–26.",
            "image_filename": "default_paper_bg.jpg",
            "journal_id": "001",
            "is_archive": True
        },
        {
            "main_heading": "Biodegradation Research",
            "sub_heading": "Enhancing Biodegradation of Methyl-Parathion by Aspergilli sp.",
            "title": "Enhancing Biodegradation of Methyl-Parathion By Aspergilli Sp. from Indian Agricultural Soil",
            "authors": "Akanksha Khare, Ashutosh Gupta, Naveen Kango, Kailash Prasad Jaiswal",
            "volume": "1",
            "issue": "1",
            "year": 2025,
            "abstract": "The fungal strain Aspergilli isolated from Indian agricultural soil was evaluated for its ability to biodegrade methyl-parathion. The study revealed that Aspergilli showed significantly better degradation at 36 hours compared to Kosakonia strains. Using HPLC-UV, HPLC-ToF, and GC-MS analysis, it was confirmed that methyl-parathion was fully transformed within 24 hours, initially hydrolyzing into p-nitrophenol followed by further biotransformation. Aspergillus niger demonstrated maximum methyl-parathion hydrolase (MPH) activity and produced rapid biotransformation. The pathway involved nitro group reduction, amine acetylation, and subsequent hydrolysis into N-(4-hydroxyphenyl) acetamide. The findings indicate a promising potential of Aspergilli in bioremediation of pesticide-contaminated soils.",
            "pdf_filename": "faai/Khare_et_al2025FAAI_Papere_ID_001.pdf",
            "citation": "Khare A., Gupta A., Kango N., Jaiswal K.P. (2025). Enhancing Biodegradation of Methyl-Parathion By Aspergilli Sp. from Indian Agricultural Soil. Frontiers of Agri and Animal Innovation (FAAI), Volume 1, Issue 1, 1–18. DOI: https://doi.org/10.1000/001",
            "image_filename": "default_paper_bg.jpg",
            "journal_id": "003",
            "is_archive": True
        },
        {
            "main_heading": "Animal Nutrition Research",
            "sub_heading": "Effect of Strategic Nutrient Supplementation on Growth Performance of Murrah Buffalo Calves",
            "title": "To evaluate the effect of strategic nutrient supplementation on the growth performance of Murrah buffalo calves",
            "authors": "Neeha Meena, Sandeep Nanavati, Mohabbat Singh Jamra, Ashok Kumar Patil, Nawal Singh Rawat, Danveer Singh Yadav",
            "volume": "1",
            "issue": "1",
            "year": 2025,
            "abstract": "A feeding trial was conducted on eighteen Murrah buffalo calves (6–9 months) to evaluate the effect of strategic nutrient supplementation on growth performance. Animals were divided into three groups: a control group and two treatment groups supplemented with macro- and micronutrients. The results indicated that supplemented groups had significantly higher dry matter intake, improved average daily gain, and better feed conversion efficiency compared to the control. This study suggests that strategic nutrient supplementation enhances feed utilization and growth in Murrah buffalo calves, highlighting its potential application in livestock production systems.",
            "pdf_filename": "faai/Meena_et_al2025_FAAI_paper_ID_002.pdf",
            "citation": "Meena N., Nanavati S., Jamra M.S., Patil A.K., Rawat N.S., Yadav D.S. (2025). To evaluate the effect of strategic nutrient supplementation on the growth performance of Murrah buffalo calves. Frontiers of Agri and Animal Innovation (FAAI), Volume 1, Issue 1, 19–25.",
            "image_filename": "default_paper_bg.jpg",
            "journal_id": "003",
            "is_archive": True
        },
        {
            "main_heading": "Environmental Biotechnology",
            "sub_heading": "Bioremediation Potential of Hydrocarbon-Degrading Fungi from Select Soil Niches of India",
            "title": "Bioremediation Potential of Hydrocarbon-Degrading Fungi from Select Soil Niches of India",
            "authors": "Ashutosh Gupta, Akanksha Khare, Naveen Kango, Kailash Prasad Jaiswal",
            "volume": "1",
            "issue": "1",
            "year": 2025,
            "abstract": "Petroleum hydrocarbons from human activities are a major source of soil contamination, especially in developing countries like India. This study explores the bioremediation potential of hydrocarbon-degrading fungi isolated from oil-contaminated soils. Various fungi including Fusarium sp., Rhizopus sp., Trichoderma harzianum and Aspergillus versicolor were found to efficiently degrade hydrocarbons such as naphthalene, acenaphthene, and anthracene. Methylene blue reduction tests and biomass analysis confirmed their strong hydrocarbon biodegradation ability. Results demonstrated that fungal isolates could effectively degrade hydrocarbons, with Fusarium and Trichoderma species showing the highest efficiency. The study highlights fungi as eco-friendly, cost-effective candidates for cleaning up petroleum hydrocarbon-polluted soils. The findings suggest that indigenous fungi can be developed into bioremediation agents for sustainable and environment-friendly management of hydrocarbon pollution.",
            "pdf_filename": "faai/Gupta_etal2025_FAAI_Paper_ID_003.pdf",
            "citation": "Gupta A., Khare A., Kango N., Jaiswal K.P. (2025). Bioremediation Potential of Hydrocarbon-Degrading Fungi from Select Soil Niches of India. Frontiers of Ecovitality & Resilient Innovation (FERI), Volume 1, Issue 1, 45–63. DOI: https://doi.org/10.1000/002",
            "image_filename": "default_paper_bg.jpg",
            "journal_id": "003",
            "is_archive": True
        },
        {
            "main_heading": "Poultry Genetics Research",
            "sub_heading": "Study of Polymorphism at MHC B-Lβ (Class II) Family Alleles Using PCR-SSP in Naked Neck Chickens",
            "title": "Study of Polymorphism at MHC B-Lβ (Class II) Family Alleles Using PCR-SSP in Naked Neck Chickens",
            "authors": "Amit Kumar Jha, M. S. Thakur, S.S. Tomar, R. K. Vandre",
            "volume": "1",
            "issue": "1",
            "year": 2025,
            "abstract": "The Major Histocompatibility Complex (MHC) plays a crucial role in disease resistance and immune response in poultry. This study investigated the polymorphism at MHC B-Lβ (class II) family alleles in Naked Neck chickens using the Polymerase Chain Reaction-Sequence Specific Primers (PCR-SSP) technique. Sixty Naked Neck chickens were analyzed for five standard haplotypes (B2, B13, B15, B19, and B21). The results revealed significant genetic diversity with 10 distinct genotypes identified. Allele B19 showed the highest frequency (0.392), followed by B15 (0.258), B2 (0.183), B21 (0.125), and B18 (0.042). The population showed Hardy-Weinberg disequilibrium (χ² = 36.179, P<0.05), indicating non-random mating or selection pressure. These findings provide valuable insights into the genetic structure of Naked Neck chickens and their potential for disease resistance breeding programs.",
            "pdf_filename": "faai/Jha_et_al2025_FAAI_Paper_ID_04.pdf",
            "citation": "Jha A.K., Thakur M.S., Tomar S.S., Vandre R.K. (2025). Study of Polymorphism at MHC B-Lβ (Class II) Family Alleles Using PCR-SSP in Naked Neck Chickens. Frontiers of Agri & Animal Innovation, Volume 1, Issue 1, 64–78.",
            "image_filename": "default_paper_bg.jpg",
            "journal_id": "003",
            "is_archive": True
        },
        {
            "main_heading": "Biogas Research",
            "sub_heading": "Influence of different cultural parameters in biogas production using university food waste",
            "title": "Influence of different cultural parameters in the production of biogas using university food waste in Telangana State of India",
            "authors": "Punam Sharnagat, KP Jaiswal",
            "volume": "1",
            "issue": "1",
            "year": 2025,
            "abstract": "This study examined the effect of pH and incubation period on biogas production using university food waste compared with cow dung and sheep waste. Results showed cow dung produced the highest biogas yield (20ml/72hours) followed by sheep manure (15ml/72hours). Alkaline pH and anaerobic dark conditions were optimal for biogas production Biogas, Methane, Anaerobic, food waste, cow dung",
            "pdf_filename": "faai/Sharnagat_2025_FAAI_Paper_ID_05.pdf",
            "citation": "Sharnagat P. (2025). Influence of different cultural parameters in the production of biogas using university food waste in Telangana State of India. Frontiers of Agri and animal Innovation, Volume 1, Issue 1, 79–87.",
            "image_filename": "default_paper_bg.jpg",
            "journal_id": "003",
            "is_archive": True
        },
        {
            "main_heading": "Environmental Research",
            "sub_heading": "Global Trade, Climate Change, and the Spread of Invasive Alien Species",
            "title": "Global Trade, Climate Change, and the Spread of Invasive Alien Species: Impacts on Ecosystem Services",
            "authors": "Babaharinand Saket, Anand Chaurasia",
            "volume": "1",
            "issue": "1",
            "year": 2025,
            "abstract": "The accelerating pace of global trade and climate change has significantly influenced ecological stability worldwide. One of the most critical consequences of these processes is the spread of Invasive Alien Species (IAS), increasingly transported across regions through trade activities and thriving in new environments due to changing climatic conditions. Findings reveal that IAS follow major trade routes, with climate change enhancing their survival and establishment in diverse habitats. The resulting invasions pose serious threats to provisioning, regulating, supporting, and cultural ecosystem services, disrupting biodiversity and ecosystem functions vital to human well-being. It emphasizes the urgent need for integrated strategies combining ecological, economic, and regulatory approaches to mitigate the impacts of IAS and safeguard ecosystem resilience. This research contributes to informed policymaking and sustainable environmental management in the face of global change.",
            "pdf_filename": "feri/Saket_2025_FERI_Paper_ID_01.pdf",
            "citation": "Saket Babaharinand and Chaurasia Anand. 2025. Global Trade, Climate Change, and the Spread of Invasive Alien Species: Impacts on Ecosystem Services. Frontiers in Environmental Revolutionary Innovation (FERI), 1(2), 1-12.",
            "image_filename": "default_paper_bg.jpg",
            "journal_id": "004",
            "is_archive": True
        },
        {
            "main_heading": "Environmental Research",
            "sub_heading": "Biodiversity Conservation and Phytodiversity Assessment in the Catchment Area of Runjh Dam, Panna (M.P.)",
            "title": "Biodiversity Conservation and Phytodiversity Assessment in the Catchment Area of Runjh Dam, Panna (M.P.)",
            "authors": "Pratima Dahayat, Anand Chaurasia",
            "volume": "1",
            "issue": "1",
            "year": 2025,
            "abstract": "The study analyzes the effects of the Runjh Dam catchment on phytodiversity in Panna, Madhya Pradesh. Quadrat and transect-based vegetation analysis, supported by satellite imagery and GIS mapping, revealed major changes in the distribution, abundance, and diversity of plant species. While increased water availability has enhanced agroforestry potential and soil moisture, the dam has also submerged forests, leading to habitat fragmentation, disappearance of endemic fauna, and changes in soil chemistry. Exotic species invasion and microclimate alteration further intensify ecological stress. The study recommends afforestation programs, buffer zones, invasive species monitoring, and long-term ecological surveillance to ensure sustainable development. Local community participation and biodiversity-based strategies are essential to balance development with ecological conservation.",
            "pdf_filename": "feri/Dahayat_And_Chaurasia_2025_FERI_Paper_No_02.pdf",
            "citation": "Dahayat Pratima and Chaurasia Anand. 2025. Biodiversity Conservation and Phytodiversity Assessment in the Catchment Area of Runjh Dam, Panna (M.P.). Frontiers in Environmental Revolutionary Innovation (FERI), 1(2), 13–20.",
            "image_filename": "default_paper_bg.jpg",
            "journal_id": "004",
            "is_archive": True
        },
        {
            "main_heading": "Aquatic Biodiversity Research",
            "sub_heading": "Macroinvertebrates as Indicators of Trophic Status & Water Quality of Kaliasote Dam",
            "title": "Macroinvertebrates as a Tool to Assess the Trophic Status and Water Quality of Kaliasote Dam",
            "authors": "Nisar Ahmad Ganie, Zahoor Ahmad Malik",
            "volume": "1",
            "issue": "1",
            "year": 2025,
            "abstract": "An ecological assessment of Kaliasote Dam was conducted to evaluate the diversity of macroinvertebrates and their role in determining the trophic status and water quality. A total of 56 species were recorded, with Arthropoda being the dominant group (32 species), followed by Mollusca (17) and Annelida (7). Seasonal variations showed higher species richness in summer compared to monsoon. Chemical parameters confirmed that Kaliasote Dam falls under the eutrophic category. However, the abundance of tolerant species like Chironomus sp. and Culex sp. indicates moderate to severe pollution in parts of the dam. Biodiversity indices (Simpson & Shannon-Weaver) confirmed moderate diversity, while biotic indices (BMWP & ASPT) highlighted varying water quality from clean to heavily polluted across sampling stations. The study concludes that Kaliasote Dam is moderately polluted with clear eutrophic tendencies, emphasizing the urgent need for ecological monitoring and pollution control strategies.",
            "pdf_filename": "feri/Ganieet_al_2025_FERI_Paper_03.pdf",
            "citation": "Ganie, N.A. and Malik, Z.A. 2025. Macroinvertebrates as a tool to assess the trophic status and water quality of Kaliasote Dam. Frontiers in Environmental Revolutionary Innovation (FERI), 1(2), 21–33.",
            "image_filename": "default_paper_bg.jpg",
            "journal_id": "004",
            "is_archive": True
        },
        {
            "main_heading": "Nutrition & Sustainability Research",
            "sub_heading": "Phytochemical and Nutritional Insights into Edible Bamboo Shoots: Bioactives, Processing, and Sustainability",
            "title": "Phytochemical and Nutritional Insights into Edible Bamboo Shoots: Bioactives, Processing, and Sustainability",
            "authors": "Sunita Tiwari, Priyanka Tiwari",
            "volume": "1",
            "issue": "1",
            "year": 2025,
            "abstract": "Bamboo shoots represent a significant underutilized food resource with exceptional nutritional and phytochemical properties. This comprehensive research paper examines the nutritional composition, bioactive compounds, processing methods, and sustainability aspects of edible bamboo shoots across multiple species. The study reveals that bamboo shoots contain superior levels of protein (3.71g/100g), dietary fiber (3.94g/100g), and essential minerals compared to common vegetables, while providing valuable phytochemicals including phenolic compounds, phytosterols, and amino acids. Through systematic analysis of processing methods, we demonstrate that toxic cyanogenic glycosides can be effectively reduced by 96% through proper treatment, making bamboo shoots safe for consumption. The environmental benefits of bamboo cultivation, including carbon sequestration rates of 12-60 tons CO2/hectare/year and rapid growth characteristics, position bamboo shoots as a sustainable solution for food security and climate change mitigation.",
            "pdf_filename": "feri/Tiwari_2025_FERI_Paper_ID_04.pdf",
            "citation": "Tiwari S., Tiwari P. 2025. Phytochemical and Nutritional Insights into Edible Bamboo Shoots: Bioactives, Processing, and Sustainability. Frontiers in Environmental Revolutionary Innovation, 1(2), 34–51.",
            "image_filename": "default_paper_bg.jpg",
            "journal_id": "004",
            "is_archive": True
        },
        {
            "main_heading": "Ornithological Research",
            "sub_heading": "First Record of a Leucistic Indian Pied Starling (Gracupica contra) from Keonjhar, Odisha, India",
            "title": "First Record of a Leucistic Indian Pied Starling (Gracupica contra) from Keonjhar, Odisha, India",
            "authors": "Anil Sarsavan, Satish Kumar Sharam, Manohar Pawar",
            "volume": "1",
            "issue": "1",
            "year": 2025,
            "abstract": "We report a leucistic Indian Pied Starling (Gracupica contra) observed in Keonjhar District, Odisha, India. In contrast to albinism, the individual's large white feathers and preserved black soft-part pigmentation (normal eye and bill) were consistent with leucism, a partial loss of melanin deposition. According to the published record, this is one of the few reports of leucism in G. contra from eastern India and the first recorded case from Keonjhar. The observation was made on 17 December 2024 in the Samantaraypur Sasan area (21.62°N, 85.59°E) of Keonjhar city. The bird's overall body was predominantly white with a dirty-blackish cap, black primaries and black tail. The throat and back were also white in color. The basal parts of the upper and lower mandibles were orange, but the distal parts were whitish. Skin around the eyes was orange and the eyes were of reddish color. Its legs were pale-pinkish. In addition to field documentation and a brief differential diagnosis that distinguishes leucism from albinism and progressive greying, this note also addresses the potential ecological and conservation significance of these pigment abnormalities.",
            "pdf_filename": "feri/Sarsavan_etal_2025_FERI_Paper_ID_05.pdf",
            "citation": "Sarsavan A., Sharam S.K., Pawar M. 2025. First Record of a Leucistic Indian Pied Starling (Gracupica contra) from Keonjhar, Odisha, India. Frontiers in Environmental Revolutionary Innovation, 1(2), 52–57.",
            "image_filename": "default_paper_bg.jpg",
            "journal_id": "004",
            "is_archive": True
        },
        {
            "main_heading": "Urban Research",
            "sub_heading": "Geo-Spatial Insights into Urban Sprawl and Land Use Transformation: A GIS-Based Case Study of Narsinghgarh, Madhya Pradesh",
            "title": "Geo-Spatial Insights into Urban Sprawl and Land Use Transformation: A GIS-Based Case Study of Narsinghgarh, Madhya Pradesh",
            "authors": "Nitesh Bhargava, Kamal Kushwaha, Manohar Pawar",
            "volume": "1",
            "issue": "1",
            "year": 2025,
            "abstract": "Urban sprawls are locations where the lines separating rural and urban areas are crossed. Urban sprawl is caused by a variety of factors, such as population expansion, socioeconomic situations, technological improvements, and development rules. In India, the rapid expansion of cities and towns due to urbanization and population growth has raised serious concerns about urban sprawl. Because urban sprawl has resulted from unplanned and uncontrolled growth, having its boundaries indefinitely is seen as a serious issue. To address these issues, plans for resolving uncertainties in urban sprawl should be put in place. In this sense, rapid data generation and the identification of urban sprawl boundaries would be aided by Geographic Information Systems (GIS). The objective of this study is to monitor the land cover and land use of a portion of Narsinghgarh city and urban sprawl over two time periods, from 2005 to 2015, to detect changes and evaluate urban sprawl using topographic sheets and Google map data in a GIS environment for better decision-making and sustainable urban growth. The investigation reveals that land use and land cover changes, as well as trends in urban spatial growth, may be accurately and thoroughly assessed using remote sensing and GIS approaches. The results demonstrate that while urban sprawl cannot be totally avoided, its effects can be considerably lessened with the use of sustainable and structured planning frameworks.",
            "pdf_filename": "feri/Bhargava_etal_2025_FERI_Paper_ID_06.pdf",
            "citation": "Bhargava N., Kushwaha K., Pawar M. 2025. Geo-Spatial Insights into Urban Sprawl and Land Use Transformation: A GIS-Based Case Study of Narsinghgarh, Madhya Pradesh. Frontiers in Environmental Revolutionary Innovation, 1(2), 58–73.",
            "image_filename": "default_paper_bg.jpg",
            "journal_id": "004",
            "is_archive": True
        },
        {
            "main_heading": "Healthcare Research",
            "sub_heading": "Effectiveness of Structured Teaching on Catheter-Associated Urinary Tract Infection (CAUTI) Prevention among Nurses at NMCH",
            "title": "Effectiveness of Structured Teaching on Catheter-Associated Urinary Tract Infection (CAUTI) Prevention among Nurses at NMCH",
            "authors": "Krishna Kant, Raju Kumar, Vivek Tiwari, Rajlaxmi Kumari, Shivanand Gupta, Sajjan Patel, K. Latha",
            "volume": "1",
            "issue": "2",
            "year": 2025,
            "abstract": "Catheter-Associated Urinary Tract Infection (CAUTI) is one of the most prevalent and preventable healthcare-associated infections (HAIs), posing a serious challenge to patient safety worldwide. Urinary tract infections (UTIs) linked to indwelling catheter use account for approximately 40% of all hospital-acquired infections. The risk of developing CAUTI increases significantly with the duration of catheterization, improper insertion techniques, lack of hand hygiene, and non-compliance with catheter care protocols. This study aimed to assess the effectiveness of a structured teaching program on CAUTI prevention among staff nurses at NMCH. The research approach was descriptive, using a one-group design with 60 staff nurses who provide care to indwelling catheter patients. Data was collected through surveys and analyzed with descriptive and inferential statistics. Results showed significant improvement in knowledge levels: pre-test results indicated 37% had poor knowledge, 50% had fair knowledge, and only 13.3% had good knowledge. After the structured teaching program, only 10% had poor knowledge, 20% had fair knowledge, and 70% demonstrated good knowledge. The overall mean knowledge score improved to 82.73% with an SD of 5.10%. The study concludes that structured teaching programs significantly enhance nurses' knowledge and awareness of CAUTI prevention, emphasizing the importance of hand hygiene, aseptic catheter insertion, and strict compliance with care protocols. Continuous education and training interventions are essential to strengthen infection control practices and minimize healthcare-associated infections in clinical settings.",
            "pdf_filename": "fhima/Kant_etal_2025FHIMA_PaperID_001.pdf",
            "citation": "Kant K., Kumar R., Tiwari V., Kumari R., Gupta S., Patel S., Latha K. 2025. Effectiveness of Structured Teaching on Catheter-Associated Urinary Tract Infection (CAUTI) Prevention among Nurses at NMCH. Frontiers of Health Innovations and Medical Advances, 1(2), 1–6. https://doi.org/10.1000/002",
            "image_filename": "default_paper_bg.jpg",
            "journal_id": "005",
            "is_archive": True
        },
        {
            "main_heading": "Maternal Health Research",
            "sub_heading": "A Study to Assess the Knowledge Regarding Respectful Maternity Care Among The Midwives at NMCH, Jamuhar",
            "title": "A Study to Assess the Knowledge Regarding Respectful Maternity Care Among The Midwives at NMCH, Jamuhar",
            "authors": "Aditya Kumar, Abhishek Kumar Satyam, Kritika Singh, Khushboo Kumari, Vivek Raj, Ruchi Tripathi, K. Latha",
            "volume": "1",
            "issue": "2",
            "year": 2025,
            "abstract": "Maternal health has undergone a significant shift in recent years, not only in terms of reducing mortality and morbidity but also in emphasizing the quality of care and human rights during pregnancy, childbirth, and the postpartum period. Respectful Maternity Care (RMC) is a global priority aimed at eliminating disrespect and abuse during maternity services. According to the World Health Organization (WHO, 2023), every woman has the right to dignified, respectful healthcare throughout pregnancy and childbirth. This study aimed to assess the knowledge regarding Respectful Maternity Care among nursing midwives at NMCH, Jamuhar, Bihar. A descriptive research design and random sampling technique were used to select 60 nursing midwives. Data was collected using a structured questionnaire consisting of 30 items across six domains: general knowledge, awareness of rights, communication, professional practices, behavior and attitude, and challenges and solutions. The study revealed that the majority of nursing midwives had adequate knowledge regarding Respectful Maternity Care, especially in the areas of general knowledge (87.3%), communication (81.0%), and professional practices (85.7%). However, knowledge was relatively low in the domain of challenges and solutions (75.7%). Among the demographic variables, only educational qualification showed a statistically significant association with knowledge level, while age, gender, and years of experience did not. The findings highlight the importance of focused training and supportive policies for effective implementation of respectful maternity practices. Strengthening midwives' capacity in RMC not only enhances maternal outcomes but also upholds the fundamental rights of women during childbirth, fostering trust and confidence in healthcare systems.",
            "pdf_filename": "fhima/Kumar_etal_2025_FHIMA_PaperID_002.pdf",
            "citation": "Kumar A., Satyam A.K., Singh K., Kumari K., Tripathi R., Latha K. 2025. A study to assess the knowledge regarding Respectful maternity care among The Midwives at NMCH, Jamuhar. Frontiers of Health Innovations and Medical Advances (FHIMA), 1(2), 7–12. https://doi.org/10.1000/001",
            "image_filename": "default_paper_bg.jpg",
            "journal_id": "005",
            "is_archive": True
        },
        {
            "main_heading": "Medical Data Science Research",
            "sub_heading": "Data Intelligence Tools in Diabetes Mellitus: Applications, Methods, and Future Directions",
            "title": "Data Intelligence Tools in Diabetes Mellitus: Applications, Methods, and Future Directions",
            "authors": "Kailash Prasad Jaiswal",
            "volume": "1",
            "issue": "1",
            "year": 2025,
            "abstract": "Diabetes mellitus (DM) is a heterogeneous metabolic disorder characterized by chronic hyperglycemia resulting from defects in insulin secretion, insulin action, or both. Globally, the prevalence and economic burden of DM continue to rise, necessitating new approaches for prevention, diagnosis, clinical management, and health‐system planning. Data intelligence (DI)—the integrated use of data engineering, analytics, machine learning (ML), and artificial intelligence (AI) within robust socio-technical systems—has emerged as a transformative enabler across the diabetes continuum of care. We synthesize evidence on key application domains, highlight clinical and operational outcomes reported to date, and analyze barriers related to data quality, algorithmic bias, privacy, interoperability, and real-world implementation. We propose a pragmatic evaluation framework and a research roadmap focused on explainability, causal inference, hybrid mechanistic–ML models, and equitable deployment at scale.",
            "pdf_filename": "fhima/Jaiswal_et_al_2025FHIMAPaperID_003.pdf",
            "citation": "Jaiswal K.P. 2025. Data Intelligence Tools in Diabetes Mellitus: Applications, Methods, and Future Directions. Curevita Innovation of BioData Intelligence, 1(1), 13–23.",
            "image_filename": "default_paper_bg.jpg",
            "journal_id": "005",
            "is_archive": True
        },
        {
            "main_heading": "Pharmaceutical AI Research",
            "sub_heading": "Comprehensive Review on the Role of Artificial Intelligence (AI) in Drug Discovery and Drug Development",
            "title": "Comprehensive Review on the Role of Artificial Intelligence (AI) in Drug Discovery and Drug Development",
            "authors": "Zahoor Ahmad Malik, Jitendra Bajaj, Neha Shukla",
            "volume": "1",
            "issue": "1",
            "year": 2025,
            "abstract": "Artificial Intelligence or AI, has become a potent technology that might change the way healthcare works, from medicine delivery to drug discovery. This paper looks at how AI is already being used and will be used in the future in the pharmaceutical business, with an emphasis on medication delivery and research. It talks about a lot of different things, such as smart drug delivery networks, sensors, drug repurposing, statistical modeling, and simulating biological and biotechnological systems. It also looks at how The review talks about how AI may be used in medication formulation and distribution, clinical trials, drug safety, and pharmacovigilance. It talks about the rules and problems that come up when using AI in the pharmaceutical industry, such as privacy, data security, and how easy it is to understand AI models. The study continues with a look at the future, pointing out new trends, talking about the flaws and biases in AI models, and stressing how important it is to work together and share information. It gives a full picture of how AI might change the pharmaceutical sector and make patient care better, as well as areas where further research and development is needed.",
            "pdf_filename": "fhima/Malik_etal_1_2_2025_FHIMA_paperID_04.pdf",
            "citation": "Malik Z.A., Bajaj J., Shukla N. 2025. A Comprehensive Review on the role of Artificial Intelligence (AI) in drug discovery and drug development. Frontiers of Health Innovations and Medical Advances, 1(2), 24–54.",
            "image_filename": "default_paper_bg.jpg",
            "journal_id": "005",
            "is_archive": True
        },
        {
            "main_heading": "Healthcare Management Research",
            "sub_heading": "The Role of Data Science in Hospital Management",
            "title": "The Role of Data Science in Hospital Management",
            "authors": "Sajjan Singh Patel, Ruchi Tripathi",
            "volume": "1",
            "issue": "2",
            "year": 2025,
            "abstract": "The integration of data science into hospital management is transforming healthcare systems by improving patient outcomes, optimizing resource allocation, and enhancing operational efficiency. Hospitals face growing challenges due to increasing patient volumes, rising costs, and the demand for personalized care. Traditional management approaches often fall short in handling the complexity of modern healthcare systems. Data science, leveraging machine learning, artificial intelligence (AI), big data analytics, and advanced statistical methods, provides powerful tools to enhance hospital operations and deliver high-quality care. This paper examines the impact of data science in hospital management, exploring its applications across multiple domains including patient care optimization, operational efficiency, predictive analytics, financial management, and resource allocation. In patient care optimization, data science enables personalized medicine and early disease detection through predictive analytics. Machine learning algorithms analyze electronic health records (EHRs), medical imaging, and laboratory data to predict patient outcomes, optimize treatment plans, and improve care quality. For operational efficiency, data science tools help optimize staffing, streamline workflows, reduce wait times, and enhance patient flow management through real-time analytics that enable effective decision-making and reduce operational bottlenecks. The study also highlights challenges in implementing data science, including data security and patient privacy concerns that must be safeguarded through strict compliance with healthcare regulations such as HIPAA and GDPR. Additional barriers include integration of data across siloed hospital departments, lack of skilled data professionals, and high infrastructure costs. The paper concludes by discussing future directions, including greater use of AI-driven decision support systems, Internet of Things (IoT)-enabled patient monitoring, and telemedicine analytics.",
            "pdf_filename": "fhima/Patel_Tripathi_2025_FHIMA_PaperID_05.pdf",
            "citation": "Patel S.S., Tripathi R. 2025. The Role of Data Science in Hospital Management. Frontiers of Health Innovations and Medical Advances (FHIMA), 1(2), 55–58.",
            "image_filename": "default_paper_bg.jpg",
            "journal_id": "005",
            "is_archive": True
        }

    ]

    total_inserted = 0
    total_skipped = 0
    journal_not_found = 0

    print("Starting ResearchPaper data insertion...\n")

    for paper_data in research_papers_data:
        # Check if journal exists
        journal = JournalMaster.query.filter_by(journal_id=paper_data["journal_id"]).first()
        
        if not journal:
            print(f"Journal with ID {paper_data['journal_id']} not found — skipping paper: {paper_data['title'][:60]}...")
            journal_not_found += 1
            continue
        
        # Duplicate check based on title and journal_id
        existing_paper = ResearchPaper.query.filter_by(title=paper_data["title"], journal_id=journal.journal_id).first()
        
        if existing_paper:
            print(f"Research paper '{paper_data['title'][:50]}...' already exists — skipping insert.")
            total_skipped += 1
        else:
            try:
                # Assign journal object/reference if needed
                paper_data["journal"] = journal

                # Create new ResearchPaper entry
                new_paper = ResearchPaper(**paper_data)
                db.session.add(new_paper)
                db.session.commit()
                total_inserted += 1
                print(f"Added successfully: {paper_data['title'][:60]}...")
            except Exception as e:
                db.session.rollback()
                print(f"Error inserting paper '{paper_data['title'][:50]}...': {str(e)}")

    # Final summary
    print("\nResearchPaper Insertion Summary:")
    print(f"Successfully inserted: {total_inserted} papers")
    print(f"Skipped (duplicates): {total_skipped} papers")
    print(f"Journals not found: {journal_not_found} papers")

    # Verification - database ke saare papers list karein
    all_papers = ResearchPaper.query.all()
    print(f"\nTotal research papers in database: {len(all_papers)}")

    if all_papers:
        print("\nResearch Papers List:")
        for paper in all_papers:
            print(f"→ ID {paper.id}: {paper.title[:50]}... | Journal ID: {paper.journal_id}")
    else:
        print("No research papers found in database.")

    print("\nResearchPaper data insertion completed!")
