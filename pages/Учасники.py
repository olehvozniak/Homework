
import streamlit as st
import random

st.set_page_config(page_title="Учасники", layout="wide")
st.title("Створення турніру")

num_students = st.number_input("Кількість учасників (парна)", min_value=2, max_value=32, step=2, value=8)

if "all_students" not in st.session_state:
    st.session_state.all_students = []

st.markdown("### Введіть імена студентів:")

students = []
for i in range(num_students):
    name = st.text_input(f"Студент {i+1}", value=f"Студент {i+1}", key=f"name_{i}")
    students.append(name)

if st.button("🎲 Створити турнірну сітку"):
    st.session_state.all_students = students.copy()
    random.shuffle(st.session_state.all_students)
    st.session_state.round = 1
    st.session_state.matches = []
    st.session_state.winners = []
    st.session_state.pair_index = 0

    matches = []
    for i in range(0, len(st.session_state.all_students), 2):
        matches.append((st.session_state.all_students[i], st.session_state.all_students[i+1]))
    st.session_state.matches = matches

# Показ пар
if "matches" in st.session_state:
    st.markdown(f"## Раунд {st.session_state.round}")
    for i, match in enumerate(st.session_state.matches):
        st.write(f"🎯 Пара {i+1}: **{match[0]}** vs **{match[1]}**")

    st.markdown("---")
    if st.button("➡️ Почати перший поєдинок"):
        st.switch_page("pages/Змагання.py")
