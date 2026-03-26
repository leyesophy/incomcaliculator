import streamlit as st

# 画面設定：スマホで見やすい幅に調整
st.set_page_config(page_title="年収シミュレーター", layout="centered")

# カスタムCSS：金額を大きく、太く、青く表示するための魔法
st.markdown("""
    <style>
    .big-font {
        font-size:40px !important;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .unit {
        font-size: 20px;
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💰 プロ仕様・年収シミュレーター")
st.caption("給与明細や源泉徴収票から今年の総収入を予測")

# タブ切り替え
tab1, tab2 = st.tabs(["📄 給与明細3ヶ月から", "🏢 中途入社・合算"])

with tab1:
    st.subheader("直近3ヶ月の給与（額面）")
    # 入力しやすいように数値入力(number_input)に戻し、カンマ表示設定に
    m1 = st.number_input("1ヶ月目", value=250000, step=1000, format="%d")
    m2 = st.number_input("2ヶ月目", value=250000, step=1000, format="%d")
    m3 = st.number_input("3ヶ月目", value=250000, step=1000, format="%d")
    
    st.subheader("ボーナス")
    bonus = st.number_input("年間ボーナス合計（予定）", value=0, step=10000, format="%d")
    
    # 計算処理
    avg = (m1 + m2 + m3) / 3
    annual_total = (avg * 12) + bonus
    
    st.divider()
    st.write("### 推定年収（計算結果）")
    # ②文字を大きく表示（HTMLカスタムクラスを使用）
    st.markdown(f'<div class="big-font">{annual_total:,.0f} <span class="unit">円</span></div>', unsafe_allow_html=True)
    st.info(f"月平均 {avg:,.0f}円 × 12ヶ月 ＋ ボーナス {bonus:,}円")

with tab2:
    st.subheader("③ 中途入社・源泉徴収合算")
    st.write("「前職の源泉徴収票」と「今の会社の給与」を足します。")
    
    # 前職
    prev_income = st.number_input("前職の源泉徴収票「支払金額」", value=0, step=1000, format="%d")
    
    st.divider()
    
    # 現職
    curr_monthly = st.number_input("今の会社の月給（額面）", value=0, step=1000, format="%d")
    months_count = st.number_input("年内の支給回数（あと何回給料があるか）", value=1, min_value=1, max_value=12)
    curr_bonus = st.number_input("今の会社での年内ボーナス予定", value=0, step=10000, format="%d")
    
    # 合計計算
    total_result = prev_income + (curr_monthly * months_count) + curr_bonus
    
    st.divider()
    st.write("### 今年の合計推定年収")
    st.markdown(f'<div class="big-font">{total_result:,.0f} <span class="unit">円</span></div>', unsafe_allow_html=True)
    
    # 内訳をわかりやすく
    col1, col2 = st.columns(2)
    col1.metric("前職分", f"{prev_income:,}円")
    col2.metric("現職分（見込）", f"{(curr_monthly * months_count) + curr_bonus:,}円")

st.caption("※金額はすべて「額面（税引前）」で入力・計算してください。")
