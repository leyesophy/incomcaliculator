import streamlit as st
from datetime import date

# 画面設定：①と言語設定（日本語）を考慮
st.set_page_config(
    page_title="推計年収シミュレーター", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# カスタムCSS：金額を大きく表示
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
    input { font-size: 18px !important; }
    </style>
    """, unsafe_allow_html=True)

# アプリタイトルの修正
st.title("💰 推計年収シミュレーター")
st.caption("直近の給与や入社日から、今年の総収入を予測します")

tab1, tab2 = st.tabs(["📄 給与明細3ヶ月分から", "🏢 中途入社・源泉徴収合算"])

with tab1:
    st.subheader("直近3ヶ月の給与（額面）")
    # ① デフォルトを空（None）に設定。入力されるまで計算を待機する仕組み
    # ※ number_inputでNoneにするとブランクになります
    m1 = st.number_input("1ヶ月目の給与", value=None, placeholder="金額を入力してください", step=1000, format="%d", key="m1")
    m2 = st.number_input("2ヶ月目の給与", value=None, placeholder="金額を入力してください", step=1000, format="%d", key="m2")
    m3 = st.number_input("3ヶ月目の給与", value=None, placeholder="金額を入力してください", step=1000, format="%d", key="m3")
    
    st.subheader("ボーナス")
    bonus = st.number_input("年間ボーナス合計（予定）", value=None, placeholder="0", step=10000, format="%d", key="b1")
    
    # 全ての月が入力されたら計算
    if m1 is not None and m2 is not None and m3 is not None:
        val_bonus = bonus if bonus is not None else 0
        avg = (m1 + m2 + m3) / 3
        annual_total = (avg * 12) + val_bonus
        
        st.divider()
        st.write("### 推計年収（予測）")
        st.markdown(f'<div class="big-font">{annual_total:,.0f} <span class="unit">円</span></div>', unsafe_allow_html=True)
        st.info(f"月平均 {avg:,.0f}円 × 12ヶ月 ＋ ボーナス {val_bonus:,}円")
    else:
        st.info("上の3ヶ月分の給与を入力すると、自動で年収を推計します。")

with tab2:
    st.subheader("③ 中途入社の推計計算")
    
    # 前職のデータ
    prev_income = st.number_input("前職の源泉徴収票「支払金額」", value=None, placeholder="0", step=1000, format="%d", key="prev")
    
    st.divider()
    
    # 現職のデータ
    st.write("#### 現職（今の会社）の情報")
    # ② 日本語カレンダー対応。format引数で日本式の日付表示に。
    hire_date = st.date_input("現職の入社日", value=date.today(), format="YYYY/MM/DD")
    
    curr_monthly = st.number_input("今の会社の月給（額面）", value=None, placeholder="金額を入力", step=1000, format="%d", key="curr_m")
    curr_bonus = st.number_input("現職での年内ボーナス予定", value=None, placeholder="0", step=10000, format="%d", key="curr_b")

    # 入社日から年内の支給回数を自動計算
    remaining_months = 12 - hire_date.month + 1
    st.caption(f"💡 入社日が {hire_date.month}月 なので、年内の給与支給を {remaining_months}回 と計算しました。")

    # 入力があれば計算
    if curr_monthly is not None:
        val_prev = prev_income if prev_income is not None else 0
        val_curr_b = curr_bonus if curr_bonus is not None else 0
        
        current_company_total = (curr_monthly * remaining_months) + val_curr_b
        total_year_income = val_prev + current_company_total
        
        st.divider()
        st.write("### 今年の合計推計年収")
        st.markdown(f'<div class="big-font">{total_year_income:,.0f} <span class="unit">円</span></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        col1.metric("前職の支払金額", f"{val_prev:,}円")
        col2.metric("現職の推計（年内）", f"{current_company_total:,}円")
    else:
        st.info("「今の会社の月給」を入力してください。")

st.caption("※このシミュレーターは、入力された額面金額に基づいた単純計算です。")
