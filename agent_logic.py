import spacy
# Load the spaCy language model
# Define functions or classes for agent logic
# Implement recruitment-related NLP processing
# think of it like a toolbox for text: tokenization,
# named entity recognition, (detects entities --> ex: python:LANGUAGE, machine learning: FIELD)
# part-of-speech tagging etc

from pypdf import PdfReader
# Import PDFReader from pypdf for reading PDF files
# Add additional imports or logic as needed for recruitment agent functionality
# used to extract text from pdf files

import io  # Import io module for handling file streams and in-memory files

# load spaCy NLP model 
try:
    nlp = spacy.load("en_core_web_sm")
    # loads a small English NLP model on "en_core_web_sm" from spaCy
    # nlp is a variable that will hold a ready-to-use NLP pipeline
except OSError:
    print("Downloading spaCy model")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")  
    # Load the model after downloading
    # spaCy, spacy.cli is a module that contains functions
    # The nlp object is now ready for NLP tasks such as tokenization, NER, POS tagging, etc.
    # normally we run this command from terminal/command line
    # downloads the NLP model. happens only once on the system
    nlp = spacy.load("en_core_web_sm")
    # load the model again after downloading so we can use it immediately

# the Resume Parsing Agent functions
def parse_resume_pdf_agent(pdf_file):
    """Extracts text from PDF file."""
    try: 
        reader = PdfReader(io.BytesIO(pdf_file.read()))
        # pdf_file.read() -> reads the whole PDF file into bytes
        # io.BytesIO(...) -> converts the bytes into in-memory file-like objects
        # PDFReader(...) -> creates a PDF reader object to read pages
        text = ""
        # initializes an eempty string tostore extracted text
        for page in reader.pages:
        # loops through all pages in PDF
            text += page.extract_text() or ""
        # page.extract_text() -> extracts text from current page
        # or "" -> ensures that if extraction fails, we add empty string insted of None
        # text += -> appends extracted text to the text variable
        return text 
        # returns all extracted text from pdf
    except Exception as e:
        return f"Error extracting text: {e}"
    
def parse_resume_text_agent(txt_file):
    """Extracts text from TXT file"""
    return txt_file.get_value().decode("utf-8")
    # txt_file.get_value() -> reads the entire content uploaded text file as bytes
    # .decode("utf-8") -> converts bytes to UTF-8 string.(normal python text)
    # returns the decoded text content

# the skill exctraction agent function
def extract_skills_agent(text):
    """Extracts skills from using pre-defined list."""
    skills_list = [
        "Python", "Java", "C++", "JavaScript", "SQL", "HTML", "CSS", "React", "Node.js", "Django",
        "Flask", "Machine Learning", "Deep Learning", "Data Analysis", "NLP", "TensorFlow", "PyTorch",
        "AWS", "Azure", "Docker", "Kubernetes", "Git", "Linux", "Agile", "Scrum", "Jenkins",
        "Tableau", "Power BI", "REST API", "GraphQL", "MongoDB", "PostgreSQL", "Spark", "Hadoop",
        "Pandas", "NumPy", "Scikit-learn", "FastAPI", "TypeScript", "Vue.js", "Angular", "CI/CD"
    ]
    # a list of pre-defined skills to look for in the resume

    doc = nlp(text.lower())
    # text.lower() -> converts text to lowercase
    # passes it to nlp(...) -> spaCy breaks text into tokens, sentences, etc
    found_skills = {token.text for token in doc if token.text in skills_list}
    # set comprehension:
    # loops over each token in text
    # if token is in skills_list, include it in found_skills
    # {...} -> cretaes a set (uniques skills only)
    return found_skills
# returns the set of skills found in resume

# the candidate information agent function
def get_candidate_name_agent(resume_text):
    """Extracts a simple name from the first few lines of text"""
    lines = resume_text.strip().split('\n')
    # .strip() -> removes leading/trailing whitespaces
    # .split('\n') -> splits the text into list of lines
    if lines:
    # checs if the list is not empty
        return lines[0].strip()
        # returns the first line of candidate's name (removing extra spaces)
    return "Unknown Candidate"
    # if no lines found, return default name.

# scoring and ranking agent function
def calculate_score_agent(resume_skills, job_skills):
    """Calculate a match score based on shared skills"""
    if not job_skills:
        return 0.0
        # if job_skills is empty, return 0 score (avoids division by zero)

    matching_skills = resume_skills.intersection(job_skills)
    # find common skills between resume and job requirements
    score = (len(matching_skills/ len(job_skills))) * 100
    # percentage match = (numberof matching skills + total job skills) * 100
    return round(score, 2)
    # returns score rounded to 2 decimal places

    # Summary:
    # 1. Loads spaCy NLP model for text processing tasks like tokenization and entity recognition.
    # 2. Defines functions to extract text from PDF and TXT resume files.
    # 3. Implements skill extraction from resume text using a predefined skills list and spaCy tokenization.
    # 4. Provides a function to extract candidate name from the first line of resume text.
    # 5. Calculates a match score between resume skills and job requirements for ranking candidates.
    # 6. Handles errors gracefully and uses comments to explain logic throughout the code.