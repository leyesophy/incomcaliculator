import streamlit as st
from datetime import date

# 画面設定
st.set_page_config(page_title="推計年収シミュレーター", layout="centered")

# カスタムCSS：金額を大きく表示
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
    /* 入力欄のカンマ表示を補助するスタイル */
    input { font-size: 18px !important; }
    </style>
    """, unsafe_allow_html=True)

# ① アプリタイトルの修正
st.title("💰 推計年収シミュレーター")
st.caption("直近の給与や入社日から、今年の総収入を予測します")

tab1, tab2 = st.tabs(["📄 給与明細3ヶ月分から", "🏢 中途入社・源泉徴収合算"])

with tab1:
    st.subheader("直近3ヶ月の給与（額面）")
    # ② 入力時もカンマ区切りで見やすく設定 (format="%d" を使用)
    m1 = st.number_input("1ヶ月目の給与", value=250000, step=1000, format="%d", key="m1")
    m2 = st.number_input("2ヶ月目の給与", value=250000, step=1000, format="%d", key="m2")
    m3 = st.number_input("3ヶ月目の給与", value=250000, step=1000, format="%d", key="m3")
    
    st.subheader("ボーナス")
    bonus = st.number_input("年間ボーナス合計（予定）", value=0, step=10000, format="%d", key="b1")
    
    avg = (m1 + m2 + m3) / 3
    annual_total = (avg * 12) + bonus
    
    st.divider()
    st.write("### 推計年収（予測）")
    st.markdown(f'<div class="big-font">{annual_total:,.0f} <span class="unit">円</span></div>', unsafe_allow_html=True)
    st.info(f"月平均 {avg:,.0f}円 × 12ヶ月 ＋ ボーナス {bonus:,}円")

with tab2:
    st.subheader("③ 中途入社の推計計算")
    
    # 前職のデータ
    prev_income = st.number_input("前職の源泉徴収票「支払金額」", value=0, step=1000, format="%d", key="prev")
    
    st.divider()
    
    # 現職のデータ
    st.write("#### 現職（今の会社）の情報")
    hire_date = st.date_input("現職の入社日", value=date.today())
    curr_monthly = st.number_input("今の会社の月給（額面）", value=0, step=1000, format="%d", key="curr_m")
    curr_bonus = st.number_input("現職での年内ボーナス予定", value=0, step=10000, format="%d", key="curr_b")

    # 入社日から年内の支給回数を自動計算（入社月〜12月まで）
    # 例：10月入社なら、10, 11, 12月の3回と仮定
    remaining_months = 12 - hire_date.month + 1
    
    st.caption(f"💡 入社日が {hire_date.month}月 なので、年内の給与支給を {remaining_months}回 と計算しました。")

    # 合計計算
    current_company_total = (curr_monthly * remaining_months) + curr_bonus
    total_year_income = prev_income + current_company_total
    
    st.divider()
    st.write("### 今年の合計推計年収")
    st.markdown(f'<div class="big-font">{total_year_income:,.0f} <span class="unit">円</span></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    col1.metric("前職の支払金額", f"{prev_income:,}円")
    col2.metric("現職の推計（年内）", f"{current_company_total:,}円")

st.caption("※このシミュレーターは、入力された額面金額に基づいた単純計算です。")
