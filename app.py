import streamlit as st
import openai
from dotenv import load_dotenv
import os
import fitz

load_dotenv()
st.info(
    """Many job seekers face challenges when 
         submitting their resumes to various job portals 
         and companies. The existing resume parsers often 
         fail to accurately extract and categorize essential 
         information such as names, contact details, work experiences, 
         and education. As a result, job seekers encounter errors and 
         inconsistencies, leading to potential job application issues and 
         missed opportunities."""
)

# st.success(
#     """ParsyPro resume parsing app aims to address these
#     challenges and provide a seamless experience for job seekers. Using advanced
#     AI technologies like OpenAI's GPT-3.5-turbo, ParsyPro ensures accurate and
#     efficient extraction of crucial information from resumes in various formats, including PDF and DOCX.
# Upon uploading their resumes, users will witness ParsyPro's powerful AI engine
# in action, effectively identifying and grouping key details like names, email addresses,
# phone numbers, work experiences, and education qualifications. The app's intelligent chat-based
# interface allows users to interact naturally, enabling specific queries and extraction of personalized information."""
# )


st.sidebar.header("Resume Parser")

openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the custom prompts to get specific information
prompts = {
    "Name ": "Please extract the name of the person applying from this resume.",
    "Contact 📱 📧": "Please extract the contact details (phone number and email) from the resume.",
    "Experience 👨🏽‍💻👩🏼‍🔬": "Please extract the work experience details from the resume and format properly.",
    "Education 🎓": "Please extract the education details from the resume and format properly.",
    "Skills 🤹🏻‍♂️🦸🏾‍♀️": "Please extract the skills details from the resume.",
    "Links 👾": "Please extract the links like github, personal website, linkedin details from the resume.",
}

uploaded_file = st.sidebar.file_uploader("Choose a file", type=["pdf"])

job_link = st.sidebar.text_input(label="Job Description Link", value="")
if st.sidebar.button("Compare 🪞"):
    st.toast("Comparison completed", icon="👍🏾")

if uploaded_file is not None:
    # Read the PDF file and extract the text content
    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text_content = ""
    for page in pdf_document:
        text_content += page.get_text()

    # Display the text content of the PDF file
    with st.expander("Parsed Resume"):
        st.write(text_content)

    # Use OpenAI ChatGPT to extract specific information
    for prompt_name, prompt_text in prompts.items():
        response = openai.ChatCompletion.create(
            model="gpt-4",  # You can use the model of your choice
            messages=[
                {"role": "system", "content": prompt_text},
                {"role": "user", "content": text_content},
            ],
        )
        extracted_info = response["choices"][0]["message"]["content"].strip()

        with st.expander(prompt_name):
            st.write(f"{prompt_name.capitalize()}: {extracted_info}")
