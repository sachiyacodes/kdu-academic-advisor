"""
Build full official KDU Computing curricula for all 6 degree programmes:
1. BSc (Hons) in Information Technology
2. BSc (Hons) in Software Engineering
3. BSc (Hons) in Computer Science
4. BSc (Hons) in Data Science & Business Analytics
5. BSc (Hons) in Information Systems
6. BSc (Hons) in Computer Engineering
"""
import csv
from pathlib import Path

import sys
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
DATA_DIR = PROJECT_ROOT / "data"

DEGREES = [
    (1, "Information Technology"),
    (2, "Software Engineering"),
    (3, "Computer Science"),
    (4, "Data Science & Business Analytics"),
    (5, "Information Systems"),
    (6, "Computer Engineering"),
    (7, "Custom / Other University Degree"),
]

# Raw audited course data: (Degree Name, [(Semester 1..8, Course Name, Credits, Subject Area, Prereq course names)])
RAW_CURRICULA = {
    "Computer Science": [
        # Sem 1 (Y1S1)
        (1, 1, "Fundamentals of Programming", 2, "Programming", []),
        (1, 1, "Programming Laboratory", 1, "Programming", []),
        (1, 1, "Foundation of Computer Science", 2, "Other", []),
        (1, 1, "Fundamentals of Databases", 2, "Database", []),
        (1, 1, "Software Development Methodologies", 2, "Software Engineering", []),
        (1, 1, "Computer Systems Architecture", 3, "Systems & Operating Systems", []),
        (1, 1, "Probability and Statistics", 3, "Statistics", []),
        (1, 1, "Mathematics for Computing", 2, "Mathematics", []),
        (1, 1, "Collaborative Hardware Project", 1, "Systems & Operating Systems", []),
        (1, 1, "English: Basic Study Skills for CS/SE/CE", 2, "Other", []),
        (1, 1, "Leadership Training", 2, "Other", []),
        # Sem 2 (Y1S2)
        (1, 2, "Web Development", 2, "Other", []),
        (1, 2, "Object Oriented Programming", 3, "Programming", ["Fundamentals of Programming"]),
        (1, 2, "Computer Networks", 3, "Networking", []),
        (1, 2, "Creative Media Tools", 1, "Other", []),
        (1, 2, "Software Analysis and Modeling", 2, "Software Engineering", ["Software Development Methodologies"]),
        (1, 2, "Discrete Mathematics", 2, "Mathematics", ["Mathematics for Computing"]),
        (1, 2, "Fundamentals of Electronics", 1, "Systems & Operating Systems", ["Computer Systems Architecture"]),
        (1, 2, "Collaborative Hardware Project", 1, "Systems & Operating Systems", ["Collaborative Hardware Project"]),
        (1, 2, "English: Advance Study Skills for CS/SE/CE", 2, "Other", []),
        # Sem 3 (Y2S1)
        (2, 1, "Operating Systems", 2, "Systems & Operating Systems", ["Computer Systems Architecture"]),
        (2, 1, "Data Structures and Algorithms", 2, "Algorithms & Data Structures", ["Object Oriented Programming"]),
        (2, 1, "Advanced Object Oriented Programming", 2, "Programming", ["Object Oriented Programming"]),
        (2, 1, "Advanced Computer Networks and Wireless Communication", 2, "Networking", ["Computer Networks"]),
        (2, 1, "Advanced Web Development", 2, "Other", ["Web Development"]),
        (2, 1, "Group Project in Software Development", 1, "Software Engineering", ["Software Analysis and Modeling"]),
        (2, 1, "Requirements Engineering", 2, "Software Engineering", ["Software Analysis and Modeling"]),
        (2, 1, "Statistical Distributions and Inference", 2, "Statistics", ["Probability and Statistics"]),
        (2, 1, "Calculus", 2, "Mathematics", ["Mathematics for Computing"]),
        (2, 1, "Principles of Management", 2, "Other", []),
        (2, 1, "Writing and Speaking Skills", 2, "Other", []),
        # Sem 4 (Y2S2)
        (2, 2, "Advanced Data Structures and Algorithms", 2, "Algorithms & Data Structures", ["Data Structures and Algorithms"]),
        (2, 2, "Artificial Intelligence", 3, "Artificial Intelligence", ["Data Structures and Algorithms", "Probability and Statistics"]),
        (2, 2, "Group Project in Software Development", 2, "Software Engineering", ["Group Project in Software Development"]),
        (2, 2, "Software Project Management", 3, "Software Engineering", ["Requirements Engineering"]),
        (2, 2, "Software Architecture", 2, "Software Engineering", ["Requirements Engineering"]),
        (2, 2, "Computer Interfacing and Microprocessors", 2, "Systems & Operating Systems", ["Operating Systems"]),
        (2, 2, "Numerical Methods", 2, "Mathematics", ["Calculus"]),
        (2, 2, "Research Writing Skills", 2, "Other", []),
        # Sem 5 (Y3S1)
        (3, 1, "Essentials of Computer Law", 2, "Other", []),
        (3, 1, "Research Methodology", 2, "Other", []),
        (3, 1, "Mobile Computing", 2, "Other", ["Advanced Object Oriented Programming"]),
        (3, 1, "Computer and Network Security", 2, "Cyber Security", ["Advanced Computer Networks and Wireless Communication"]),
        (3, 1, "Bioinformatics", 2, "Other", []),
        (3, 1, "UX and UI Engineering", 2, "Software Engineering", ["Advanced Web Development"]),
        (3, 1, "Advanced Database Techniques", 2, "Database", ["Fundamentals of Databases"]),
        (3, 1, "Distributed Computing", 2, "Cloud Computing", ["Operating Systems", "Advanced Computer Networks and Wireless Communication"]),
        (3, 1, "Digital Image Processing", 2, "Artificial Intelligence", ["Mathematics for Computing"]),
        (3, 1, "Expert Systems and Logic Programming", 2, "Artificial Intelligence", ["Artificial Intelligence"]),
        (3, 1, "Cloud Computing", 2, "Cloud Computing", ["Distributed Computing"]),
        (3, 1, "Data Mining and Business Intelligence", 2, "Data Analysis", ["Fundamentals of Databases", "Probability and Statistics"]),
        (3, 1, "Big Data Analytics", 2, "Data Analysis", ["Fundamentals of Databases"]),
        (3, 1, "Enterprise System Administration", 2, "Systems & Operating Systems", ["Operating Systems"]),
        # Sem 6 (Y3S2)
        (3, 2, "Computer Graphics and Visualization", 2, "Other", ["Calculus"]),
        (3, 2, "Automata Theory", 2, "Algorithms & Data Structures", ["Discrete Mathematics"]),
        (3, 2, "Complex Systems and Agent Technology", 2, "Artificial Intelligence", ["Artificial Intelligence"]),
        (3, 2, "Information Security", 2, "Cyber Security", ["Computer and Network Security"]),
        (3, 2, "Modeling and Simulation", 2, "Mathematics", ["Calculus", "Statistical Distributions and Inference"]),
        (3, 2, "Nature Inspired Computing", 2, "Artificial Intelligence", ["Artificial Intelligence"]),
        (3, 2, "Internet of Things", 2, "Systems & Operating Systems", ["Computer Interfacing and Microprocessors"]),
        (3, 2, "Natural Language Processing", 2, "Artificial Intelligence", ["Artificial Intelligence"]),
        (3, 2, "Machine Learning", 2, "Artificial Intelligence", ["Artificial Intelligence", "Statistical Distributions and Inference"]),
        (3, 2, "Distributed Systems", 2, "Cloud Computing", ["Distributed Computing"]),
        (3, 2, "Advanced Mobile Computing", 2, "Other", ["Mobile Computing"]),
        (3, 2, "Independent Research Study", 2, "Other", ["Research Methodology"]),
        (3, 2, "Operational Research", 3, "Statistics", ["Statistical Distributions and Inference"]),
        (3, 2, "Statistical Tools for Computing", 1, "Statistics", ["Probability and Statistics"]),
        (3, 2, "Microcontrollers and Embedded Systems", 2, "Systems & Operating Systems", ["Computer Interfacing and Microprocessors"]),
        (3, 2, "Geoinformatics", 2, "Other", []),
        # Sem 7 (Y4S1)
        (4, 1, "Emerging Trends in Computing", 2, "Other", []),
        (4, 1, "Theory of Programming Languages", 2, "Algorithms & Data Structures", ["Automata Theory"]),
        (4, 1, "Artificial Cognitive Systems", 2, "Artificial Intelligence", ["Artificial Intelligence"]),
        (4, 1, "Computability and Complexity", 2, "Algorithms & Data Structures", ["Automata Theory"]),
        (4, 1, "Semantic Web and Ontology", 2, "Database", ["Fundamentals of Databases"]),
        (4, 1, "Computer Music", 2, "Other", []),
        (4, 1, "High Performance Computing", 2, "Cloud Computing", ["Distributed Computing"]),
        (4, 1, "Social Aspects and Professional Practices", 2, "Other", []),
        (4, 1, "Digital Forensics", 2, "Cyber Security", ["Information Security"]),
        (4, 1, "Cyber Security", 2, "Cyber Security", ["Information Security"]),
        (4, 1, "Deep Learning", 2, "Artificial Intelligence", ["Machine Learning"]),
        (4, 1, "Location Based Services", 2, "Other", []),
        (4, 1, "Interactive Media and Game Development", 2, "Other", ["Computer Graphics and Visualization"]),
        (4, 1, "Individual Research Project", 2, "Other", ["Independent Research Study"]),
        (4, 1, "Formal Methods and Software Verification", 2, "Software Engineering", ["Software Architecture"]),
        (4, 1, "Software Quality Assurance", 2, "Software Engineering", ["Software Architecture"]),
        (4, 1, "Advanced Operating Systems", 2, "Systems & Operating Systems", ["Operating Systems"]),
        (4, 1, "Robotics and Automation", 2, "Artificial Intelligence", ["Computer Interfacing and Microprocessors"]),
        (4, 1, "Entrepreneurship and Business Management", 2, "Other", []),
        # Sem 8 (Y4S2)
        (4, 2, "Individual Research Project", 7, "Other", ["Individual Research Project"]),
        (4, 2, "Industrial Training", 6, "Other", []),
    ],

    "Software Engineering": [
        # Sem 1 (Y1S1)
        (1, 1, "Fundamentals of Programming", 2, "Programming", []),
        (1, 1, "Programming Laboratory", 1, "Programming", []),
        (1, 1, "Foundation of Computer Science", 2, "Other", []),
        (1, 1, "Computer Systems Architecture", 2, "Systems & Operating Systems", []),
        (1, 1, "Fundamentals of Databases", 3, "Database", []),
        (1, 1, "Fundamentals of Visual Computing", 2, "Other", []),
        (1, 1, "Probability and Statistics", 3, "Statistics", []),
        (1, 1, "Engineering Mathematics", 2, "Mathematics", []),
        (1, 1, "English: Basic Study Skills for CS/SE/CE", 2, "Other", []),
        (1, 1, "Leadership Training", 2, "Other", []),
        # Sem 2 (Y1S2)
        (1, 2, "Developments in Mathematics and Sciences", 2, "Mathematics", ["Engineering Mathematics"]),
        (1, 2, "Object Oriented Programming I", 3, "Programming", ["Fundamentals of Programming"]),
        (1, 2, "Web Development", 2, "Other", []),
        (1, 2, "Computer Networks I", 2, "Networking", []),
        (1, 2, "Discrete Mathematics", 2, "Mathematics", ["Engineering Mathematics"]),
        (1, 2, "Group Project in Hardware", 3, "Systems & Operating Systems", ["Computer Systems Architecture"]),
        (1, 2, "Fundamentals of Electrical Engineering", 2, "Systems & Operating Systems", []),
        (1, 2, "Basic Electronics", 2, "Systems & Operating Systems", []),
        (1, 2, "English: Advanced Study Skills for CS/SE/CE", 2, "Other", []),
        # Sem 3 (Y2S1)
        (2, 1, "Data Structures and Algorithms I", 3, "Algorithms & Data Structures", ["Object Oriented Programming I"]),
        (2, 1, "Operating Systems", 2, "Systems & Operating Systems", ["Computer Systems Architecture"]),
        (2, 1, "Object Oriented Programming II", 2, "Programming", ["Object Oriented Programming I"]),
        (2, 1, "Computer Networks II", 2, "Networking", ["Computer Networks I"]),
        (2, 1, "Requirements Engineering", 2, "Software Engineering", []),
        (2, 1, "Electronics Systems", 2, "Systems & Operating Systems", ["Basic Electronics"]),
        (2, 1, "Calculus and Numerical Methods", 3, "Mathematics", ["Engineering Mathematics"]),
        (2, 1, "Principles of Management", 3, "Other", []),
        (2, 1, "Writing and Speaking Skills", 0, "Other", []),
        # Sem 4 (Y2S2)
        (2, 2, "Data Structures and Algorithms II", 2, "Algorithms & Data Structures", ["Data Structures and Algorithms I"]),
        (2, 2, "Advanced Computer Architecture and Organization", 2, "Systems & Operating Systems", ["Computer Systems Architecture"]),
        (2, 2, "Artificial Intelligence", 2, "Artificial Intelligence", ["Data Structures and Algorithms I"]),
        (2, 2, "Software Project Management", 3, "Software Engineering", ["Requirements Engineering"]),
        (2, 2, "Software Process Engineering", 2, "Software Engineering", ["Requirements Engineering"]),
        (2, 2, "Statistical Distributions and Inference", 2, "Statistics", ["Probability and Statistics"]),
        (2, 2, "Computer Interfacing and Microprocessors", 2, "Systems & Operating Systems", ["Operating Systems"]),
        (2, 2, "Group Project in Software Development", 3, "Software Engineering", ["Object Oriented Programming II", "Requirements Engineering"]),
        (2, 2, "Research Writing Skills", 0, "Other", []),
        # Sem 5 (Y3S1)
        (3, 1, "Engineering Foundation for Software", 2, "Software Engineering", []),
        (3, 1, "Software Modeling", 2, "Software Engineering", ["Requirements Engineering"]),
        (3, 1, "Software Construction Technologies and Tools", 2, "Software Engineering", ["Object Oriented Programming II"]),
        (3, 1, "Software Design and Architecture", 2, "Software Engineering", ["Software Modeling"]),
        (3, 1, "Human Computer Interaction", 2, "Software Engineering", ["Web Development"]),
        (3, 1, "Essentials of Computer Law", 2, "Other", []),
        (3, 1, "Advanced Database and Big Data Analytics", 3, "Database", ["Fundamentals of Databases"]),
        (3, 1, "Computer & Network Security", 2, "Cyber Security", ["Computer Networks II"]),
        (3, 1, "Image Processing & Computer Vision", 2, "Artificial Intelligence", ["Engineering Mathematics"]),
        (3, 1, "Research Methodology", 2, "Other", []),
        (3, 1, "Logic Programming", 2, "Artificial Intelligence", ["Artificial Intelligence"]),
        (3, 1, "Mobile Computing", 2, "Other", ["Object Oriented Programming II"]),
        # Sem 6 (Y3S2)
        (3, 2, "Engineering Economics for Software", 2, "Other", []),
        (3, 2, "Software Verification and Validation", 2, "Software Engineering", ["Software Design and Architecture"]),
        (3, 2, "Software Process", 2, "Software Engineering", ["Software Process Engineering"]),
        (3, 2, "Social Aspects of Computing", 2, "Other", []),
        (3, 2, "Independent Study", 2, "Other", ["Research Methodology"]),
        (3, 2, "Digital Forensic", 2, "Cyber Security", ["Computer & Network Security"]),
        (3, 2, "Computer Graphics & Visualization", 2, "Other", ["Calculus and Numerical Methods"]),
        (3, 2, "Automata Theory", 2, "Algorithms & Data Structures", ["Discrete Mathematics"]),
        (3, 2, "Information Security", 2, "Cyber Security", ["Computer & Network Security"]),
        (3, 2, "High Performance Computing", 2, "Cloud Computing", ["Operating Systems"]),
        (3, 2, "Complex Systems and Agent Technology", 2, "Artificial Intelligence", ["Artificial Intelligence"]),
        # Sem 7 (Y4S1)
        (4, 1, "Formal Methods and Software Verification", 2, "Software Engineering", ["Software Verification and Validation"]),
        (4, 1, "Software Evolution", 2, "Software Engineering", ["Software Process"]),
        (4, 1, "Software Quality", 2, "Software Engineering", ["Software Verification and Validation"]),
        (4, 1, "Emerging Trends in Computing", 2, "Other", []),
        (4, 1, "Theory of Programming Languages", 2, "Algorithms & Data Structures", ["Automata Theory"]),
        (4, 1, "Natural Language Processing", 2, "Artificial Intelligence", ["Artificial Intelligence"]),
        (4, 1, "Artificial Cognitive Systems", 2, "Artificial Intelligence", ["Artificial Intelligence"]),
        (4, 1, "Compilers Design", 2, "Algorithms & Data Structures", ["Automata Theory"]),
        (4, 1, "Semantic Web and Ontology", 2, "Database", ["Fundamentals of Databases"]),
        (4, 1, "Distributed Systems", 2, "Cloud Computing", ["Computer Networks II"]),
        (4, 1, "Advanced Topics in Statistics", 2, "Statistics", ["Statistical Distributions and Inference"]),
        (4, 1, "Individual Research Project", 4, "Other", ["Independent Study"]),
        # Sem 8 (Y4S2)
        (4, 2, "Individual Research Project", 9, "Other", ["Individual Research Project"]),
        (4, 2, "Industrial Training", 6, "Other", []),
    ],

    "Data Science & Business Analytics": [
        # Sem 1 (Y1S1)
        (1, 1, "Fundamentals of Data Science", 1, "Data Analysis", []),
        (1, 1, "Probability and Statistics", 3, "Statistics", []),
        (1, 1, "Calculus I", 2, "Mathematics", []),
        (1, 1, "Fundamentals of Programming", 2, "Programming", []),
        (1, 1, "Programming Laboratory", 1, "Programming", []),
        (1, 1, "Fundamentals of Databases", 2, "Database", []),
        (1, 1, "Principles of Management", 2, "Other", []),
        (1, 1, "Introduction to Communication Skills", 3, "Other", []),
        # Sem 2 (Y1S2)
        (1, 2, "Discrete Mathematics for Data Science", 3, "Mathematics", ["Calculus I"]),
        (1, 2, "Linear Algebra I", 2, "Mathematics", ["Calculus I"]),
        (1, 2, "Statistical Inference", 3, "Statistics", ["Probability and Statistics"]),
        (1, 2, "Object Oriented Programming", 2, "Programming", ["Fundamentals of Programming"]),
        (1, 2, "Applied Statistical Computing", 2, "Statistics", ["Probability and Statistics"]),
        (1, 2, "Business Economics", 2, "Other", []),
        (1, 2, "Fundamentals of Business Communication", 3, "Other", []),
        # Sem 3 (Y2S1)
        (2, 1, "Calculus II", 2, "Mathematics", ["Calculus I"]),
        (2, 1, "Linear Algebra II", 2, "Mathematics", ["Linear Algebra I"]),
        (2, 1, "Regression Analysis", 3, "Statistics", ["Statistical Inference"]),
        (2, 1, "Data Structures and Algorithms", 3, "Algorithms & Data Structures", ["Object Oriented Programming"]),
        (2, 1, "Programming for Data Science", 2, "Programming", ["Object Oriented Programming"]),
        (2, 1, "Accounting and Finance", 3, "Other", []),
        (2, 1, "Advanced Communication Skills", 3, "Other", []),
        # Sem 4 (Y2S2)
        (2, 2, "Categorical Data Analysis", 2, "Data Analysis", ["Regression Analysis"]),
        (2, 2, "Essentials of Artificial Intelligence", 2, "Artificial Intelligence", ["Programming for Data Science"]),
        (2, 2, "Data Mining and Data Warehousing", 3, "Data Analysis", ["Fundamentals of Databases"]),
        (2, 2, "Software Engineering", 3, "Software Engineering", ["Object Oriented Programming"]),
        (2, 2, "Cost & Management Accounting", 2, "Other", ["Accounting and Finance"]),
        (2, 2, "Business Intelligence and Analytics", 2, "Data Analysis", ["Fundamentals of Data Science"]),
        (2, 2, "Conversation Analysis", 3, "Other", []),
        # Sem 5 (Y3S1)
        (3, 1, "Advanced Database Management Systems", 2, "Database", ["Fundamentals of Databases"]),
        (3, 1, "Machine Learning", 3, "Artificial Intelligence", ["Essentials of Artificial Intelligence", "Linear Algebra II"]),
        (3, 1, "Multivariate Data Analysis", 2, "Data Analysis", ["Regression Analysis"]),
        (3, 1, "Computer Networks", 2, "Networking", []),
        (3, 1, "Research Methodology", 3, "Other", []),
        (3, 1, "Bayesian Data Analysis", 2, "Statistics", ["Statistical Inference"]),
        (3, 1, "Professional Practices and IT Law", 2, "Other", []),
        (3, 1, "Operations Research", 3, "Statistics", ["Linear Algebra II"]),
        (3, 1, "Group Project in Applied Data Analytics", 0, "Data Analysis", ["Programming for Data Science"]),
        # Sem 6 (Y3S2)
        (3, 2, "Big Data Analytics", 3, "Data Analysis", ["Data Mining and Data Warehousing"]),
        (3, 2, "Time Series Analysis", 3, "Statistics", ["Regression Analysis"]),
        (3, 2, "Group Project in Applied Data Analytics", 3, "Data Analysis", ["Group Project in Applied Data Analytics"]),
        (3, 2, "Operation Management", 2, "Other", []),
        (3, 2, "Cloud Computing", 2, "Cloud Computing", ["Computer Networks"]),
        (3, 2, "Cyber Security", 2, "Cyber Security", ["Computer Networks"]),
        (3, 2, "Deep Learning", 3, "Artificial Intelligence", ["Machine Learning"]),
        (3, 2, "Discourse Communication", 3, "Other", []),
        # Sem 7 (Y4S1)
        (4, 1, "Image Processing and Computer Vision", 2, "Artificial Intelligence", ["Linear Algebra II"]),
        (4, 1, "Data Management and Governance", 2, "Database", ["Advanced Database Management Systems"]),
        (4, 1, "Project Management for Data Science", 2, "Other", []),
        (4, 1, "Natural Language Processing", 2, "Artificial Intelligence", ["Machine Learning"]),
        (4, 1, "Semantic Web and Ontology", 2, "Database", ["Fundamentals of Databases"]),
        (4, 1, "Spatial Data Analysis", 2, "Data Analysis", ["Regression Analysis"]),
        (4, 1, "Emerging Trends in Data Science", 2, "Data Analysis", []),
        (4, 1, "Parallel Computing", 2, "Cloud Computing", ["Computer Networks"]),
        (4, 1, "Information Security", 2, "Cyber Security", ["Cyber Security"]),
        (4, 1, "Strategic Business Analysis", 2, "Data Analysis", ["Business Intelligence and Analytics"]),
        (4, 1, "Individual Research Project", 0, "Other", ["Research Methodology"]),
        # Sem 8 (Y4S2)
        (4, 2, "Individual Research Project", 9, "Other", ["Individual Research Project"]),
        (4, 2, "Industrial Training", 6, "Other", []),
    ],

    "Information Technology": [
        # Sem 1 (Y1S1)
        (1, 1, "Information Technology Concepts", 2, "Other", []),
        (1, 1, "Fundamentals of Computer Programming", 2, "Programming", []),
        (1, 1, "Computer Programming Laboratory", 1, "Programming", []),
        (1, 1, "Fundamentals of Computer Systems", 2, "Systems & Operating Systems", []),
        (1, 1, "Fundamentals of Multimedia Technologies", 2, "Other", []),
        (1, 1, "Mathematics for IT I", 3, "Mathematics", []),
        (1, 1, "Principles of Management", 2, "Other", []),
        (1, 1, "English Study Skills for ICT", 2, "Other", []),
        (1, 1, "Leadership Training", 2, "Other", []),
        # Sem 2 (Y1S2)
        (1, 2, "Object Oriented Designing", 2, "Software Engineering", ["Fundamentals of Computer Programming"]),
        (1, 2, "Object Oriented Programming", 3, "Programming", ["Fundamentals of Computer Programming"]),
        (1, 2, "Fundamentals of Database Management Systems", 3, "Database", []),
        (1, 2, "Computer Systems Architecture", 2, "Systems & Operating Systems", ["Fundamentals of Computer Systems"]),
        (1, 2, "Internet of Things Applications and Design", 2, "Systems & Operating Systems", ["Fundamentals of Computer Systems"]),
        (1, 2, "Computer Network Systems I", 2, "Networking", []),
        (1, 2, "Web Technologies", 2, "Other", []),
        (1, 2, "Basic Probability and Statistics", 2, "Statistics", ["Mathematics for IT I"]),
        (1, 2, "Presentation Skills for ICT", 2, "Other", []),
        # Sem 3 (Y2S1)
        (2, 1, "Rapid Application Development", 3, "Programming", ["Object Oriented Programming"]),
        (2, 1, "System Analysis and Design", 2, "Software Engineering", ["Object Oriented Designing"]),
        (2, 1, "UX and UI Engineering", 3, "Software Engineering", ["Web Technologies"]),
        (2, 1, "Advanced Database Management Systems", 3, "Database", ["Fundamentals of Database Management Systems"]),
        (2, 1, "Computer Network Systems II", 2, "Networking", ["Computer Network Systems I"]),
        (2, 1, "Industry based Software Engineering Project", 0, "Software Engineering", ["Object Oriented Programming"]),
        (2, 1, "Mathematics for IT II", 2, "Mathematics", ["Mathematics for IT I"]),
        (2, 1, "Human Resource Management", 2, "Other", []),
        (2, 1, "Writing and Speaking Skills", 2, "Other", []),
        # Sem 4 (Y2S2)
        (2, 2, "Data Structures and Algorithms", 3, "Algorithms & Data Structures", ["Object Oriented Programming"]),
        (2, 2, "Software Engineering", 2, "Software Engineering", ["System Analysis and Design"]),
        (2, 2, "Operating Systems", 2, "Systems & Operating Systems", ["Computer Systems Architecture"]),
        (2, 2, "Project Management", 2, "Other", []),
        (2, 2, "Research Methodology", 2, "Other", []),
        (2, 2, "Industry based Software Engineering Project", 2, "Software Engineering", ["Industry based Software Engineering Project"]),
        (2, 2, "Statistical Distributions and Inference", 2, "Statistics", ["Basic Probability and Statistics"]),
        (2, 2, "Research Writing Skills", 2, "Other", []),
        # Sem 5 (Y3S1)
        (3, 1, "Advanced Web Technologies", 3, "Other", ["Web Technologies"]),
        (3, 1, "Enterprise Application Development", 3, "Software Engineering", ["Rapid Application Development"]),
        (3, 1, "Advanced Multimedia Technologies", 2, "Other", ["Fundamentals of Multimedia Technologies"]),
        (3, 1, "Mobile Computing", 2, "Other", ["Object Oriented Programming"]),
        (3, 1, "Advanced Computer Network Systems I", 2, "Networking", ["Computer Network Systems II"]),
        (3, 1, "Information and Data Security", 2, "Cyber Security", ["Computer Network Systems II"]),
        (3, 1, "Computer Ethics and IT Law", 2, "Other", []),
        (3, 1, "Career Development Planning", 1, "Other", []),
        (3, 1, "Essentials of Artificial Intelligence", 3, "Artificial Intelligence", ["Data Structures and Algorithms"]),
        # Sem 6 (Y3S2)
        (3, 2, "Distributed Systems", 2, "Cloud Computing", ["Computer Network Systems II"]),
        (3, 2, "Software Quality Assurance", 2, "Software Engineering", ["Software Engineering"]),
        (3, 2, "Cyber Security", 3, "Cyber Security", ["Information and Data Security"]),
        (3, 2, "Cloud Computing and Virtualization", 3, "Cloud Computing", ["Computer Network Systems II"]),
        (3, 2, "Enterprise Resource Planning Systems", 2, "Other", ["Fundamentals of Database Management Systems"]),
        (3, 2, "Independent Research Study", 2, "Other", ["Research Methodology"]),
        (3, 2, "Machine Learning", 3, "Artificial Intelligence", ["Essentials of Artificial Intelligence"]),
        (3, 2, "Geoinformatics", 2, "Other", []),
        (3, 2, "Location Based Services", 2, "Other", []),
        (3, 2, "Entrepreneurship and Innovation", 2, "Other", []),
        # Sem 7 (Y4S1)
        (4, 1, "Data Mining and Data Warehousing", 3, "Data Analysis", ["Advanced Database Management Systems"]),
        (4, 1, "Data Analytics", 2, "Data Analysis", ["Basic Probability and Statistics"]),
        (4, 1, "Advanced Computer Network Systems II", 2, "Networking", ["Advanced Computer Network Systems I"]),
        (4, 1, "Database Administration", 3, "Database", ["Advanced Database Management Systems"]),
        (4, 1, "Deployment Engineering", 1, "Cloud Computing", ["Cloud Computing and Virtualization"]),
        (4, 1, "Semantic Web and Ontology", 2, "Database", ["Fundamentals of Database Management Systems"]),
        (4, 1, "Digital Image Processing", 2, "Artificial Intelligence", ["Mathematics for IT I"]),
        (4, 1, "Emerging Technologies in ICT", 2, "Other", []),
        (4, 1, "Interactive Media and Game Development", 2, "Other", []),
        (4, 1, "Blockchain Technologies", 2, "Cyber Security", ["Information and Data Security"]),
        (4, 1, "Social Aspects and Professional Practices", 2, "Other", []),
        (4, 1, "Natural Language Processing", 2, "Artificial Intelligence", ["Machine Learning"]),
        (4, 1, "Individual Research Project", 2, "Other", ["Independent Research Study"]),
        # Sem 8 (Y4S2)
        (4, 2, "Individual Research Project", 7, "Other", ["Individual Research Project"]),
        (4, 2, "Industrial Training", 6, "Other", []),
    ],

    "Information Systems": [
        # Sem 1 (Y1S1)
        (1, 1, "Information Technology Concepts", 2, "Other", []),
        (1, 1, "Fundamentals of Computer Programming", 2, "Programming", []),
        (1, 1, "Computer Programming Laboratory", 1, "Programming", []),
        (1, 1, "Fundamentals of Computer Systems", 2, "Systems & Operating Systems", []),
        (1, 1, "Fundamentals of Multimedia Technologies", 2, "Other", []),
        (1, 1, "Mathematics for IT I", 3, "Mathematics", []),
        (1, 1, "Principles of Management", 2, "Other", []),
        (1, 1, "English Study Skills for ICT", 2, "Other", []),
        (1, 1, "Leadership Training", 2, "Other", []),
        # Sem 2 (Y1S2)
        (1, 2, "Object Oriented Designing", 2, "Software Engineering", ["Fundamentals of Computer Programming"]),
        (1, 2, "Object Oriented Programming", 3, "Programming", ["Fundamentals of Computer Programming"]),
        (1, 2, "Fundamentals of Database Management Systems", 3, "Database", []),
        (1, 2, "Computer Systems Architecture", 2, "Systems & Operating Systems", ["Fundamentals of Computer Systems"]),
        (1, 2, "Internet of Things Applications and Design", 2, "Systems & Operating Systems", ["Fundamentals of Computer Systems"]),
        (1, 2, "Computer Network Systems I", 2, "Networking", []),
        (1, 2, "Web Technologies", 2, "Other", []),
        (1, 2, "Basic Probability and Statistics", 2, "Statistics", ["Mathematics for IT I"]),
        (1, 2, "Presentation Skills for ICT", 2, "Other", []),
        # Sem 3 (Y2S1)
        (2, 1, "Rapid Application Development", 3, "Programming", ["Object Oriented Programming"]),
        (2, 1, "System Analysis and Design", 2, "Software Engineering", ["Object Oriented Designing"]),
        (2, 1, "UX and UI Engineering", 3, "Software Engineering", ["Web Technologies"]),
        (2, 1, "Advanced Database Management Systems", 3, "Database", ["Fundamentals of Database Management Systems"]),
        (2, 1, "Computer Network Systems II", 2, "Networking", ["Computer Network Systems I"]),
        (2, 1, "Industry based Software Engineering Project", 0, "Software Engineering", ["Object Oriented Programming"]),
        (2, 1, "Mathematics for IT II", 2, "Mathematics", ["Mathematics for IT I"]),
        (2, 1, "Human Resource Management", 2, "Other", []),
        (2, 1, "Writing and Speaking Skills", 2, "Other", []),
        # Sem 4 (Y2S2)
        (2, 2, "Data Structures and Algorithms", 3, "Algorithms & Data Structures", ["Object Oriented Programming"]),
        (2, 2, "Software Engineering", 2, "Software Engineering", ["System Analysis and Design"]),
        (2, 2, "Operating Systems", 2, "Systems & Operating Systems", ["Computer Systems Architecture"]),
        (2, 2, "Project Management", 2, "Other", []),
        (2, 2, "Research Methodology", 2, "Other", []),
        (2, 2, "Industry based Software Engineering Project", 2, "Software Engineering", ["Industry based Software Engineering Project"]),
        (2, 2, "Statistical Distributions and Inference", 2, "Statistics", ["Basic Probability and Statistics"]),
        (2, 2, "Research Writing Skills", 2, "Other", []),
        # Sem 5 (Y3S1)
        (3, 1, "Advanced Web Technologies", 3, "Other", ["Web Technologies"]),
        (3, 1, "Management Information Systems", 3, "Database", ["Fundamentals of Database Management Systems"]),
        (3, 1, "Accounting and Financial Management", 3, "Other", []),
        (3, 1, "Principles of Economics", 2, "Other", []),
        (3, 1, "Information and Data Security", 2, "Cyber Security", ["Computer Network Systems II"]),
        (3, 1, "Computer Ethics and IT Law", 2, "Other", []),
        (3, 1, "Mobile Computing", 2, "Other", ["Object Oriented Programming"]),
        (3, 1, "Essentials of Artificial Intelligence", 3, "Artificial Intelligence", ["Data Structures and Algorithms"]),
        (3, 1, "Career Development Planning", 1, "Other", []),
        # Sem 6 (Y3S2)
        (3, 2, "E-commerce and Digital Marketing", 3, "Other", ["Web Technologies"]),
        (3, 2, "Organizational Behaviour", 2, "Other", ["Principles of Management"]),
        (3, 2, "Knowledge Management", 2, "Database", ["Management Information Systems"]),
        (3, 2, "Operational Research", 3, "Statistics", ["Basic Probability and Statistics"]),
        (3, 2, "Software Quality Assurance", 2, "Software Engineering", ["Software Engineering"]),
        (3, 2, "Enterprise Resource Planning Systems", 2, "Database", ["Management Information Systems"]),
        (3, 2, "Independent Research Study", 2, "Other", ["Research Methodology"]),
        (3, 2, "Geoinformatics", 2, "Other", []),
        (3, 2, "Location Based Services", 2, "Other", []),
        (3, 2, "Entrepreneurship and Innovation", 2, "Other", []),
        # Sem 7 (Y4S1)
        (4, 1, "Enterprise Architecture", 2, "Software Engineering", ["Management Information Systems"]),
        (4, 1, "Data Analytics", 2, "Data Analysis", ["Basic Probability and Statistics"]),
        (4, 1, "Information Systems Auditing and Control", 3, "Cyber Security", ["Information and Data Security"]),
        (4, 1, "Business Process Reengineering", 2, "Software Engineering", ["Enterprise Resource Planning Systems"]),
        (4, 1, "Operations and Supply Chain Management", 2, "Other", []),
        (4, 1, "Strategic IT Management", 2, "Other", ["Management Information Systems"]),
        (4, 1, "Deployment Engineering", 1, "Cloud Computing", []),
        (4, 1, "Digital Image Processing", 2, "Artificial Intelligence", []),
        (4, 1, "Emerging Technologies in ICT", 2, "Other", []),
        (4, 1, "Blockchain Technologies", 2, "Cyber Security", ["Information and Data Security"]),
        (4, 1, "Social Aspects and Professional Practices", 2, "Other", []),
        (4, 1, "Natural Language Processing", 2, "Artificial Intelligence", ["Essentials of Artificial Intelligence"]),
        (4, 1, "Individual Research Project", 2, "Other", ["Independent Research Study"]),
        # Sem 8 (Y4S2)
        (4, 2, "Individual Research Project", 7, "Other", ["Individual Research Project"]),
        (4, 2, "Industrial Training", 6, "Other", []),
    ],

    "Computer Engineering": [
        # Sem 1 (Y1S1)
        (1, 1, "Computer Systems Architecture", 3, "Systems & Operating Systems", []),
        (1, 1, "Foundation of Computer Engineering", 2, "Other", []),
        (1, 1, "Fundamentals of Programming", 2, "Programming", []),
        (1, 1, "Programming Laboratory", 1, "Programming", []),
        (1, 1, "Fundamentals of Databases", 2, "Database", []),
        (1, 1, "Software Development Methodologies", 2, "Software Engineering", []),
        (1, 1, "Probability and Statistics", 3, "Statistics", []),
        (1, 1, "Engineering Mathematics", 2, "Mathematics", []),
        (1, 1, "English: Basic Study Skills for CS/SE/CE", 2, "Other", []),
        (1, 1, "Leadership Training", 2, "Other", []),
        (1, 1, "Group Project in Hardware", 1, "Systems & Operating Systems", []),
        # Sem 2 (Y1S2)
        (1, 2, "Group Project in Hardware", 1, "Systems & Operating Systems", ["Group Project in Hardware"]),
        (1, 2, "Fundamentals of Electrical Engineering", 2, "Systems & Operating Systems", []),
        (1, 2, "Basic Electronics", 2, "Systems & Operating Systems", []),
        (1, 2, "Object Oriented Programming", 3, "Programming", ["Fundamentals of Programming"]),
        (1, 2, "Web Development", 2, "Other", []),
        (1, 2, "Computer Networks", 3, "Networking", []),
        (1, 2, "Discrete Mathematics", 2, "Mathematics", ["Engineering Mathematics"]),
        (1, 2, "Creative Media Tools", 1, "Other", []),
        (1, 2, "English: Advanced Study Skills for CS/SE/CE", 2, "Other", []),
        # Sem 3 (Y2S1)
        (2, 1, "Digital Electronics and Systems", 3, "Systems & Operating Systems", ["Basic Electronics"]),
        (2, 1, "Data Structures and Algorithms", 2, "Algorithms & Data Structures", ["Object Oriented Programming"]),
        (2, 1, "Operating Systems", 2, "Systems & Operating Systems", ["Computer Systems Architecture"]),
        (2, 1, "Advanced Object Oriented Programming", 2, "Programming", ["Object Oriented Programming"]),
        (2, 1, "Mobile Computing", 2, "Other", ["Object Oriented Programming"]),
        (2, 1, "Requirements Engineering", 2, "Software Engineering", ["Software Development Methodologies"]),
        (2, 1, "Calculus", 2, "Mathematics", ["Engineering Mathematics"]),
        (2, 1, "Statistical Distributions and Inference", 2, "Statistics", ["Probability and Statistics"]),
        (2, 1, "Principles of Management", 2, "Other", []),
        (2, 1, "Writing and Speaking Skills", 2, "Other", []),
        # Sem 4 (Y2S2)
        (2, 2, "Engineering Drawing", 2, "Other", []),
        (2, 2, "Advanced Computer Architecture", 3, "Systems & Operating Systems", ["Computer Systems Architecture"]),
        (2, 2, "Computer Interfacing and Microprocessors", 2, "Systems & Operating Systems", ["Operating Systems"]),
        (2, 2, "Rapid Application Development", 3, "Programming", ["Advanced Object Oriented Programming"]),
        (2, 2, "Artificial Intelligence", 3, "Artificial Intelligence", ["Data Structures and Algorithms"]),
        (2, 2, "Advanced Data Structures and Algorithms", 2, "Algorithms & Data Structures", ["Data Structures and Algorithms"]),
        (2, 2, "Numerical Methods", 2, "Mathematics", ["Calculus"]),
        (2, 2, "Research Writing Skills", 2, "Other", []),
        # Sem 5 (Y3S1)
        (3, 1, "Micro Controllers and Embedded Systems", 2, "Systems & Operating Systems", ["Computer Interfacing and Microprocessors"]),
        (3, 1, "Embedded Systems Laboratory", 1, "Systems & Operating Systems", ["Computer Interfacing and Microprocessors"]),
        (3, 1, "Research Methodology", 2, "Other", []),
        (3, 1, "Digital Signal Processing", 2, "Systems & Operating Systems", ["Calculus"]),
        (3, 1, "Design Project", 2, "Systems & Operating Systems", ["Digital Electronics and Systems"]),
        (3, 1, "Computer and Network Security", 2, "Cyber Security", ["Computer Networks"]),
        (3, 1, "Essentials of Computer Law", 2, "Other", []),
        (3, 1, "Applied Mechanics", 2, "Other", []),
        (3, 1, "Enterprise Systems Administration", 2, "Systems & Operating Systems", ["Operating Systems"]),
        (3, 1, "UX and UI Engineering", 2, "Software Engineering", ["Web Development"]),
        (3, 1, "Data Mining and Business Intelligence", 2, "Data Analysis", ["Fundamentals of Databases"]),
        (3, 1, "Digital Image Processing", 2, "Artificial Intelligence", ["Engineering Mathematics"]),
        (3, 1, "Expert Systems and Logic Programming", 2, "Artificial Intelligence", ["Artificial Intelligence"]),
        (3, 1, "Cloud Computing", 2, "Cloud Computing", ["Computer Networks"]),
        (3, 1, "Big Data Analytics", 2, "Data Analysis", ["Fundamentals of Databases"]),
        # Sem 6 (Y3S2)
        (3, 2, "Computer Systems Engineering", 2, "Systems & Operating Systems", ["Advanced Computer Architecture"]),
        (3, 2, "Digital Systems Design", 2, "Systems & Operating Systems", ["Digital Electronics and Systems"]),
        (3, 2, "Independent Research Study", 2, "Other", ["Research Methodology"]),
        (3, 2, "Electrical Properties of Materials", 2, "Systems & Operating Systems", ["Basic Electronics"]),
        (3, 2, "Information Security", 2, "Cyber Security", ["Computer and Network Security"]),
        (3, 2, "Statistical Tools for Data Analysis", 1, "Statistics", ["Statistical Distributions and Inference"]),
        (3, 2, "Robotics and Automation", 2, "Artificial Intelligence", ["Micro Controllers and Embedded Systems"]),
        (3, 2, "Telecommunication Networks", 2, "Networking", ["Computer Networks"]),
        (3, 2, "Complex Systems and Agent Technology", 2, "Artificial Intelligence", ["Artificial Intelligence"]),
        (3, 2, "Natural Language Processing", 2, "Artificial Intelligence", ["Artificial Intelligence"]),
        (3, 2, "Nature Inspired Computing", 2, "Artificial Intelligence", ["Artificial Intelligence"]),
        (3, 2, "Advanced Mobile Computing", 2, "Other", ["Mobile Computing"]),
        (3, 2, "Machine Learning", 2, "Artificial Intelligence", ["Artificial Intelligence"]),
        # Sem 7 (Y4S1)
        (4, 1, "VLSI Design and Fabrication", 3, "Systems & Operating Systems", ["Digital Systems Design"]),
        (4, 1, "Advanced Operating Systems", 2, "Systems & Operating Systems", ["Operating Systems"]),
        (4, 1, "Semiconductors and Solid State Devices", 2, "Systems & Operating Systems", ["Electrical Properties of Materials"]),
        (4, 1, "High Performance Computing", 2, "Cloud Computing", ["Advanced Computer Architecture"]),
        (4, 1, "Advanced Robotics", 2, "Artificial Intelligence", ["Robotics and Automation"]),
        (4, 1, "Advanced Natural Language Processing", 2, "Artificial Intelligence", ["Natural Language Processing"]),
        (4, 1, "Advanced IoT Systems", 2, "Systems & Operating Systems", ["Micro Controllers and Embedded Systems"]),
        (4, 1, "Deep Learning", 2, "Artificial Intelligence", ["Machine Learning"]),
        (4, 1, "Agent Based Systems and Community Modeling", 2, "Artificial Intelligence", ["Complex Systems and Agent Technology"]),
        (4, 1, "Location Based Services", 2, "Other", []),
        (4, 1, "Artificial Cognitive Systems", 2, "Artificial Intelligence", ["Artificial Intelligence"]),
        (4, 1, "Software Quality Assurance", 2, "Software Engineering", ["Requirements Engineering"]),
        (4, 1, "Individual Research Project", 2, "Other", ["Independent Research Study"]),
        (4, 1, "Entrepreneurship and Business Management", 2, "Other", []),
        (4, 1, "Social Aspects and Professional Practices", 2, "Other", []),
        # Sem 8 (Y4S2)
        (4, 2, "Individual Research Project", 7, "Other", ["Individual Research Project"]),
        (4, 2, "Industrial Training", 6, "Other", []),
    ],
}

PREFIX_MAP = {
    "Computer Science": "CS",
    "Software Engineering": "SE",
    "Data Science & Business Analytics": "DS",
    "Information Technology": "IT",
    "Information Systems": "IS",
    "Computer Engineering": "CE",
}

def main():
    print("Building full KDU computing curricula...")

    # 1. Write degrees.csv
    degrees_path = DATA_DIR / "degrees.csv"
    with open(degrees_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["degree_id", "name"])
        for d_id, name in DEGREES:
            writer.writerow([d_id, name])
    print(f"[OK] Wrote {len(DEGREES)} degrees to {degrees_path}")

    # 2. Assign unique course IDs and formatted course codes
    courses_out = []
    prereqs_out = []
    course_name_to_id = {}

    course_id_counter = 1

    from scripts.verify_curricula_line_by_line import txt_courses

    def map_course_type(raw_type: str) -> str:
        t = raw_type.strip()
        if "Elective" in t or "elective" in t:
            return "Elective"
        elif "Non-GPA" in t or "Credit not explicitly stated" in t:
            return "NGPA"
        else:
            return "Core"

    for degree_name, course_list in RAW_CURRICULA.items():
        prefix = PREFIX_MAP[degree_name]
        sem_counters = {}

        for year, semester, name, credits, subject_area, prereqs in course_list:
            sem_key = (year, semester)
            sem_counters[sem_key] = sem_counters.get(sem_key, 0) + 1
            code_num = sem_counters[sem_key]
            course_code = f"{prefix}{year}{semester}{code_num:02d}"

            raw_type = txt_courses[course_id_counter - 1]["type"]
            c_type = map_course_type(raw_type)

            course_record = {
                "course_id": course_id_counter,
                "course_code": course_code,
                "course_name": name,
                "degree": degree_name,
                "year": year,
                "semester": semester,
                "credits": credits,
                "subject_area": subject_area,
                "course_type": c_type,
                "prereqs": prereqs,
            }
            courses_out.append(course_record)
            course_id_counter += 1

    # 3. Build prerequisites list
    prereq_id_counter = 1
    for course in courses_out:
        deg = course["degree"]
        c_id = course["course_id"]
        for p_name in course["prereqs"]:
            matching_candidate = None
            for candidate in courses_out:
                if candidate["degree"] == deg and candidate["course_name"] == p_name and candidate["course_id"] < c_id:
                    matching_candidate = candidate
            if matching_candidate:
                prereqs_out.append({
                    "prerequisite_id": prereq_id_counter,
                    "course_id": c_id,
                    "prerequisite_course_id": matching_candidate["course_id"],
                })
                prereq_id_counter += 1
            else:
                print(f"Warning: Prereq '{p_name}' not found for {deg} -> {course['course_name']}")

    # 4. Write courses.csv
    courses_path = DATA_DIR / "courses.csv"
    with open(courses_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["course_id", "course_code", "course_name", "degree", "year", "semester", "credits", "subject_area", "course_type"])
        for c in courses_out:
            writer.writerow([
                c["course_id"],
                c["course_code"],
                c["course_name"],
                c["degree"],
                c["year"],
                c["semester"],
                c["credits"],
                c["subject_area"],
                c["course_type"],
            ])
    print(f"[OK] Wrote {len(courses_out)} courses to {courses_path}")

    # 5. Write prerequisites.csv
    prereqs_path = DATA_DIR / "prerequisites.csv"
    with open(prereqs_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["prerequisite_id", "course_id", "prerequisite_course_id"])
        for p in prereqs_out:
            writer.writerow([p["prerequisite_id"], p["course_id"], p["prerequisite_course_id"]])
    print(f"[OK] Wrote {len(prereqs_out)} prerequisites to {prereqs_path}")

if __name__ == "__main__":
    main()
