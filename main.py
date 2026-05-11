import streamlit as st
import pandas as pd

st.set_page_config(page_title="Сканер за Вредни Вещества", layout="centered")
st.title("🔍 Продуктов Сканер")
st.subheader("Въведи баркод или код на продукт")

barcode = st.text_input("Баркод / EAN / Код:", placeholder="Например: 1234567890123")

if st.button("Сканирай продукт", type="primary"):
    if not barcode:
        st.error("Моля въведи баркод!")
    else:
        mock_db = {
            "1234567890123": {
                "name": "Шоколад Милка",
                "ingredients": ["Палмово масло", "Захар", "Лецитин", "Ванилин"],
                "harmful": ["Палмово масло (екологично вредно)", "Захар (високо съдържание)"]
            },
            "9876543210987": {
                "name": "Чипс Lays",
                "ingredients": ["Картофи", "Слънчогледово олио", "Глутамат"],
                "harmful": ["Глутамат (E621)", "Акролеин при прегряване"]
            },
            "1112223334445": {
                "name": "Шампоан Head & Shoulders",
                "ingredients": ["Sodium Laureth Sulfate", "Paraben", "Fragrance"],
                "harmful": ["Sodium Laureth Sulfate", "Parabens"]
            }
        }
        
        product = mock_db.get(barcode, None)
        
        if product:
            st.success(f"Намерен продукт: **{product['name']}**")
            st.write("**Състав:**")
            for ing in product["ingredients"]:
                st.write(f"- {ing}")
            
            if product["harmful"]:
                st.error("⚠️ Открити вредни / нежелани вещества:")
                for harm in product["harmful"]:
                    st.write(f"❌ {harm}")
            else:
                st.success("Не са открити вредни вещества.")
        else:
            st.warning("Продуктът не е намерен в базата. Моля опитай друг баркод.")

st.divider()
st.caption("Демо приложение за учебна цел - GitHub домашно")
