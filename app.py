import streamlit as st
import unicodedata

# 画面設定
st.set_page_config(page_title="推計年収シミュレーター", layout="centered")

# 【全般的な文字サイズアップ】CSS（維持）
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-size: 20px !important;
    }
    button[data-baseweb="tab"] div {
        font-size: 22px !important;
    }
    .stMarkdown p, label {
        font-size: 22px !important;
        font-weight: bold !important;
    }
    div[data-baseweb="input"] {
        font-size: 26px !important;
        height: 60px !important;
    }
    div[data-baseweb="select"] {
        font-size: 24px !important;
    }
    .result-box {
        font-size: 48px !important;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        background-color: #f0f2f6;
        padding: 30px;
        border-radius: 15px;
        margin: 15px 0;
        border: 2px solid #1E88E5;
    }
    .unit { font-size: 24px; color: #333; }
    .stCaption {
        font-size: 18px !important;
        line-height: 1.6;
    }
    /* クリアボタン専用スタイル */
    .stButton > button {
        width: 100% !important;
        height: 55px !important;
        font-size: 22px !important;
        color: #ff4b4b !important;
        border: 2px solid #ff4b4b !important;
        background-color: white !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# セッションクリア用の関数
def clear_inputs(keys):
    for key in keys:
        if key in st.session_state:
            st.session_state[key] = ""
    st.rerun()

# 金額入力をカンマ区切りにする補助関数
def comma_input(label, key):
    if key not in st.session_state:
        st.session_state[key] = ""

    raw_val = st.text_input(label, value=st.session_state[key], key=f"input_{key}", placeholder="例：3,000,000")

    normalized_val = unicodedata.normalize('NFKC', raw_val).replace(',', '').replace('円', '')
    
    if normalized_val.isdigit():
        number = int(normalized_val)
        formatted = f"{number:,}"
        if st.session_state[key] != formatted:
            st.session_state[key] = formatted
            st.rerun()
        return number
    elif normalized_val == "":
        st.session_state[key] = ""
        return None
    else:
        if raw_val != "":
            st.error("数字のみ入力してください")
        return None

st.title("💰 推計年収シミュレーター")
st.divider()

tab1, tab2 = st.tabs(["📄 給与明細", "📑 源泉徴収票"])

with tab1:
    st.write("### 直近3ヶ月の給与（額面）")
    m1 = comma_input("1ヶ月目", "t1_m1")
    m2 = comma_input("2ヶ月目", "t1_m2")
    m3 = comma_input("3ヶ月目", "t1_m3")
    
    st.write("### ボーナス実績")
    bonus = comma_input("年間合計", "t1_b")
    
    if m1 and m2 and m3:
        b_val = bonus if bonus else 0
        avg = (m1 + m2 + m3) / 3
        annual = (avg * 12) + b_val
        st.divider()
        st.write("### 💎 理論上の年収（予測）")
        st.markdown(f'<div class="result-box">{annual:,.0f} <span class="unit">円</span></div>', unsafe_allow_html=True)
        
        # クリアボタンの配置
        if st.button("🔄 入力内容をクリア", key="btn_clear_t1"):
            clear_inputs(["t1_m1", "t1_m2", "t1_m3", "t1_b"])

with tab2:
    st.write("### 源泉徴収票から年換算")
    st.caption("「もし1年間フルで在籍していたら」を逆算します。")

    pay_amount = comma_input("支払金額（現職分のみ）", "t2_pay")
    
    months_list = [f"{i}月" for i in range(1, 13)]
    start_month_str = st.selectbox("現職の入社月", options=months_list, index=7)
    start_month = int(start_month_str.replace('月', ''))

    if pay_amount:
        working_months = 12 - start_month + 1
        theoretical_annual = (pay_amount / working_months) * 12
        
        st.divider()
        st.write(f"### 💎 現職の推計年収")
        st.markdown(f'<div class="result-box">{theoretical_annual:,.0f} <span class="unit">円</span></div>', unsafe_allow_html=True)
        
        # クリアボタンの配置
        if st.button("🔄 入力内容をクリア", key="btn_clear_t2"):
            clear_inputs(["t2_pay"])
        
        st.info(f"💡 {start_month}月〜12月の実績（{working_months}ヶ月分）から、12ヶ月分を算出した理論値です。")

st.divider()
st.caption("※この数値は額面での推計です。")
