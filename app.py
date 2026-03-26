import streamlit as st

st.title("💰 年収推計シミュレーター")

# 入力しやすくするための工夫
m1_str = st.text_input("1ヶ月目の総支給額（例: 250000）", value="250000")
m2_str = st.text_input("2ヶ月目の総支給額", value="250000")
m3_str = st.text_input("3ヶ月目の総支給額", value="250000")

bonus_str = st.text_input("年間ボーナス予定（合計）", value="0")

if st.button("年収を計算する"):
    try:
        # 文字を数字に変換して計算
        m1 = float(m1_str)
        m2 = float(m2_str)
        m3 = float(m3_str)
        bonus = float(bonus_str)
        
        avg = (m1 + m2 + m3) / 3
        annual = (avg * 12) + bonus
        
        st.balloons()
        st.success(f"推定年収： {annual:,.0f} 円")
    except ValueError:
        st.error("数字だけを入力してください（カンマなどは不要です）")
