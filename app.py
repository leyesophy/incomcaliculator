import streamlit as st
from datetime import date
import locale

# 画面設定
st.set_page_config(page_title="推計年収シミュレーター", layout="centered")

# カスタムCSS（前回のまま）
st.markdown("""
    <style>
    .big-font {
        font-size:42px !important;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .unit { font-size: 20px; color: #333; }
    input { font-size: 18px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("💰 推計年収シミュレーター")

tab1, tab2 = st.tabs(["📄 給与明細3ヶ月分から", "🏢 中途入社・源泉徴収合算"])

# --- Tab 1 は変更なし ---
with tab1:
    st.subheader("直近3ヶ月の給与（額面）")
    m1 = st.number_input("1ヶ月目の給与", value=None, placeholder="金額を入力", step=1000, format="%d", key="m1")
    m2 = st.number_input("2ヶ月目の給与", value=None, placeholder="金額を入力", step=1000, format="%d", key="m2")
    m3 = st.number_input("3ヶ月目の給与", value=None, placeholder="金額を入力", step=1000, format="%d", key="m3")
    bonus = st.number_input("年間ボーナス合計（予定）", value=None, placeholder="0", step=10000, format="%d", key="b1")
    
    if m1 is not None and m2 is not None and m3 is not None:
        val_bonus = bonus if bonus is not None else 0
        avg = (m1 + m2 + m3) / 3
        annual_total = (avg * 12) + val_bonus
        st.write("### 推計年収（予測）")
        st.markdown(f'<div class="big-font">{annual_total:,.0f} <span class="unit">円</span></div>', unsafe_allow_html=True)

# --- Tab 2: カレンダー日本語化対応 ---
with tab2:
    st.subheader("🏢 中途入社の推計計算")
    prev_income = st.number_input("前職の源泉徴収票「支払金額」", value=None, placeholder="0", step=1000, format="%d", key="prev")
    
    st.divider()
    st.write("#### 現職（今の会社）の情報")
    
    # 修正ポイント：カレンダーの月名を日本語にするための設定
    # ※サーバー環境によっては locale が効かない場合があるため、表示形式を強制的に日本式にします
    hire_date = st.date_input(
        "現職の入社日", 
        value=date.today(),
        format="YYYY/MM/DD" # これで 2024/10/01 のような表示に固定されます
    )
    
    # 日本語の月名を表示するためのヒントを表示
    st.caption(f"📅 判定：**{hire_date.year}年 {hire_date.month}月** 入社")

    curr_monthly = st.number_input("今の会社の月給（額面）", value=None, placeholder="金額を入力", step=1000, format="%d", key="curr_m")
    curr_bonus = st.number_input("現職での年内ボーナス予定", value=None, placeholder="0", step=10000, format="%d", key="curr_b")

    remaining_months = 12 - hire_date.month + 1
    st.info(f"💡 年内の給与支給は残り **{remaining_months}回** です。")

    if curr_monthly is not None:
        val_prev = prev_income if prev_income is not None else 0
        val_curr_b = curr_bonus if curr_bonus is not None else 0
        current_company_total = (curr_monthly * remaining_months) + val_curr_b
        total_year_income = val_prev + current_company_total
        
        st.write("### 今年の合計推計年収")
        st.markdown(f'<div class="big-font">{total_year_income:,.0f} <span class="unit">円</span></div>', unsafe_allow_html=True)
