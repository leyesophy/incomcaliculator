import streamlit as st

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

tab1, tab2 = st.tabs(["📄 給与明細3ヶ月分から", "📑 現職の源泉徴収票から合算"])

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
    st.subheader("📑 源泉徴収票の項目を合算")
    st.info("源泉徴収票に記載されている「現職分」と「前職分」をそれぞれ入力してください。")

    # ① 現職の支払金額（メインの大きな枠）
    current_pay = st.number_input("① 現職の「支払金額」（メインの枠）", value=None, placeholder="源泉徴収票の大きな数字を入力", step=1000, format="%d", key="t2_curr")

    # ② 前職の支払金額（下部や摘要欄に記載されている分）
    previous_pay = st.number_input("② 前職の「支払金額」（下部に記載分）", value=None, placeholder="前職分の金額を入力", step=1000, format="%d", key="t2_prev")

    st.divider()
    
    st.write("#### ③ 年末までの残り支給分（追加見込）")
    st.caption("源泉徴収票の締め日以降に支払われる予定の金額です。")
    
    col1, col2 = st.columns(2)
    with col1:
        future_m = st.number_input("今後の月給（額面）", value=None, placeholder="1ヶ月分", step=1000, format="%d", key="t2_f_m")
    with col2:
        future_c = st.number_input("残り回数", value=0, min_value=0, max_value=12, step=1, key="t2_f_c")
    
    future_b = st.number_input("今後のボーナス予定（額面）", value=None, placeholder="0", step=10000, format="%d", key="t2_f_b")

    # 計算
    if current_pay is not None:
        val_curr = current_pay
        val_prev = previous_pay if previous_pay else 0
        val_fm = future_m if future_m else 0
        val_fc = future_c if future_c else 0
        val_fb = future_b if future_b else 0
        
        # 合計 = 現職(源泉票) + 前職(源泉票) + (月給 × 残り回数) + 今後のボーナス
        total_income = val_curr + val_prev + (val_fm * val_fc) + val_fb
        
        st.write("### 今年の最終着地（推計）")
        st.markdown(f'<div class="big-font">{total_income:,.0f} <span class="unit">円</span></div>', unsafe_allow_html=True)
        
        # わかりやすい内訳表示
        st.write("📊 **計算の内訳**")
        st.write(f"- 源泉徴収票（現職）: {val_curr:,}円")
        st.write(f"- 源泉徴収票（前職）: {val_prev:,}円")
        st.write(f"- 今後の支給予定: {(val_fm * val_fc) + val_fb:,}円")
    else:
        st.info("源泉徴収票の「支払金額」を入力してください。")

st.caption("※金額はすべて「額面（税引前）」で入力してください。")
