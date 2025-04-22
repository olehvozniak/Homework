
import streamlit as st

st.set_page_config(page_title="Інтерполяційний турнір", layout="wide")

st.title("🎓 Інтерполяційний турнір")

st.markdown("""
Вітаємо в турнірі з інтерполяції!  
Обирайте вкладку зліва, щоб:
- 👥 **Створити турнір**
- ⚔️ **Провести бій**
- 📊 **Переглянути сітку**
""")

if selected_page == "🏆 Учасники":
    st.switch_page("pages/Учасники.py")

if selected_page == "⚔️ Змагання":
    st.switch_page("pages/Змагання.py")
