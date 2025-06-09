def parse_customs_report(path):
    """
    Read PDF/XLSX/CSV customs worksheet and return dict[description:str] -> duty:int
    """
    import pathlib, re, pandas as pd, pdfplumber
    from PyPDF2 import PdfReader

    ext = pathlib.Path(path).suffix.lower()
    duty_map = {}
    if ext in ['.xlsx', '.xls']:
        df = pd.read_excel(path, engine='openpyxl', header=None)
        # TODO: implement Excel/CSV parsing logic
    elif ext == '.csv':
        df = pd.read_csv(path, header=None)
        # TODO: implement CSV parsing logic
    else:
        # PDF fallback
        try:
            reader = pdfplumber.open(str(path))
            text = "\n".join(page.extract_text() or '' for page in reader.pages)
        except Exception:
            reader = PdfReader(str(path))
            text = "\n".join(page.pages[i].extract_text() or '' for i in range(len(reader.pages)))
        for line in text.splitlines():
            m = re.search(r"(.*?)\s+(\d{1,2})\s?%$", line.strip())
            if m:
                desc, duty = m.group(1).strip(), int(m.group(2))
                duty_map[desc.lower()] = duty
    return duty_map
