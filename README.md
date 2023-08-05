# 📄 Resume Parser

## Overview 🚀

Many job seekers face challenges when submitting their resumes to various job portals and companies. The existing resume parsers often fail to accurately extract and categorize essential information such as names, contact details, work experiences, and education. As a result, job seekers encounter errors and inconsistencies, leading to potential job application issues and missed opportunities.

To address this issue, I have developed the "Resume Parser" app, powered by OpenAI's advanced language model. The app aims to enhance the resume parsing process, ensuring accurate extraction of vital information and providing job seekers with a seamless experience when applying for jobs.

## Features ✨

- Extracts and organizes key information from resumes, including names, contact details, work experiences, education, skills, and more.
- Utilizes OpenAI's ChatGPT to enable natural language interactions and personalized queries for specific information extraction.
- Supports various resume formats, such as PDF and DOCX, making it convenient for users to upload their resumes.
- Provides a user-friendly interface with expandable sections for displaying the parsed resume and extracted information.

## How to Use 📝

1. Clone this repository to your local machine.

2. Install the required dependencies:
   ```
   pip install streamlit fitz openai-python dotenv
   ```

3. Create a `.env` file in the root directory and set your OpenAI API key and organization ID:
   ```dotenv
   OPENAI_API_KEY="your_openai_api_key"
   OPENAI_ORG="your_openai_organization_id"
   ```

4. Run the Streamlit app locally:
   ```
   streamlit run app.py
   ```

5. Upload your resume in PDF or DOCX format using the file uploader in the sidebar.

6. Observe the extracted information in expandable sections based on the defined prompts.

## Future Enhancements 🚀

This project is open to contributions, and I welcome feedback and suggestions for improvement. Some potential future enhancements include:

- Supporting additional resume formats for better compatibility.
- Implementing further natural language understanding to handle more complex prompts.
- Expanding the list of predefined prompts for extracting various types of information.

## License 📜

This project is licensed under the [MIT License](LICENSE).

Feel free to use and modify the code according to your needs. Happy parsing! 🎉