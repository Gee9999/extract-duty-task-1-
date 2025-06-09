import streamlit as st
from pathlib import Path
import pandas as pd
from src.extract_duties import parse_customs_report

st.set_page_config(page_title="Duty & Invoice Loader")
st.title("🔍 Duty Extraction & Invoice Loader")

st.markdown("""
Upload the **Customs Worksheet PDF** below. The app will scan its lines
for table rows and extract each item’s description → duty%.
""")

cust_file = st.file_uploader("Customs Worksheet PDF", type=["pdf"])
if cust_file:
    tmp = Path("temp.pdf")
    tmp.write_bytes(cust_file.getbuffer())

    try:
        duties = parse_customs_report(tmp)
        st.success("✅ Duties extracted!")
        st.dataframe(
            pd.DataFrame(
                [{"description": desc, "duty %": duty} for desc, duty in duties.items()]
            )
        )
    except Exception as e:
        st.error(f"⚠️ Error: {e}")
