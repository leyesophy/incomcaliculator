import streamlit as st

# 画面設定
st.set_page_config(page_title="推計年収シミュレーター", layout="centered")

# CSS設定（文字サイズ等は維持）
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 20px !important; }
    button[data-baseweb="tab"] div { font-size: 22px !important; }
    .stMarkdown p, label { font-size: 22px !important; font-weight: bold !important; }
    
    /* number_inputのサイズ調整 */
    div[data-baseweb="input"] {
        font-size: 26px !important;
        height: 60px !important;
    }
    
    .result-box {
        font-size: 48px !important; font-weight: bold; color: #1E88E5;
        text-align: center; background-color: #f0f2f6; padding: 30px;
        border-radius: 15px; margin: 15px 0; border: 2px solid #1E88E5;
    }
    .unit { font-size: 24px; color: #333; }
    
    .stButton > button {
        width: 100% !important; height: 55px !important; font-size: 20px !important;
        color: #ff4b4b !important; border: 2px solid #ff4b4b !important;
        background-color: white !important; border-radius: 10px !important;
        margin-bottom: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# クリアボタン用のカウント
if "clear_count" not in st.session_state:
    st.session_state.clear_count = 0

def clear_all():
    st.session_state.clear_count += 1
    st.rerun()

# --- 【最重要】キーボードを強制的に数字（半角）にする入力関数 ---
def number_input_fixed(label, key):
    # keyにclear_countを含めることで、クリアボタン押下時に確実に初期化
    unique_key = f"num_{key}_{st.session_state.clear_count}"
    
    # st.number_inputを使うことで、ブラウザが「数字キーボード」を強制起動します
    val = st.number_input(
        label, 
        min_value=0, 
        value=0, 
        step=10000, 
        key=unique_key,
        format="%d" # 整数として表示
    )
    return val

st.title("💰 推計年収シミュレーター")
st.divider()

tab1, tab2 = st.tabs(["📄 給与明細", "📑 源泉徴収票"])

with tab1:
    if st.button("🔄 入力内容をすべてクリア", key="btn_clear_t1"):
        clear_all()
    
    st.write("### 直近3ヶ月の給与（額面）")
    m1 = number_input_fixed("1ヶ月目", "t1_m1")
    m2 = number_input_fixed("2ヶ月目", "t1_m2")
    m3 = number_input_fixed("3ヶ月目", "t1_m3")
    
    st.write("### ボーナス実績")
    bonus = number_input_fixed("年間合計", "t1_b")
    
    if m1 > 0 or m2 > 0 or m3 > 0:
        avg = (m1 + m2 + m3) / 3
        annual = (avg * 12) + bonus
        st.divider()
        st.write("### 💎 理論上の年収（予測）")
        # 表示側ではしっかりカンマ区切りにします
        st.markdown(f'<div class="result-box">{int(annual):,} <span class="unit">円</span></div>', unsafe_allow_html=True)

with tab2:
    if st.button("🔄 入力内容をすべてクリア", key="btn_clear_t2"):
        clear_all()
        
    st.write("### 源泉徴収票から年換算")
    pay_amount = number_input_fixed("支払金額（現職分のみ）", "t2_pay")
    
    months_list = [f"{i}月" for i in range(1, 13)]
    start_month_str = st.selectbox("現職の入社月", options=months_list, index=7)
    start_month = int(start_month_str.replace('月', ''))

    if pay_amount > 0:
        working_months = 12 - start_month + 1
        theoretical_annual = (pay_amount / working_months) * 12
        st.divider()
        st.write(f"### 💎 現職の推計年収")
        st.markdown(f'<div class="result-box">{int(theoretical_annual):,} <span class="unit">円</span></div>', unsafe_allow_html=True)
