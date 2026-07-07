import pandas as pd
import numpy as np
import re


INPUT_FILE = "data_labeled.xlsx"
OUTPUT_FILE = "data_cleaned.xlsx"

# Row 1 contains the question text, row 2 contains the actual column names (responseId, DATE, ...)
# header=1 makes the second row the header row used in df
df = pd.read_excel(INPUT_FILE, header=1)

print("Row count before cleaning:", len(df))
print("Column count before cleaning:", len(df.columns))

df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")

stringDate = df["DATE"].dt.strftime("%Y-%m-%d")

df["start_time_full"] = pd.to_datetime(
    stringDate + " " + df["IS"].astype(str),
    format="%Y-%m-%d %I:%M %p", errors="coerce"
)
df["end_time_full"] = pd.to_datetime(
    stringDate + " " + df["IE"].astype(str),
    format="%Y-%m-%d %I:%M %p", errors="coerce"
)

df["survey_duration_minutes"] = (
    df["end_time_full"] - df["start_time_full"]
).dt.total_seconds() / 60

df["IN"] = df["IN"].astype(str).str.strip()
df.loc[df["IN"].isin(["nan", "None", ""]), "IN"] = np.nan

df["F1"] = df["F1"].astype(str).str.strip()
df.loc[df["F1"].isin(["nan", "None", ""]), "F1"] = np.nan


rating_cols = [
    "Q1", "Q2", "Q3", "Q3b", "Q3c",
    "Q3d", "Q5b", "Q5c", "Q8",
]

for col in rating_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")
    df.loc[df[col] == 99, col] = np.nan  # 99 (not applicable) becomes empty instead of an actual rating

comment_cols = [
    "Q1A", "Q2A", "Q3.1",
    "Q3b.1", "Q3c.1", "Q3d.1",
    "Q5b.1", "Q5c.1", "Q8.1",
]

# All the different variants that mean "no comment", after trimming extra spaces
noComment = {".", "لايوجد", "لابوجد", "لا يوجد", "لا يوجد.", "لايوجد."}


def unifyNoComment(text):
    if pd.isna(text):
        return text

    cleanedText = str(text).strip()
    cleanedText = cleanedText.strip('"').strip()   # remove stray quotation marks at the edges only
    cleanedText = re.sub(r"\s+", " ", cleanedText)  # collapse repeated spaces into a single space

    if cleanedText in noComment:
        return "No comment"

    return cleanedText


for col in comment_cols:
    df[col] = df[col].apply(unifyNoComment)


reason_cols = [
    "primary_reason_Sat", "secondary_reason_Sat",
    "primary_reason_Rec", "secondary_reason_Rec",
]

for col in reason_cols:
    df[col] = df[col].astype(str).str.strip()
    df.loc[df[col].isin(["nan", "None", ""]), col] = np.nan


df.to_excel(OUTPUT_FILE, index=False)

print("Row count after cleaning:", len(df))
print("Column count after cleaning:", len(df.columns))
print("Cleaned file saved to:", OUTPUT_FILE)