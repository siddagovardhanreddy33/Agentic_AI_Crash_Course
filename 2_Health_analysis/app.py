import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# Gemini Model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)

# Page Config
st.set_page_config(
    page_title="Blood Work Analysis",
    page_icon="🩸",
    layout="wide"
)

st.title("🩸 Blood Work Analysis Assistant")

uploaded_file = st.file_uploader(
    "Upload Blood Report (.txt)",
    type=["txt"]
)

if uploaded_file:

    blood_report = uploaded_file.read().decode("utf-8")

    st.subheader("Uploaded Blood Report")

    st.text_area(
        label="Blood Report",
        value=blood_report,
        height=300
    )

    if st.button("Analyze Report"):

        # ==========================
        # Prompt 1 (UNCHANGED)
        # ==========================

        extraction_prompt = f""" 
you are a medical data extraction assistant

from the blood report below , extract ALL test values and classify each as HIGH, LOW, or Normal 
based on the reference ranges provided in the report .

format your response as :
- Test Name:Value | Status:HIGH/LOW/NORMAL | Reference:range
Return in a clean markdown table.


Blood Report : {blood_report}

"""

        with st.spinner("Extracting blood values..."):

            extraction_response = llm.invoke(extraction_prompt)

            extracted_values = extraction_response.content

        st.subheader("📊 Blood Work Analysis")

        st.markdown(extracted_values)

        # ==========================
        # Prompt 2 (UNCHANGED)
        # ==========================

        dite_prompt = f"""   
You are a clinical nutritionist specializing in Indian dietary habits.

Based on the blood work analysis below , write:
1. A short health summary in 4-5 lines explaining the patient's condition in simple language
2. A short , practical Indian dite plan having only two sections (1) foods to avoide , (2)foods to eat more of . 
Do not include any other sections in the dite plan

Blood Work Analysis : {extracted_values}

"""

        with st.spinner("Generating health summary and diet plan..."):

            dite_response = llm.invoke(dite_prompt)

        st.subheader("🥗 Health Summary & Diet Plan")

        st.markdown(dite_response.content)

        st.success("Analysis Completed")