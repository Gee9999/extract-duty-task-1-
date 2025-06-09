import streamlit as st
from pathlib import Path
import pandas as pd
from src.extract_duties import parse_customs_report

st.set_page_config(page_title="Duty & Invoice Loader")
st.title("🔍 Duty Extraction & Invoice Loader")

st.markdown("Upload your **Customs Worksheet** (Excel/CSV or PDF) below.")

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
        st.error(f"⚠️ Error parsing worksheet: {e}")
        st.stop()

    inv_file = st.file_uploader("Now upload your Invoice (CSV/XLSX)", type=["csv","xls","xlsx"])
    if inv_file:
        inv_tmp = Path("temp_invoice" + Path(inv_file.name).suffix)
        inv_tmp.write_bytes(inv_file.getbuffer())
        try:
            if inv_tmp.suffix.lower() in [".xls", ".xlsx"]:
                df_inv = pd.read_excel(inv_tmp, engine="openpyxl")
            else:
                df_inv = pd.read_csv(inv_tmp, encoding="utf-8-sig")
            st.subheader("Invoice Preview")
            st.dataframe(df_inv.head(10))
        except Exception as e:
            st.error(f"⚠️ Error loading invoice: {e}")
