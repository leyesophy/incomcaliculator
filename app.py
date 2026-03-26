import streamlit as st
import unicodedata

# 画面設定
st.set_page_config(page_title="推計年収シミュレーター", layout="centered")

# CSS：結果表示を豪華に
st.markdown("""
    <style>
    .result-box {
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
    div[data-baseweb="input"] { font-size: 22px !important; }
    </style>
    """, unsafe_allow_html=True)

# 【こだわり機能】入力された文字を「半角数字」にし「カンマ区切り」で上書きする関数
def comma_input(label, key):
    # セッション状態で値を管理
    if key not in st.session_state:
        st.session_state[key] = ""

    # テキスト入力として受け取る
    raw_val = st.text_input(label, value=st.session_state[key], key=f"input_{key}", placeholder="例：3,000,000")

    # 全角を半角に変換し、カンマを除去
    normalized_val = unicodedata.normalize('NFKC', raw_val).replace(',', '').replace('円', '')
    
    if normalized_val.isdigit():
        number = int(normalized_val)
        formatted = f"{number:,}"
        # 入力値が変わった場合のみ、セッション状態を更新して再描画
        if st.session_state[key] != formatted:
            st.session_state[key] = formatted
            st.rerun()
        return number
    elif normalized_val == "":
        st.session_state[key] = ""
        return None
    else:
        if raw_val != "":
            st.error("数字を入力してください")
        return None

st.title("💰 推計年収シミュレーター")

tab1, tab2 = st.tabs(["📄 給与明細3ヶ月分から", "📑 源泉徴収票から年換算"])

with tab1:
    st.subheader("直近3ヶ月の平均から算出")
    m1 = comma_input("1ヶ月目の給与（額面）", "t1_m1")
    m2 = comma_input("2ヶ月目の給与（額面）", "t1_m2")
    m3 = comma_input("3ヶ月目の給與（額面）", "t1_m3")
    bonus = comma_input("年間ボーナス合計（実績）", "t1_b")
    
    if m1 and m2 and m3:
        b_val = bonus if bonus else 0
        avg = (m1 + m2 + m3) / 3
        annual = (avg * 12) + b_val
        st.write("### 理論上の年収（12ヶ月換算）")
        st.markdown(f'<div class="result-box">{annual:,.0f} <span class="unit">円</span></div>', unsafe_allow_html=True)

with tab2:
    st.subheader("📑 源泉徴収票から1年分を推計")
    st.info("入社月と支払金額から「1年間フルで働いた場合」の年収を逆算します。")

    pay_amount = comma_input("源泉徴収票の「支払金額」（現職分のみ）", "t2_pay")
    
    months_list = [f"{i}月" for i in range(1, 13)]
    # デフォルトを8月に設定
    start_month_str = st.selectbox("現職の入社月（対象年）", options=months_list, index=7)
    start_month = int(start_month_str.replace('月', ''))

    if pay_amount:
        # 在職月数の計算（入社月〜12月）
        working_months = 12 - start_month + 1
        
        # 1ヶ月あたりの平均 × 12ヶ月
        theoretical_annual = (pay_amount / working_months) * 12
        
        st.divider()
        st.write(f"### 現職での推計年収（12ヶ月換算）")
        st.markdown(f'<div class="result-box">{theoretical_annual:,.0f} <span class="unit">円</span></div>', unsafe_allow_html=True)
        
        st.success(f"📊 **計算根拠**")
        st.write(f"・在職期間: {start_month}月 〜 12月（{working_months}ヶ月間）")
        st.write(f"・月額換算: 約 {pay_amount / working_months:,.0f} 円")
