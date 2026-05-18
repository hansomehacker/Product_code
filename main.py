import streamlit as st
from PIL import Image
import pytesseract
import re
import pandas as pd

st.set_page_config(page_title="Сканер за Вредни Е-та", layout="wide")
st.title("📸 Сканер за Вредни Добавки в Продукти")

# --- Sidebar ---
st.sidebar.header("Как работи")
st.sidebar.info(
    "Качваш снимка на етикета → приложението чете текста с OCR → "
    "търси вредни добавки и E-номера."
)

# Разширена база данни
harmful_db = {
    "Захар / Сиропи": ["захар", "захароза", "глюкозо-фруктозен сироп", "фруктоза", "глюкоза"],
    "Палмово масло": ["палмово масло", "палмова мазнина", "palm oil"],
    "Натриев нитрит": ["e250", "натриев нитрит"],
    "Аспартам": ["e951", "аспартам"],
    "Натриев бензоат": ["e211", "бензоат"],
    "Мононатриев глутамат": ["e621", "глутамат"],
    "Транс мазнини": ["частично хидрогенирани", "trans fat"],
    "Изкуствени оцветители": ["e129", "allura red", "e102", "e110", "e124", "e133"],
    "Консерванти": ["e202", "e211", "e221", "e223"],
    "Други вредни": ["e320", "e321", "e407", "e621", "e951"]
}

# --- Основна част ---
option = st.radio("Избери начин на въвеждане:", ["Камера / Качване на снимка", "Ръчно въвеждане на текст"])

if option == "Камера / Качване на снимка":
    uploaded_file = st.camera_input("Направи снимка на етикета") or st.file_uploader("Или качи снимка", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Снимка на продукта", use_column_width=True)
        
        with st.spinner("Чета текста от етикета..."):
            # OCR
            text = pytesseract.image_to_string(image, lang='bul')  # bul за български
            cleaned_text = re.sub(r'\s+', ' ', text).strip().lower()
            
            st.subheader("Разпознат текст:")
            st.text_area("", cleaned_text, height=150)

else:  # Ръчно въвеждане
    product_input = st.text_area("Въведи съставки или име на продукт:")
    cleaned_text = product_input.lower() if product_input else ""

# --- Анализ ---
if st.button("🔍 Анализирай за вредни вещества", type="primary"):
    if not cleaned_text:
        st.warning("Моля въведи текст или качи снимка.")
    else:
        detected = []
        
        for category, terms in harmful_db.items():
            for term in terms:
                if term in cleaned_text:
                    detected.append((category, term))
        
        # Премахваме дубликати
        detected = list(dict.fromkeys(detected))
        
        if detected:
            st.error("⚠️ Намерени са потенциално вредни добавки!")
            df = pd.DataFrame(detected, columns=["Категория", "Открит термин"])
            st.dataframe(df, use_container_width=True)
            
            st.subheader("Препоръки:")
            st.markdown("""
            - Избягвай честа консумация на този продукт
            - Търси алтернативи без тези добавки
            - Винаги проверявай пълния списък на съставките
            """)
        else:
            st.success("✅ Не са открити вредни вещества от базата данни.")
            st.info("Добър избор! Въпреки това винаги чети етикета внимателно.")


st.caption("Демо приложение")
