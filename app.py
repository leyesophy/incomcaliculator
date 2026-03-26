import streamlit as st
import pandas as pd

st.title("📊 複数職種・人件費シミュレーター")

# サイドバーで2種類の時給を設定
st.sidebar.header("タイプA（例：一般スタッフ）")
wage_a = st.sidebar.number_input("時給A（円）", value=1200)
count_a = st.sidebar.number_input("人数A（人）", value=5, min_value=0)

st.sidebar.header("タイプB（例：リーダー/社員）")
wage_b = st.sidebar.number_input("時給B（円）", value=1800)
count_b = st.sidebar.number_input("人数B（人）", value=1, min_value=0)

st.sidebar.header("共通設定")
hours = st.sidebar.number_input("1日の稼働時間（h）", value=8)
days = st.sidebar.number_input("月間稼働日数（日）", value=22)

# 計算ロジック
daily_a = wage_a * count_a * hours
daily_b = wage_b * count_b * hours
total_daily = daily_a + daily_b
total_monthly = total_daily * days

# 結果表示
st.subheader("💰 月間コストの内訳")
col1, col2 = st.columns(2)
with col1:
    st.metric("1日の総額", f"{total_daily:,} 円")
    st.write(f"内訳A: {daily_a:,}円 / 内訳B: {daily_b:,}円")
with col2:
    st.metric("ひと月の総額", f"{total_monthly:,} 円")

# 円グラフで内訳を表示（新機能！）
st.divider()
st.subheader("🍰 人件費の比率")
pie_data = pd.DataFrame({
    "タイプ": ["タイプA", "タイプB"],
    "金額": [daily_a, daily_b]
})
# シンプルな円グラフ（plotlyなどを使わず、まずは標準機能で）
st.bar_chart(pie_data.set_index("タイプ")) # 棒グラフの方が見やすい場合も多いです