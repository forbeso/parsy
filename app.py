import streamlit as st
import fitz
import openai


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


st.sidebar.header("Resume Parser")

# OpenAI API Key - Replace 'YOUR_OPENAI_API_KEY' with your actual API key
openai.organization = "org-1cNNF3rlpTglSpDuuuHxFMQE"
openai.api_key = "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"

# Define the custom prompts to get specific information
prompts = {
    "Name": "Please extract the name of the person applying from this resume.",
    "Contact": "Please extract the contact details (phone number and email) from the resume.",
    "Experience": "Please extract the experience details from the resume and format properly.",
    "Education": "Please extract the education details from the resume and format properly.",
    "Skills": "Please extract the skills details from the resume.",
    # Add more prompts for other information you want to extract
}

uploaded_file = st.sidebar.file_uploader("Choose a file", type=["pdf"])
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
