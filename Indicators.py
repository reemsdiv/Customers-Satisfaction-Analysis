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



# 2. تحديد اسم عمود الـ NPS
col_name = 'تقييم_الترشيح_NPS'

# التأكد من تحويل البيانات إلى أرقام لتجنب أي أخطاء نصية
df[col_name] = pd.to_numeric(df[col_name], errors='coerce')

# 3. استخراج القيم الأساسية
# إجمالي التقييمات الصالحة
total_responses = df[col_name].count()

# عدد المروجين (9 و 10)
promoters = df[df[col_name] >= 9][col_name].count()

# عدد المنتقدين (من 0 إلى 6)
detractors = df[df[col_name] <= 6][col_name].count()

# 4. حساب النسبة المئوية للمروجين والمنتقدين
if total_responses > 0:
    promoters_percent = (promoters / total_responses) * 100
    detractors_percent = (detractors / total_responses) * 100

    # حساب النتيجة النهائية لمؤشر NPS
    nps_score = promoters_percent - detractors_percent

    # 5. طباعة النتائج بشكل مرتب
    print("-" * 40)
    print(f"إجمالي التقييمات: {total_responses}")
    print(f"عدد المروجين (9-10): {promoters} (%.1f%%)" % promoters_percent)
    print(f"عدد المنتقدين (0-6): {detractors} (%.1f%%)" % detractors_percent)
    print("-" * 40)
    print(f"مؤشر صافي نقاط الترويج (NPS) = {nps_score:.1f}")
    print("-" * 40)
else:
    print("لم يتم العثور على تقييمات صالحة في هذا العمود.")