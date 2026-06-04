import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="Blood Report Analyzer",
    page_icon="🩸",
    layout="wide"
)

# Title
st.title("🩸 AI Blood Report Analyzer")
st.markdown(
    "Upload your blood report (.txt) and get AI-powered health insights and diet recommendations."
)

# Check API key
if not os.getenv("GOOGLE_API_KEY"):
    st.error("GOOGLE_API_KEY not found in .env file")
    st.stop()

# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# Upload File
uploaded_file = st.file_uploader(
    "Upload Blood Report",
    type=["txt"]
)

if uploaded_file is not None:

    blood_report = uploaded_file.read().decode("utf-8")

    st.subheader("📄 Uploaded Blood Report")

    st.text_area(
        label="Report Content",
        value=blood_report,
        height=250
    )

    if st.button("🔍 Analyze Report"):

        # -----------------------------
        # Step 1: Extract Blood Values
        # -----------------------------
        with st.spinner("Extracting blood parameters..."):

            extraction_prompt = f"""
You are an expert pathology assistant.

Analyze the following blood report.

Extract all blood parameters.

For each parameter provide:

1. Test Name
2. Observed Value
3. Reference Range
4. Status (HIGH / LOW / NORMAL)

Return in a clean markdown table.

Blood Report:

{blood_report}
"""

            extraction_response = llm.invoke(extraction_prompt)

            extracted_values = extraction_response.content

        st.subheader("📊 Blood Parameter Analysis")
        st.markdown(extracted_values)

        # -----------------------------
        # Step 2: Health Summary
        # -----------------------------
        with st.spinner("Generating health summary..."):

            summary_prompt = f"""
You are an experienced physician.

Based on the blood report analysis below:

1. Summarize overall health status.
2. Mention important abnormalities.
3. Mention possible risks.
4. Keep explanation simple.

Blood Analysis:

{extracted_values}
"""

            summary_response = llm.invoke(summary_prompt)

            health_summary = summary_response.content

        st.subheader("🩺 Health Summary")
        st.markdown(health_summary)

        # -----------------------------
        # Step 3: Diet Recommendation
        # -----------------------------
        with st.spinner("Generating diet recommendations..."):

            diet_prompt = f"""
You are a certified Indian nutritionist.

Based on this blood report analysis:

{extracted_values}

Provide:

## Foods To Eat More
## Foods To Avoid
## Lifestyle Recommendations
## Daily Habits

Keep recommendations practical for Indian diets.
"""

            diet_response = llm.invoke(diet_prompt)

            diet_plan = diet_response.content

        st.subheader("🥗 Diet Recommendations")
        st.markdown(diet_plan)

        st.success("Analysis Completed Successfully ✅")