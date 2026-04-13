import streamlit as st

from src.preprocess import preprocess_logs
from src.retrieve import retrieve_similar_incidents
from src.analyze import analyze_root_cause


st.set_page_config(page_title="AI Root Cause Analyzer", layout="wide")

st.title("AI Root Cause Analyzer")
st.write("Upload logs or paste raw logs to identify the likely root cause of an incident.")

uploaded_file = st.file_uploader("Upload a log file", type=["log", "txt"])
log_text_input = st.text_area("Or paste logs here", height=250)

analyze_clicked = st.button("Analyze Root Cause")


def read_uploaded_file(file) -> str:
    return file.read().decode("utf-8", errors="ignore")


if analyze_clicked:
    raw_logs = ""

    if uploaded_file is not None:
        raw_logs = read_uploaded_file(uploaded_file)
    elif log_text_input.strip():
        raw_logs = log_text_input.strip()

    if not raw_logs:
        st.warning("Please upload a log file or paste logs.")
    else:
        with st.spinner("Analyzing logs..."):
            cleaned_logs, suspicious_lines, log_summary = preprocess_logs(raw_logs)
            retrieved_docs = retrieve_similar_incidents(log_summary, k=3)
            rca_result = analyze_root_cause(log_summary, suspicious_lines, retrieved_docs)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Suspicious Log Lines")
            if suspicious_lines:
                for line in suspicious_lines:
                    st.code(line)
            else:
                st.info("No suspicious lines detected.")

            st.subheader("Condensed Log Summary")
            st.text(log_summary)

        with col2:
            st.subheader("Similar Past Incidents")
            for doc in retrieved_docs:
                st.markdown(f"**{doc.metadata.get('title', 'Unknown Incident')}**")
                st.write(doc.page_content)
                st.markdown("---")

        st.subheader("Root Cause Analysis")
        st.write(rca_result)