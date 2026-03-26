import streamlit as st
import unicodedata

# 画面設定
st.set_page_config(page_title="推計年収シミュレーター", layout="centered")

# 【超・巨大文字サイズ】CSS
st.markdown("""
    <style>
    html, body, [class*="css"]  { font-size: 28px !important; }
    button[data-baseweb="tab"] div { font-size: 30px !important; font-weight: bold !important; }
    .stMarkdown p, label { font-size: 32px !important; font-weight: bold !important; }
    div[data-baseweb="input"] { font-size: 36px !important; height: 85px !important; }
    input { height: 85px !important; }
    div[data-baseweb="select"] { font-size: 32px !important; height: 75px !important; }
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
    .stCaption { font-size: 24px !important; line-height: 1.6; color: #555 !important; }
    </style>
    """, unsafe_allow_html=True)

# 【改良版】確定時にカンマで上書きする関数
def comma_input(label, key):
    # セッション状態で表示用の文字列を管理
    display_key = f"display_{key}"
    if display_key not in st.session_state:
        st.session_state[display_key] = ""

    # 入力フォーム
    raw_input = st.text_input(label, value=st.session_state[display_key], key=f"widget_{key}", placeholder="例：3000000")

    # 入力があった場合の処理
    # 全角を半角に変換し、既存のカンマを除去
    clean_val = unicodedata.normalize('NFKC', raw_input).replace(',', '').replace('円', '')
    
    if clean_val.isdigit():
        number = int(clean_val)
        formatted = f"{number:,}"
        
        # 現在の表示と異なる場合（＝新しい値が確定した時）にセッションを更新して再描画
        if st.session_state[display_key] != formatted:
            st.session_state[display_key] = formatted
            st.rerun()
        return number
    elif clean_val == "":
        if st.session_state[display_key] != "":
            st.session_state[display_key] = ""
            st.rerun()
        return None
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
        avg = (m1 + m2 + m3) / 3
        annual = (avg * 12) + b_val
        st.divider()
        st.write("### 💎 推計年収")
        st.markdown(f'<div class="result-box">{annual:,.0f}<br><span class="unit">円</span></div>', unsafe_allow_html=True)

with tab2:
    st.write("### 源泉徴収票から年換算")
    pay_amount = comma_input("支払金額（現職分）", "t2_pay")
    
    months_list = [f"{i}月" for i in range(1, 13)]
    start_month_str = st.selectbox("現職の入社月", options=months_list, index=7)
    start_month = int(start_month_str.replace('月', ''))

    if pay_amount:
        working_months = 12 - start_month + 1
        theoretical_annual = (pay_amount / working_months) * 12
        st.divider()
        st.write(f"### 💎 12ヶ月換算の年収")
        st.markdown(f'<div class="result-box">{theoretical_annual:,.0f}<br><span class="unit">円</span></div>', unsafe_allow_html=True)
        st.info(f"💡 {start_month}月〜12月の実績（{working_months}ヶ月分）を元にしています。")

st.divider()
