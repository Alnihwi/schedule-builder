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
        filter = file.loc[file["Course"].isin(subject)]
        groups = filter.groupby(["Course", "Group", "Type"])
        dic_lecture = {}
        dic_lab = {}

        for (course, group_id, typ), group in groups:
            session = []

            for _, row in group.iterrows():
                session.append((
                    row["Course"],
                    row["Group"],
                    row["Day"],
                    row["Start Time"],
                    row["End Time"], 
                    row["Professor"],
                    row["Room"],
                    row["Type"]
                ))

            if typ == "نظري":
                dic_lecture.setdefault(course, []).append(session)
            elif typ == "عملي":
                dic_lab.setdefault(course, []).append(session)

        all = []

        for course in subject:

            lecture_groups = dic_lecture[course]

            if course in dic_lab:
                combined = []
                lab_groubs = dic_lab[course]

                for lec in lecture_groups:
                    for lab in lab_groubs:
                        combined.append(lec + lab)
                all.append(combined)
            else:
                all.append(lecture_groups)


        comp = list(product(*all))

        def is_conflict(start1, end1, start2, end2):
            return not (end1 <= start2 or end2 <= start1)

        final = []
        for combo in comp:
            flat = [item for group in combo for item in group]
            conflict = False
            for i in range(len(flat)):
                for j in range(i + 1, len(flat)):
                    s1, e1 = flat[i][3], flat[i][4]
                    s2, e2 = flat[j][3], flat[j][4]
                    if flat[i][2] == flat[j][2] and is_conflict(s1, e1, s2, e2):
                        conflict = True
                        break
                if conflict:
                    break
            if not conflict:
                final.append(flat)

        st.success(f"✅ تم العثور على {len(final)} جدول بدون تعارض.")

        if final:
            for idx, schedule in enumerate(final):
                st.subheader(f"📅 الجدول رقم {idx + 1}")
                df_schedule = pd.DataFrame(schedule, columns=["Course", "Group", "Day", "Start Time", "End Time", "Professor", "Room", "Type"])

                
                st.dataframe(df_schedule, use_container_width=True)

