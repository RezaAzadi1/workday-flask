from flask import Flask, render_template, request
import jdatetime

app = Flask(__name__)

# ----------------------------
# تعطیلات رسمی سال ۱۴۰۳
# ----------------------------
holidays = [
    "14031122","14031125", "14031229", "14040102", "14040103","14040104","14040111","14040112", "14040113","1404314","14040324",
    "14040414","14040415", "14040602","14040610","14040619","14040903", "14041013", "14041027","14041115","14041122","14041220",
    "14050101","14050102","14050103","14050104","14050112","14050125","14050513","14050521","14050609","14050823","14051002",
    "14051104","14051210","14051219","14051229"
]

# ----------------------------
# توابع محاسبه
# ----------------------------
def is_working_day(date):
    """آیا روز کاری است؟"""
    if date.strftime("%Y%m%d") in holidays or date.weekday() in [4, 5]:
        return False
    return True

def add_working_days(start_date, days_to_add):
    """افزودن روزهای کاری به تاریخ شروع"""
    current_date = start_date
    added_days = 0
    # اگر تاریخ شروع تعطیل است، برو روز بعد
    while not is_working_day(current_date):
        current_date += jdatetime.timedelta(days=1)
    while added_days < days_to_add:
        current_date += jdatetime.timedelta(days=1)
        if is_working_day(current_date):
            added_days += 1
    return current_date

def get_formatted_date(date):
    """فرمت خروجی"""
    return date.strftime("%Y/%m/%d")

# ----------------------------
# مسیر صفحه اصلی
# ----------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        start_input = request.form.get("start_date")
        days_to_add = request.form.get("days_to_add")
        if start_input and days_to_add:
            try:
                start_date = jdatetime.datetime.strptime(start_input.replace("-", ""), "%Y%m%d")
                days_to_add = int(days_to_add)
                end_date = add_working_days(start_date, days_to_add)
                result = f"تاریخ نهایی پس از {days_to_add} روز کاری: {get_formatted_date(end_date)}"
            except Exception as e:
                result = f"خطا در ورودی: {e}"
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
