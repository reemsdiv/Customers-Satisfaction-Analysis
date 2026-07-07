import pandas as pd
import sys

sys.stdout.reconfigure(encoding="utf-8")

INPUT_FILE = "data_cleaned.xlsx"
OUTPUT_FILE = "indicators_summary.xlsx"

# Row 1 has the Arabic question text, row 2 has the real column codes (Q1, Q2, F1, ...)
df = pd.read_excel(INPUT_FILE, header=1)

# أسئلة كل مؤشر (كل سؤال يُحسب لوحده، بدون دمج)
CSAT_COLS = ["Q1", "Q3", "Q3b", "Q3c", "Q3d", "Q5b", "Q5c"]
CES_COL = "Q2"
NPS_COL = "Q8"


# دوال حساب المؤشرات

def calc_csat(series):
    """CSAT لسؤال واحد = % (راضٍ تماماً + راضٍ نوعاً ما) من إجمالي المجيبين على السؤال."""
    s = series.dropna()
    if len(s) == 0:
        return None
    satisfied = s.isin([4, 5]).sum()
    return round((satisfied / len(s)) * 100, 2)


def calc_ces(series):
    """CES = % (سهل جداً + سهل نوعاً ما) - % (صعب + صعب نوعاً ما). النطاق -100 إلى 100."""
    s = series.dropna()
    if len(s) == 0:
        return None
    easy = s.isin([4, 5]).sum()
    hard = s.isin([1, 2]).sum()
    return round(((easy - hard) / len(s)) * 100, 2)


def calc_nps(series):
    """NPS = % الموصون (9-10) - % غير الموصون (0-6). النطاق -100 إلى 100."""
    s = series.dropna()
    if len(s) == 0:
        return None
    promoters = s.isin([9, 10]).sum()
    detractors = s[s <= 6].shape[0]
    return round(((promoters - detractors) / len(s)) * 100, 2)


# ============================================================

overall_rows = []
for col in CSAT_COLS:
    overall_rows.append({"المؤشر": "CSAT", "السؤال": col, "القيمة": calc_csat(df[col])})
overall_rows.append({"المؤشر": "CES", "السؤال": CES_COL, "القيمة": calc_ces(df[CES_COL])})
overall_rows.append({"المؤشر": "NPS", "السؤال": NPS_COL, "القيمة": calc_nps(df[NPS_COL])})

overall_df = pd.DataFrame(overall_rows)
print("=== المؤشرات العامة (كل سؤال لوحده) ===")
print(overall_df.to_string(index=False))


# ============================================================

services = df["F1"].dropna().unique()

per_service_rows = []
for service in services:
    sub = df[df["F1"] == service]
    row = {"اسم_الخدمة": service, "عدد_الاستجابات": len(sub)}
    for col in CSAT_COLS:
        row[f"CSAT_{col}"] = calc_csat(sub[col])
    row["CES_Q2"] = calc_ces(sub[CES_COL])
    row["NPS_Q8"] = calc_nps(sub[NPS_COL])
    per_service_rows.append(row)

per_service_df = pd.DataFrame(per_service_rows)

print("\n=== المؤشرات لكل خدمة (كل سؤال لوحده) ===")
print(per_service_df.to_string(index=False))


# ============================================================

with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
    overall_df.to_excel(writer, sheet_name="عام", index=False)
    per_service_df.to_excel(writer, sheet_name="لكل خدمة", index=False)

print(f"\nتم حفظ النتائج في: {OUTPUT_FILE}")