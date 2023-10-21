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
from langchain.chains import LLMChain, ConversationChain

from docx import Document

import io

load_dotenv(find_dotenv())


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

st.header("Get Answers From Your Docs Before You Can Say...")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_question = st.chat_input(
    placeholder="your message here",
    key="userInput",
    max_chars=None,
    disabled=False,
)

with st.sidebar:
    st.header("Which document would you like to talk to?")

    # user_key = st.sidebar.text_input(
    #     "Your Open AI Key", value="", help="Input your Open AI Key to use the app."
    # )

    uploaded_files = st.sidebar.file_uploader(
        "Choose a file", type=["pdf", "docx", "txt"]
    )


def get_initial_msgs():
    with st.chat_message(name="assistant"):
        st.info(
            """
            Hello! I am Parsly, an AI assistant that can 
                 read your documents and answer your questions. I am still under development, 
                 but I have learned to perform many kinds of tasks, including:
                 I can read and understand your documents, including PDFs, Word documents, and email messages. 
                 I can answer your questions about your documents, even if they are open ended, challenging, or strange.
                I can generate different creative text formats of text content, like poems, code, scripts, 
                musical pieces, email, letters, etc. I will try my best to fulfill all your requirements.
            """
        )


def get_doc_content():
    word_document = Document(docx=io.BytesIO(uploaded_files.read()))

    content = ""
    for paragraph in word_document.paragraphs:
        content += paragraph.text

    return content


def get_pdf_content():
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
    st.write(uploaded_files.type)
    st.write(uploaded_files.name)

    return text_content


def sendMessage(user_question):
    if user_question is not None:
        if uploaded_files is not None:
            # calls function to parse uploaded document
            text_content = ""
            if uploaded_files.type == "application/pdf":
                text_content = get_pdf_content()
            else:
                text_content = get_doc_content()

            with st.chat_message(name="user"):
                st.write(user_question)
                # Add user message to chat history
                st.session_state.messages.append(
                    {"role": "user", "content": user_question}
                )
            # Display the text content of the PDF file
            with st.chat_message(name="assistant"):
                with st.expander("Parsed Document Details"):
                    st.write("The details I gathered from your document: \n")
                    st.write(text_content)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": text_content}
                    )

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
                with st.spinner("🤔"):
                    llm = ChatOpenAI(model="gpt-4", streaming=True)
                    conversation = ConversationChain(llm=llm, verbose=True)

                    # Pass the value of the variable text_content to the predict() method
                    output = conversation.predict(
                        input="Your task is to answer any questions and related tasks based on the information provided. \n Here is the question: "
                        + user_question
                        + " \n and here is the content: \n {} ".format(text_content)
                    )

                    st.write(output)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": output}
                    )
        else:
            with st.chat_message(name="assistant"):
                no_document = """Hi, I'm here to help you with knowing your 
                documents better. Please remember to add a document by using the upload feature
                in the sidebar to the left."""
                st.write(no_document)
                st.session_state.messages.append(
                    {"role": "assistant", "content": no_document}
                )


get_initial_msgs()

if user_question:
    sendMessage(user_question=user_question)
