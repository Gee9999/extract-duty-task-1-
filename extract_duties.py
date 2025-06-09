import streamlit as st
from pathlib import Path
import pandas as pd
from src.extract_duties import parse_customs_report

st.set_page_config(page_title="Duty & Invoice Loader")
st.title("🔍 Duty Extraction & Invoice Loader")

st.markdown("Upload your **Customs Worksheet** (Excel or PDF) below.")

cust_file = st.file_uploader("Customs Worksheet", type=["pdf","xls","xlsx","csv"])
if cust_file:
    tmp = Path("temp_report" + Path(cust_file.name).suffix)
    tmp.write_bytes(cust_file.getbuffer())
    try:
        duty_map = parse_customs_report(tmp)
        st.success("✅ Duties extracted!")
        st.dataframe(
            pd.DataFrame(
                [{"description": d, "duty %": p} for d,p in duty_map.items()]
            )
        )
    except Exception as e:
        st.error(f"⚠️ Error: {e}")
