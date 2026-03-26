import streamlit as st
import unicodedata

# 画面設定
st.set_page_config(page_title="推計年収シミュレーター", layout="centered")

# CSS設定（文字サイズ等は維持）
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 20px !important; }
    button[data-baseweb="tab"] div { font-size: 22px !important; }
    .stMarkdown p, label { font-size: 22px !important; font-weight: bold !important; }
    div[data-baseweb="input"] { font-size: 26px !important; height: 60px !important; }
    div[data-baseweb="select"] { font-size: 24px !important; }
    .result-box {
        font-size: 48px !important; font-weight: bold; color: #1E88E5;
        text-align: center; background-color: #f0f2f6; padding: 30px;
        border-radius: 15px; margin: 15px 0; border: 2px solid #1E88E5;
    }
    .unit { font-size: 24px; color: #333; }
    .stCaption { font-size: 18px !important; line-height: 1.6; }
    .stButton > button {
        width: 100% !important; height: 55px !important; font-size: 20px !important;
        color: #ff4b4b !important; border: 2px solid #ff4b4b !important;
        background-color: white !important; border-radius: 10px !important;
        margin-bottom: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 確実なクリアのためのロジック ---
# クリアボタンが押されるたびにこの数値をカウントアップし、入力欄のIDを新しくします
if "clear_count" not in st.session_state:
    st.session_state.clear_count = 0

def clear_all():
    # セッション内の入力データを消去
    for key in list(st.session_state.keys()):
        if key.startswith("data_"):
            st.session_state[key] = ""
    # カウントを増やすことで、入力欄（widget）を「新品」に交換する
    st.session_state.clear_count += 1
    st.rerun()

# 金額入力関数（改良版）
def comma_input(label, key):
    data_key = f"data_{key}"
    # クリアボタンで新しくなったIDを生成
    widget_key = f"widget_{key}_{st.session_state.clear_count}"
    
    if data_key not in st.session_state:
        st.session_state[data_key] = ""

    # valueにはセッションの値を、keyにはクリアのたびに変わる一意のIDを指定
    raw_val = st.text_input(label, value=st.session_state[data_key], key=widget_key, placeholder="0")
    
    normalized_val = unicodedata.normalize('NFKC', raw_val).replace(',', '').replace('円', '')
    
    if normalized_val.isdigit():
        number = int(normalized_val)
        formatted = f"{number:,}"
        if st.session_state[data_key] != formatted:
            st.session_state[data_key] = formatted
            st.rerun()
        return number
    elif normalized_val == "":
        st.session_state[data_key] = ""
        return None
    return None

st.title("💰 推計年収シミュレーター")
st.divider()

tab1, tab2 = st.tabs(["📄 給与明細", "📑 源泉徴収票"])

with tab1:
    if st.button("🔄 入力内容をすべてクリア", key="btn_clear_t1"):
        clear_all()
    
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

with tab2:
    if st.button("🔄 入力内容をすべてクリア", key="btn_clear_t2"):
        clear_all()
        
    st.write("### 源泉徴収票から年換算")
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
