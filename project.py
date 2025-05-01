import pandas as pd
import streamlit as st
from itertools import product
from datetime import datetime

st.set_page_config(page_title="منشئ جدول المحاضرات", layout="wide")

st.title("📚 جدول المحاضرات للطلبة")

file = pd.read_excel("final_project.xlsx")

file["Start Time"] = file["Start Time"].map(lambda x: datetime.strptime(x, "%H:%M").time())
file["End Time"] = file["End Time"].map(lambda x: datetime.strptime(x, "%H:%M").time())



unique = file["Course"].unique()
subject = st.multiselect("اختر المواد التي تريد جدولها:", unique)

if st.button("🔍 إنشاء الجداول الممكنة"):
    if not subject:
        st.warning("يرجى اختيار مادة واحدة على الأقل.")
    else:
        # تصفية المواد المختارة
        filter = file.loc[file["Course"].isin(subject)]
        groups = filter.groupby("Course")
        dic = {}

        for course, group in groups:
            dic[course] = list(zip(
                group["Course"],
                group["Group"],
                group["Day"],
                group["Start Time"],
                group["End Time"],
                group["Professor"],
                group["Room"]
            ))

        all_values = list(dic.values())
        comp = list(product(*all_values))

        def is_conflict(start1, end1, start2, end2):
            return not (end1 <= start2 or end2 <= start1)

        final = []
        for i in comp:
            conflict = False
            for j in range(len(i)):
                for k in range(j + 1, len(i)):
                    start1, end1 = i[j][3], i[j][4]
                    start2, end2 = i[k][3], i[k][4]
                    if is_conflict(start1, end1, start2, end2):
                        conflict = True
                        break
                if conflict:
                    break
            if not conflict:
                final.append(i)

        st.success(f"تم العثور على {len(final)} جدول صالح بدون تعارض.")

        if final:
            for idx, schedule in enumerate(final):
                st.subheader(f"📅 الجدول رقم {idx + 1}")
                df_schedule = pd.DataFrame(schedule, columns=["Course", "Group", "Day", "Start Time", "End Time", "Professor", "Room"])
                st.dataframe(df_schedule, use_container_width=True)


# import pandas as pd
# import streamlit as st
# from itertools import product
# from datetime import datetime



# file = pd.read_excel("final_project.xlsx")

# file["Start Time"] = file["Start Time"].map(lambda x: datetime.strptime(x, "%H:%M").time())
# file["End Time"] = file["End Time"].map(lambda x: datetime.strptime(x, "%H:%M").time())



# subject = []
# unique = file["Course"].unique()

# n = int(input("how many subject do you want: "))

# for i in range(n):
#     put = input("enter the subject name: ")
#     while put not in unique:
#         print("wrong name ...")
#         put = input("enter the subject name again: ")
#     subject.append(put)



# filter = file.loc[file["Course"].isin(subject)]
# groups = filter.groupby("Course")
# dic = {}


# for course, group in groups:
#     dic[course] = list(zip(
#         group["Course"],
#         group["Group"],
#         group["Day"],
#         group["Start Time"],
#         group["End Time"],
#         group["Professor"],
#         group["Room"]
#     ))

# all_values = list(dic.values())

# comp = list(product(*all_values))

# def is_conflict(start1, end1, start2, end2):
#     return not (end1 <= start2 or end2 <= start1)


# final = []
# for i in comp:
#     conflict = False
    
#     for j in range(len(i)):
#         for k in range(j+1, len(i)):
#             start1, end1 = i[j][3], i[j][4]
#             start2, end2 = i[k][3], i[k][4]
            
#             if is_conflict(start1, end1, start2, end2):
#                 conflict = True
#                 break
#         if conflict:
#             break
#     if not conflict:
#         final.append(i)


# colum = ["Course", "Group", "Day", "Start Time", "End Time", "Professor", "Room"]

# for idx, schedule in enumerate(final):
#     print(f"Schedule #{idx + 1}")
#     df_schedule = pd.DataFrame(schedule, columns=colum)
#     print(df_schedule)
#     print("-" * 50)