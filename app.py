import streamlit as st
import unicodedata

# 画面設定
st.set_page_config(page_title="推計年収シミュレーター", layout="centered")

# 【超・巨大文字サイズ】CSS
st.markdown("""
    <style>
    /* 全体のベースをさらに大きく (標準16px → 前回20px → 今回28px) */
    html, body, [class*="css"]  {
        font-size: 28px !important;
    }
    
    /* タブの文字を巨大化 */
    button[data-baseweb="tab"] div {
        font-size: 30px !important;
        font-weight: bold !important;
    }

    /* 入力ラベル（項目名）を目立たせる */
    .stMarkdown p, label {
        font-size: 32px !important;
        font-weight: bold !important;
        margin-bottom: 15px !important;
    }

    /* 入力ボックスを特大サイズに (高さ60px → 85px) */
    div[data-baseweb="input"] {
        font-size: 36px !important;
        height: 85px !important;
    }
    input {
        height: 85px !important;
    }

    /* セレクトボックス（入社月） */
    div[data-baseweb="select"] {
        font-size: 32px !important;
        height: 75px !important;
    }

    /* 結果表示ボックス（青文字）を最大化 */
    .result-box {
        font-size: 64px !important;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        background-color: #f0f2f6;
        padding: 40px;
        border-radius: 20px;
        margin: 20px 0;
        border: 4px solid #1E88E5;
        line-height: 1.2;
    }
    .unit { font-size: 32px; color: #333; }

    /* 説明文もはっきりと */
    .stCaption {
        font-size: 24px !important;
        line-height: 1.6;
        color: #555 !important;
    }

    /* 区切り線も太く */
    hr {
        border: 0;
        height: 3px;
        background: #ccc;
    }
    </style>
    """, unsafe_allow_html=True)

# 金額入力をカンマ区切りにする補助関数
def comma_input(label, key):
    if key not in st.session_state:
        st.session_state[key] = ""

    raw_val = st.text_input(label, value=st.session_state[key], key=f"input_{key}", placeholder="3,000,000")

    # 全角を半角に変換し、カンマを除去
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
            st.error("数字を入れてください")
        return None

st.title("💰 推計年収シミュレーター")
st.divider()

tab1, tab2 = st.tabs(["📄 給与明細", "📑 源泉徴収票"])

with tab1:
    st.write("### 3ヶ月の給与額面")
    m1 = comma_input("1ヶ月目", "t1_m1")
    m2 = comma_input("2ヶ月目", "t1_m2")
    m3 = comma_input("3ヶ月目", "t1_m3")
    
    st.write("### ボーナス合計")
    bonus = comma_input("年間実績", "t1_b")
    
    if m1 and m2 and m3:
        b_val = bonus if bonus else 0
        avg = (m1 +
