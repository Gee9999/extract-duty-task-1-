import streamlit as st
from pathlib import Path
from src.extract_duties import parse_customs_report

st.set_page_config(page_title="Duty Extractor")
st.title("Duty Extraction Tester")

file = st.file_uploader("Upload customs report", type=["pdf","xls","xlsx","csv"])
if file:
    tmp_dir = Path("temp_report")
    tmp_dir.mkdir(exist_ok=True)
    tmp = tmp_dir / file.name
    tmp.write_bytes(file.getbuffer())
    try:
        duties = parse_customs_report(tmp)
        st.success("Extracted duties:")
        st.json(duties)
    except Exception as e:
        st.error(f"Error: {e}")
