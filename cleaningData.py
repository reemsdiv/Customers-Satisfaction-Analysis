import pandas as pd
import numpy as np
import re

INPUT_FILE = "data_labeled.xlsx"
OUTPUT_FILE = "data_cleaned.xlsx"

df = pd.read_excel(INPUT_FILE)

print("عدد الصفوف قبل التنظيف:", len(df))
print("عدد الأعمدة قبل التنظيف:", len(df.columns))

rename_map = {
    "responseId": "رقم_الاستجابة",
    "DATE": "تاريخ_الاستجابة",
    "IS": "وقت_البداية",
    "IE": "وقت_النهاية",
    "IN": "اسم_الباحث",
    "F1": "اسم_الخدمة",

    "Q1": "تقييم_1",
    "Q1A": "تعليق_تقييم_1",
    "primary_reason_Sat": "السبب_الرئيسي_للرضا",
    "secondary_reason_Sat": "السبب_الثانوي_للرضا",

    "Q2": "تقييم_2",
    "Q2A": "تعليق_تقييم_2",

    "Q3": "تقييم_3",
    "Q3.1": "تعليق_تقييم_3",
    "Q3b": "تقييم_3ب",
    "Q3b.1": "تعليق_تقييم_3ب",
    "Q3c": "تقييم_3ج",
    "Q3c.1": "تعليق_تقييم_3ج",
    "Q3d": "تقييم_3د",
    "Q3d.1": "تعليق_تقييم_3د",

    "Q5b": "تقييم_5ب",
    "Q5b.1": "تعليق_تقييم_5ب",
    "Q5c": "تقييم_5ج",
    "Q5c.1": "تعليق_تقييم_5ج",

    "Q8": "تقييم_الترشيح_NPS",
    "Q8.1": "تعليق_الترشيح",
    "primary_reason_Rec": "السبب_الرئيسي_للترشيح",
    "secondary_reason_Rec": "السبب_الثانوي_للترشيح",

}

df = df.rename(columns=rename_map)

df["تاريخ_الاستجابة"] = pd.to_datetime(df["تاريخ_الاستجابة"], errors="coerce")

stringDate = df["تاريخ_الاستجابة"].dt.strftime("%Y-%m-%d")

df["وقت_البداية_الكامل"] = pd.to_datetime(
    stringDate + " " + df["وقت_البداية"].astype(str),
    format="%Y-%m-%d %I:%M %p", errors="coerce"
)
df["وقت_النهاية_الكامل"] = pd.to_datetime(
    stringDate + " " + df["وقت_النهاية"].astype(str),
    format="%Y-%m-%d %I:%M %p", errors="coerce"
)

df["مدة_الاستبيان_بالدقائق"] = (
    df["وقت_النهاية_الكامل"] - df["وقت_البداية_الكامل"]
).dt.total_seconds() / 60

df["اسم_الباحث"] = df["اسم_الباحث"].astype(str).str.strip()
df.loc[df["اسم_الباحث"].isin(["nan", "None", ""]), "اسم_الباحث"] = np.nan

df["اسم_الخدمة"] = df["اسم_الخدمة"].astype(str).str.strip()
df.loc[df["اسم_الخدمة"].isin(["nan", "None", ""]), "اسم_الخدمة"] = np.nan


rating_cols = [
    "تقييم_1", "تقييم_2", "تقييم_3", "تقييم_3ب", "تقييم_3ج",
    "تقييم_3د", "تقييم_5ب", "تقييم_5ج", "تقييم_الترشيح_NPS",
]

for col in rating_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")
    df.loc[df[col] == 99, col] = np.nan  # 99 (غير منطبق) تصير فاضية بدل تقييم فعلي

comment_cols = [
    "تعليق_تقييم_1", "تعليق_تقييم_2", "تعليق_تقييم_3",
    "تعليق_تقييم_3ب", "تعليق_تقييم_3ج", "تعليق_تقييم_3د",
    "تعليق_تقييم_5ب", "تعليق_تقييم_5ج", "تعليق_الترشيح",
]

# كل الصيغ المختلفة التي تعني "لا يوجد تعليق" بعد إزالة المسافات الزائدة
noComment = {".", "لايوجد", "لابوجد", "لا يوجد", "لا يوجد.", "لايوجد."}


def unifyNoComment(text):
    if pd.isna(text):
        return text

    cleanedText = str(text).strip()
    cleanedText = cleanedText.strip('"').strip()   # إزالة علامات اقتباس زائدة بالأطراف فقط
    cleanedText = re.sub(r"\s+", " ", cleanedText)  # توحيد المسافات المتكررة إلى مسافة واحدة

    if cleanedText in noComment:
        return "لا يوجد تعليق"

    return cleanedText


for col in comment_cols:
    df[col] = df[col].apply(unifyNoComment)


reason_cols = [
    "السبب_الرئيسي_للرضا", "السبب_الثانوي_للرضا",
    "السبب_الرئيسي_للترشيح", "السبب_الثانوي_للترشيح",
]

for col in reason_cols:
    df[col] = df[col].astype(str).str.strip()
    df.loc[df[col].isin(["nan", "None", ""]), col] = np.nan


df.to_excel(OUTPUT_FILE, index=False)

print("عدد الصفوف بعد التنظيف:", len(df))
print("عدد الأعمدة بعد التنظيف:", len(df.columns))
print("تم حفظ الملف النظيف في:", OUTPUT_FILE)