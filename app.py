import streamlit as st
import PyPDF2
import openai

# Replace with your actual OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

st.set_page_config(page_title="AI Resume Screener", layout="centered")

st.title("Bluebird AI Resume Screener")
st.markdown("Upload a resume and paste the job description. This AI will tell you how well the candidate fits the role.")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste the Job Description Here")

if uploaded_file and job_description:
    # Extract text from PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    resume_text = ""
    for page in pdf_reader.pages:
        resume_text += page.extract_text()

    with st.spinner("Analyzing..."):
        prompt = f"""
You are an AI HR assistant. A resume has been uploaded. Based on the following job description, analyze the resume.

Job Description:
{job_description}

Resume Content:
{resume_text}

Please answer the following:
1. What is the candidate's overall experience and key strengths?
2. List top relevant skills that match the job.
3. How well does this candidate fit the role? Give a score out of 10.
4. Any concerns or red flags?

Format your response cleanly.
"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=800
        )

        st.markdown("### AI Analysis")
        st.write(response['choices'][0]['message']['content'])
