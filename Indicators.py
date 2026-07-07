import pandas as pd

# 1. قراءة ملف الإكسل (تأكدي أن الملف في نفس مسار الكود)
file_name = 'data_cleaned.xlsx'
df = pd.read_excel(file_name)

# 2. تحديد اسم العمود
col_name = 'تقييم_1'

# 3. التأكد من تحويل البيانات إلى أرقام (لتجنب مشكلة قراءتها كنصوص)
df[col_name] = pd.to_numeric(df[col_name], errors='coerce')

# 4. حساب إجمالي التقييمات (مع تجاهل الخلايا الفارغة NaN)
total_reviews = df[col_name].count()

# 5. حساب عدد التقييمات الإيجابية (التي تساوي 4 أو 5)
positive_reviews = df[df[col_name] >= 4][col_name].count()

# 6. حساب وطباعة النتيجة
if total_reviews > 0:
    csat_score = (positive_reviews / total_reviews) * 100

    print("-" * 30)
    print(f"إجمالي التقييمات: {total_reviews}")
    print(f"التقييمات الإيجابية (4 و 5): {positive_reviews}")
    print(f"مؤشر رضا العملاء (CSAT): {csat_score:.1f}%")
    print("-" * 30)
else:
    print("لم يتم العثور على تقييمات صالحة في هذا العمود.")