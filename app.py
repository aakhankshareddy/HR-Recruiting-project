import streamlit as st
import pandas as pd

# Brings in Pandas for working with data tables (dataframes).
from agent_logic import (
    parse_resume_pdf_agent,
    parse_resume_text_agent,
    extract_skills_agent,
    get_candidate_name_agent,
    calculate_score_agent
)
# Imports the functions we wrote in agent_logic.py.

st.set_page_config(
    page_title="Recruitment AI Agent", 
    page_icon="🔎",
    layout="centered"
)

# Sets up the look and feel of the Streamlit app.:
st.title("Recruitment AI Agent")
st.subheader("Automated Resume Screening with AI")

job_description = st.text_area(
    "Enter the Job Description Here:",
    height=200,
    placeholder="E.g., Looking for a Data Scientist with experience in Python, Machine Learning, and Data Visualization."
)
# A text area for the user to input the job description.

uploaded_resumes = st.file_uploader(
    "Upload Resumes (PDF or TXT)",
    type=["pdf", "txt"],
    accept_multiple_files=True
)
# A file uploader that allows multiple PDF or TXT files.
# uploaded_resumes will be a list of uploaded file objects.

if st.button("Screening Candidates", use_container_width=True):
    # A button to trigger the screening process.
    if job_description and uploaded_resumes:
        with st.spinner("Screening candidates.."):
            job_skills = extract_skills_agent(job_description)
            # Extracts skills from the job description using our agent function.

            candidate_results = []
            # Initializes an empty list to store candidate results.

            for resume_file in uploaded_resumes:
                file_extension = resume_file.name.split(".")[-1].lower()
                # Gets the file extension (pdf or txt) in lowercase.

                if file_extension == "pdf":
                    resume_text = parse_resume_pdf_agent(resume_file)
                elif file_extension == "txt":
                    resume_text = parse_resume_text_agent(resume_file)
                else:
                    st.warning(f"Unsupported file type: {resume_file.name}")
                    continue

                # Extract candidate name and skills
                resume_skills = extract_skills_agent(resume_text)
                score = calculate_score_agent(job_skills, resume_skills)

                candidate_results.append({
                    "Candidate Name": get_candidate_name_agent(resume_text),
                    "Match Score ": score,
                    "Matching Skills": ", ".join(resume_skills.intersection(job_skills)),
                    "File Name": resume_file.name
                })

        # Sort candidates by match score in descending order.
        candidate_results.sort(key=lambda x: x["Match Score "], reverse=True)

        st.success("Screening completed!")
        st.markdown("---")
        st.header("Candidate Rankings")

        df = pd.DataFrame(candidate_results)
        st.dataframe(df, use_container_width=True)

        st.markdown("---")
        st.header("Data Analysis")

        for candidate in candidate_results:
            st.subheader(f"Analysis for {candidate['Candidate Name']}")
            st.metric(label="Match Score", value=f"{candidate['Match Score ']:.2f}%")
            
            st.markdown("Matching Skills:")
            if candidate["Matching Skills"]:
                st.code(candidate["Matching Skills"])
            else:
                st.write("No matching skills found.")   
    else:
        st.warning("Please provide a job description and upload at least one resume.")