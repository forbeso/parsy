import streamlit as st
import openai
from dotenv import load_dotenv, find_dotenv
import os
import fitz
import pytesseract
from PIL import Image
import re
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
)
from langchain.chains import LLMChain
from langchain import ConversationChain


load_dotenv(find_dotenv())

role = ["AI", "user"]

# openai.organization = os.getenv("OPENAI_ORG")
# openai.api_key = os.getenv("OPENAI_API_KEY")


# st.info(
#     """Many job seekers face challenges when
#          submitting their resumes to various job portals
#          and companies. The existing resume parsers often
#          fail to accurately extract and categorize essential
#          information such as names, contact details, work experiences,
#          and education. As a result, job seekers encounter errors and
#          inconsistencies, leading to potential job application issues and
#          missed opportunities."""
# )

# Define the custom prompts to get specific information
prompts = {
    "Name ": "Please extract the name of the person applying from this resume.",
    "Contact 📱 📧": "Please extract the contact details (phone number and email) from the resume.",
    "Experience 👨🏽‍💻👩🏼‍🔬": "Please extract the work experience details from the resume and format properly.",
    "Education 🎓": "Please extract the education details from the resume and format properly.",
    "Skills 🤹🏻‍♂️🦸🏾‍♀️": "Please extract the skills details from the resume.",
    "Links 👾": "Please extract the links like github, personal website, linkedin details from the resume.",
    # "Cover Letter": "Please create a cover letter based on the resume and {} if a job description is provided below".format(
    #     job_descr
    # ),
}

user_question = st.chat_input(
    placeholder="your message here",
    key="userInput",
    max_chars=None,
    disabled=False,
)

with st.sidebar:
    st.header("Talk to your docs")

    # user_key = st.sidebar.text_input(
    #     "Your Open AI Key", value="", help="Input your Open AI Key to use the app."
    # )

    uploaded_files = st.sidebar.file_uploader("Choose a file", type=["pdf"])


def get_doc_content():
    # Read the PDF file and extract the text content
    pdf_document = fitz.open(
        stream=uploaded_files.read(),
        filetype="pdf",
    )
    text_content = ""

    for page in pdf_document:
        text_content += page.get_text()

    # Handle special characters and bullet points using regular expressions
    text_content = re.sub(r"\s+([•●▪▸*-])\s+", r" \1 ", text_content)
    text_content = re.sub(r"\s+([,.:;?!(){}\[\]])\s+", r"\1 ", text_content)

    return text_content


def sendMessage(user_question):
    if user_question and uploaded_files is not None:
        text_content = get_doc_content()
        with st.chat_message(name="user"):
            st.write(user_question)
        # Display the text content of the PDF file
        with st.chat_message(name="assistant"):
            with st.expander("Parsed Document Details"):
                st.write("The details I gathered from your document: \n")
                st.write(text_content)

                # Use OpenAI ChatGPT to extract specific information
                # for prompt_name, prompt_text in prompts.items():
                #     response = openai.ChatCompletion.create(
                #         model="gpt-4",  # You can use the model of your choice
                #         messages=[
                #             {"role": "system", "content": prompt_text},
                #             {"role": "user", "content": text_content},
                #         ],
                #     )
                #     extracted_info = response["choices"][0]["message"]["content"].strip()

                #     with st.expander(prompt_name):
                #         st.write(f"{prompt_name.capitalize()}: {extracted_info}")

        with st.chat_message(name="assistant"):
            llm = ChatOpenAI(
                model="gpt-4",
            )
            conversation = ConversationChain(llm=llm, verbose=True)

            # Pass the value of the variable text_content to the predict() method
            output = conversation.predict(
                input=user_question + " according to: \n {} ".format(text_content)
            )

            st.success(output)
    else:
        with st.chat_message(name="AI"):
            st.write("Please remember to add a document")


if user_question:
    sendMessage(user_question=user_question)
