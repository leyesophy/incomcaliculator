import streamlit as st
from datetime import date

# 画面設定
st.set_page_config(page_title="推計年収シミュレーター", layout="centered")

# カスタムCSS
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
    input { font-size: 20px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("💰 推計年収シミュレーター")

tab1, tab2 = st.tabs(["📄 給与明細3ヶ月分から", "📑 現職の源泉徴収票から予測"])

with tab1:
    st.subheader("直近3ヶ月の給与（額面）から予測")
    m1 = st.number_input("1ヶ月目の給与", value=None, placeholder="金額を入力", step=1000, format="%d", key="t1_m1")
    m2 = st.number_input("2ヶ月目の給与", value=None, placeholder="金額を入力", step=1000, format="%d", key="t1_m2")
    m3 = st.number_input("3ヶ月目の給与", value=None, placeholder="金額を入力", step=1000, format="%d", key="t1_m3")
    bonus = st.number_input("年間ボーナス合計（予定）", value=None, placeholder="0", step=10000, format="%d", key="t1_b1")
    
    if m1 and m2 and m3:
        val_bonus = bonus if bonus else 0
        avg = (m1 + m2 + m3) / 3
        annual_total = (avg * 12) + val_bonus
        st.write("### 推計年収（予測）")
        st.markdown(f'<div class="big-font">{annual_total:,.0f} <span class="unit">円</span></div>', unsafe_allow_html=True)

with tab2:
    st.subheader("📑 現職のみの推計年収（中途入社対応）")
    st.info("現職の源泉徴収票に記載された「これまでの実績」から、今の会社での年収を予測します。")

    # 入社日の入力
    hire_date = st.date_input("現職の入社日", value=date.today(), format="YYYY/MM/DD")
    
    # 現職の源泉徴収票に記載された「支払金額」（現職分のみ）
    current_pay = st.number_input("① 源泉徴収票の「支払金額」（現職分）", value=None, placeholder="現職でのこれまでの合計額", step=1000, format="%d", key="t2_curr")

    st.divider()
    
    st.write("#### ② 年末までの追加支給分（見込）")
    st.caption(f"{hire_date.month}月入社の場合の、今後の収入を予測します。")
    
    col1, col2 = st.columns(2)
    with col1:
        future_m = st.number_input("今後の月給（額面）", value=None, placeholder="1ヶ月分", step=1000, format="%d", key="t2_f_m")
    with col2:
        # 入社月から逆算した、年内の残り回数のデフォルトを提示
        default_count = 12 - date.today().month + 1 if date.today().year == hire_date.year else 0
        future_c = st.number_input("残り支給回数", value=default_count, min_value=0, max_value=12, step=1, key="t2_f_c")
    
    future_b = st.number_input("今後のボーナス予定（額面）", value=None, placeholder="0", step=10000, format="%d", key="t2_f_b")

    # 計算
    if current_pay is not None:
        val_curr = current_pay
        val_fm = future_m if future_m else 0
        val_fc = future_c if future_c else 0
        val_fb = future_b if future_b else 0
        
        # 今回の仕様：前職分は含まず、現職の源泉徴収票の額 ＋ 今後の見込
        total_income = val_curr + (val_fm * val_fc) + val_fb
        
        st.write("### 今の会社での着地推計（現職のみ）")
        st.markdown(f'<div class="big-font">{total_income:,.0f} <span class="unit">円</span></div>', unsafe_allow_html=True)
        
        # 状況の解説
        st.info(f"💡 {hire_date.year}年度は、これまでの実績 {val_curr:,}円 に、今後見込分を加算して計算しています。")
    else:
        st.info("源泉徴収票の「支払金額」を入力してください。")

st.caption("※前職の収入額は含まず、現職での総収入（額面）を計算しています。")
