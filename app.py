import streamlit as st
from datetime import date

# 画面設定
st.set_page_config(page_title="推計年収シミュレーター", layout="centered")

# 金額を大きく表示するCSS
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
    /* 入力欄の文字を大きく */
    div[data-baseweb="input"] { font-size: 20px !important; }
    </style>
    """, unsafe_allow_html=True)

# 金額入力をカンマ区切りにする補助関数
def format_input_amount(label, key):
    # テキストとして入力を受け取り、表示時にカンマを入れる
    val = st.text_input(label, value="", key=key, placeholder="例: 1,200,000")
    # カンマを除去して数字に変換
    clean_val = val.replace(',', '').replace('円', '')
    if clean_val.isdigit():
        amount = int(clean_val)
        # 入力欄の下にカンマ区切りの確認用表示を出す（Streamlitの仕様上の工夫）
        st.caption(f"入力額: {amount:,} 円")
        return amount
    return None

st.title("💰 推計年収シミュレーター")

tab1, tab2 = st.tabs(["📄 給与明細3ヶ月分から", "📑 源泉徴収票から年換算"])

with tab1:
    st.subheader("直近3ヶ月の平均から算出")
    m1 = format_input_amount("1ヶ月目の給与（額面）", "t1_m1")
    m2 = format_input_amount("2ヶ月目の給与（額面）", "t1_m2")
    m3 = format_input_amount("3ヶ月目の給与（額面）", "t1_m3")
    bonus = format_input_amount("年間ボーナス合計（実績）", "t1_b")
    
    if m1 and m2 and m3:
        b_val = bonus if bonus else 0
        avg = (m1 + m2 + m3) / 3
        annual = (avg * 12) + b_val
        st.write("### 理論上の年収（12ヶ月換算）")
        st.markdown(f'<div class="result-box">{annual:,.0f} <span class="unit">円</span></div>', unsafe_allow_html=True)

with tab2:
    st.subheader("📑 源泉徴収票から1年分を推計")
    st.info("入社月と支払金額から「1年間フルで働いた場合」の年収を逆算します。")

    # 源泉徴収票の支払金額を入力
    pay_amount = format_input_amount("源泉徴収票の「支払金額」（現職分のみ）", "t2_pay")
    
    # 入社月の選択（1月〜12月）
    months_list = [f"{i}月" for i in range(1, 13)]
    start_month_str = st.selectbox("現職の入社月（源泉徴収票の対象年）", options=months_list, index=7) # デフォルト8月
    start_month = int(start_month_str.replace('月', ''))

    if pay_amount:
        # 在職月数の計算（入社月から12月まで）
        working_months = 12 - start_month + 1
        
        # 1ヶ月あたりの平均給与
        monthly_avg = pay_amount / working_months
        
        # 年間換算（12ヶ月分）
        theoretical_annual = monthly_avg * 12
        
        st.divider()
        st.write(f"### 現職での推計年収（12ヶ月換算）")
        st.markdown(f'<div class="result-box">{theoretical_annual:,.0f} <span class="unit">円</span></div>', unsafe_allow_html=True)
        
        # 計算の根拠を表示
        st.success(f"📊 **計算根拠**")
        st.write(f"・在職期間: {start_month}月 〜 12月（{working_months}ヶ月間）")
        st.write(f"・期間中の総支給: {pay_amount:,} 円")
        st.write(f"・月額換算: 約 {monthly_avg:,.0f} 円")
        st.caption("※ボーナスを含んだ支払金額から単純に月割り計算しています。")

st.caption("※このアプリは「もし1年間在籍したら」というポテンシャルを可視化するものです。")
