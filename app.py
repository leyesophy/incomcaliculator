with tab1:
    if st.button("🔄 入力内容をすべてクリア", key="btn_clear_t1"):
        clear_all()
    
    st.write("### 直近3ヶ月の給与（額面）")
    m1 = number_input_fixed("1ヶ月目", "t1_m1")
    m2 = number_input_fixed("2ヶ月目", "t1_m2")
    m3 = number_input_fixed("3ヶ月目", "t1_m3")
    
    st.write("### ボーナス実績")
    bonus = number_input_fixed("年間合計", "t1_b")
    
    if m1 is not None and m2 is not None and m3 is not None:
        b_val = bonus if bonus else 0
        avg = (m1 + m2 + m3) / 3
        annual = (avg * 12) + b_val
        
        st.divider()
        st.write("### 💎 理論上の年収（予測）")
        st.markdown(f'<div class="result-box">{int(annual):,} <span class="unit">円</span></div>', unsafe_allow_html=True)
        
        # --- 計算過程の表示 ---
        with st.expander("📝 計算過程を確認する", expanded=True):
            st.write(f"1. **月平均額**: ({m1:,} + {m2:,} + {m3:,}) ÷ 3ヶ月 = **{int(avg):,}円**")
            st.write(f"2. **年換算（月収分）**: {int(avg):,}円 × 12ヶ月 = **{int(avg*12):,}円**")
            if b_val > 0:
                st.write(f"3. **ボーナス加算**: {int(avg*12):,}円 + {b_val:,}円 = **{int(annual):,}円**")
            else:
                st.write("3. **ボーナス加算**: なし")

with tab2:
    if st.button("🔄 入力内容をすべてクリア", key="btn_clear_t2"):
        clear_all()
        
    st.write("### 源泉徴収票から年換算")
    st.caption("「入社翌月から12月までの給与」をベースに、12ヶ月分を逆算します。")

    pay_amount = number_input_fixed("支払金額（入社翌月〜12月分）", "t2_pay")
    
    months_list = [f"{i}月" for i in range(1, 13)]
    start_month_str = st.selectbox("現職の入社月", options=months_list, index=7)
    start_month = int(start_month_str.replace('月', ''))

    if pay_amount:
        # 入社月の翌月から12月までの月数を算出 (例: 8月入社なら 12-8=4ヶ月)
        working_months = 12 - start_month
        
        if working_months > 0:
            theoretical_annual = (pay_amount / working_months) * 12
            st.divider()
            st.write(f"### 💎 現職の推計年収")
            st.markdown(f'<div class="result-box">{int(theoretical_annual):,} <span class="unit">円</span></div>', unsafe_allow_html=True)
            
            # --- 計算過程の表示 ---
            with st.expander("📝 計算過程を確認する", expanded=True):
                st.write(f"1. **対象期間**: {start_month+1}月 〜 12月（計 **{working_months}ヶ月間**）")
                st.write(f"2. **推定月収**: {pay_amount:,}円 ÷ {working_months}ヶ月 = **{int(pay_amount/working_months):,}円**")
                st.write(f"3. **年換算**: {int(pay_amount/working_months):,}円 × 12ヶ月 = **{int(theoretical_annual):,}円**")
            
            st.info(f"💡 {start_month+1}月〜12月の実績に基づいた理論値です。")
        else:
            st.warning("⚠️ 12月入社の場合は、翌月以降の実績がないため計算できません。")
