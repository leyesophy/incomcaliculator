import streamlit as st
import unicodedata

# 画面設定
st.set_page_config(page_title="推計年収シミュレーター", layout="centered")

# CSS設定
st.markdown("""
    <style>
    /* 全体のベース文字サイズ */
    html, body, [class*="css"] {
        font-size: 20px !important;
    }

    /* 【修正】タイトルを一回り小さく調整 */
    h1 {
        font-size: 32px !important;
        padding-bottom: 10px;
    }
    
    /* タブの文字サイズ */
    button[data-baseweb="tab"] div {
        font-size: 22px !important;
    }

    /* 入力ラベル（項目名） */
    .stMarkdown p, label {
        font-size: 22px !important;
        font-weight: bold !important;
    }

    /* 入力ボックス（数字キーボード対応サイズ） */
    div[data-baseweb="input"] {
        font-size: 26px !important;
        height: 60px !important;
    }

    /* セレクトボックス */
    div[data-baseweb="select"] {
        font-size: 24px !important;
    }

    /* 結果表示ボックス */
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

    /* 説明文 */
    .stCaption {
        font-size: 18px !important;
        line-height: 1.6;
    }

    /* クリアボタンのスタイル */
    .stButton > button {
        width: 100% !important;
        height: 55px !important;
        font-size: 20px !important;
        color: #ff4b4b !important;
        border: 2px solid #ff4b4b !important;
        background-color: white !important;
        border-radius: 10px !important;
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

# デフォルト空欄 & 数字キーボード強制の入力関数
def number_input_fixed(label, key):
    unique_key = f"num_{key}_{st.session_state.clear_count}"
    val = st.number_input(
        label, 
        min_value=0, 
        value=None, 
        placeholder="金額を入力",
        step=10000, 
        key=unique_key,
        format="%d"
    )
    return val

# タイトル（サイズはCSSで制御）
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
    
    if m1 and m2 and m3:
        b_val = bonus if bonus else 0
        avg = (m1 + m2 + m3) / 3
        annual = (avg * 12) + b_val
        st.divider()
        st.write("### 💎 理論上の年収（予測）")
        st.markdown(f'<div class="result-box">{int(annual):,} <span class="unit">円</span></div>', unsafe_allow_html=True)

with tab2:
    if st.button("🔄 入力内容をすべてクリア", key="btn_clear_t2"):
        clear_all()
        
    st.write("### 源泉徴収票から年換算")
    st.caption("「もし1年間フルで在籍していたら」を逆算します。")

    pay_amount = number_input_fixed("支払金額（現職分のみ）", "t2_pay")
    
    months_list = [f"{i}月" for i in range(1, 13)]
    start_month_str = st.selectbox("現職の入社月", options=months_list, index=7)
    start_month = int(start_month_str.replace('月', ''))

    if pay_amount:
        working_months = 12 - start_month + 1
        theoretical_annual = (pay_amount / working_months) * 12
        st.divider()
        st.write(f"### 💎 現職の推計年収")
        st.markdown(f'<div class="result-box">{int(theoretical_annual):,} <span class="unit">円</span></div>', unsafe_allow_html=True)
        st.info(f"💡 {start_month}月〜12月の実績に基づいた理論値です。")

st.divider()
st.caption("※この数値は額面での推計です。")
