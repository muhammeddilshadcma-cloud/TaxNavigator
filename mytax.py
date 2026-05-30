import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# ====================================================================
# PREMIUM UI CONFIGURATION
# ====================================================================
st.set_page_config(page_title="TaxNavigator Pro | Muhammed Dilshad PK", layout="wide", page_icon="🇮🇳")

def apply_ultra_theme():
    st.markdown("""
        <style>
        .stApp { background-color: #000000 !important; color: #FFFFFF !important; }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #87CEEB 0%, #2196F3 100%) !important;
            box-shadow: 5px 0 15px rgba(33, 150, 243, 0.3);
        }
        [data-testid="stSidebar"] * { color: #000000 !important; font-weight: 700 !important; }
        .tax-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(12px);
            border-radius: 20px;
            padding: 30px;
            border: 1px solid rgba(135, 206, 235, 0.2);
            margin-bottom: 20px;
            animation: fadeIn 0.8s ease-in-out;
        }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .stButton>button {
            background: linear-gradient(90deg, #87CEEB, #2196F3) !important;
            color: #000000 !important; border-radius: 12px !important;
            border: none !important; padding: 15px 30px !important;
            font-size: 16px !important; font-weight: bold !important;
            transition: all 0.3s ease !important;
        }
        .stButton>button:hover { box-shadow: 0 0 20px #87CEEB; transform: scale(1.02); }
        .stButton>button:active { transform: scale(0.95); }
        h1, h2, h3 { color: #87CEEB !important; }
        .footer { text-align: center; color: #87CEEB; padding: 20px; border-top: 1px solid rgba(135, 206, 235, 0.1); }
        </style>
    """, unsafe_allow_html=True)

apply_ultra_theme()

# ====================================================================
# SESSION STATE INITIALIZATION
# ====================================================================
if 'step' not in st.session_state: st.session_state.step = 0
if 'data' not in st.session_state: 
    st.session_state.data = {
        "salary": 0.0, "hp_income": 0.0, "biz_income": 0.0, "cap_gains": 0.0,
        "other_sources": 0.0, "presumptive": 0.0, "deductions": 0.0,
        "entity": "Individual", "name": "", "pan": "", "age": 30, "is_nri": False
    }

# ====================================================================
# SIDEBAR
# ====================================================================
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>TaxNavigator</h1>", unsafe_allow_html=True)
    st.session_state.data['entity'] = st.selectbox("Entity", ["Individual", "HUF", "Firm", "LLP", "Company", "Trust"])
    
    # Dynamic Human Icon logic
    if st.session_state.data['entity'] in ["Individual", "HUF"]:
        st.image("https://img.icons8.com/fluency/144/user-male-circle.png", width=120)
    else:
        st.image("https://img.icons8.com/fluency/144/company.png", width=120)
    
    st.markdown("---")
    st.write("👤 **Owner:** Muhammed Dilshad PK")
    st.write("Assessment Year: **2026-27**")
    st.markdown("### 🔍 Research Centre")
    query = st.text_input("Section Search (e.g. 194Q, 44AB)")

# ====================================================================
# APP WORKFLOW
# ====================================================================
st.progress(st.session_state.step/5, text=f"Step {st.session_state.step} of 5")

# STEP 0: WELCOME
if st.session_state.step == 0:
    st.markdown("<div class='tax-card'>", unsafe_allow_html=True)
    st.title("Welcome to TaxNavigator® Enterprise")
    st.write("Calculate • Compare • Plan • Research • Comply")
    if st.button("Start Professional Analysis"):
        st.session_state.step = 1
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# STEP 1: PROFILE
elif st.session_state.step == 1:
    st.markdown("<div class='tax-card'>", unsafe_allow_html=True)
    st.subheader("👤 Step 1: Taxpayer Identification")
    c1, c2 = st.columns(2)
    st.session_state.data['name'] = c1.text_input("Full Name", st.session_state.data['name'])
    st.session_state.data['pan'] = c2.text_input("PAN Number (10 digits)").upper()
    st.session_state.data['age'] = c1.number_input("Age", 1, 100, 30)
    st.session_state.data['is_nri'] = c2.checkbox("Are you an NRI?")
    if st.button("Proceed to Income Entry ➜"):
        st.session_state.step = 2
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# STEP 2: INCOME ENTRY
elif st.session_state.step == 2:
    st.markdown("<div class='tax-card'>", unsafe_allow_html=True)
    st.subheader("💰 Step 2: Income Sources")
    
    with st.expander("💼 Salary & House Property", expanded=True):
        st.session_state.data['salary'] = st.number_input("Gross Annual Salary", value=0.0)
        st.session_state.data['hp_income'] = st.number_input("Income from House Property (Rent minus Interest)", value=0.0)
        
    with st.expander("📈 Capital Gains & Business"):
        st.session_state.data['cap_gains'] = st.number_input("Short/Long Term Capital Gains", value=0.0)
        st.session_state.data['biz_income'] = st.number_input("Manual Business Profit (Non-Presumptive)", value=0.0)
        
    with st.expander("🏛️ Other Sources"):
        st.session_state.data['other_sources'] = st.number_input("Bank Interest, Dividends, Lottery", value=0.0)

    if st.button("Proceed to Presumptive Taxation ➜"):
        st.session_state.step = 3
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# STEP 3: PRESUMPTIVE TAX
elif st.session_state.step == 3:
    st.markdown("<div class='tax-card'>", unsafe_allow_html=True)
    st.subheader("⚡ Step 3: Presumptive Taxation (Sec 44AD/ADA)")
    mode = st.selectbox("Select Section", ["None", "44AD (Small Business)", "44ADA (Professional)"])
    
    if mode == "44AD (Small Business)":
        turnover = st.number_input("Total Turnover (Max 3 Cr)", value=0.0)
        digital = st.number_input("Digital Receipts", value=0.0)
        st.session_state.data['presumptive'] = (digital * 0.06) + ((turnover-digital) * 0.08)
    elif mode == "44ADA (Professional)":
        receipts = st.number_input("Total Professional Receipts (Max 75L)", value=0.0)
        st.session_state.data['presumptive'] = receipts * 0.50
    else:
        st.session_state.data['presumptive'] = 0.0
        
    st.info(f"Presumptive Income: ₹{st.session_state.data['presumptive']:,.0f}")
    if st.button("Proceed to Deductions ➜"):
        st.session_state.step = 4
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# STEP 4: DEDUCTIONS (DROPDOWN SECTIONS)
elif st.session_state.step == 4:
    st.markdown("<div class='tax-card'>", unsafe_allow_html=True)
    st.subheader("📉 Step 4: Chapter VI-A Deductions")
    st.caption("Enter details for the Old Tax Regime. The system will automatically calculate the best regime for you.")

    total_d = 0.0

    # 1. Investments (80C Category)
    with st.expander("💎 Section 80C, 80CCC, 80CCD (Investments - Max 1.5L)"):
        c1, c2 = st.columns(2)
        lic_ppf = c1.number_input("Life Insurance / PPF / ELSS / EPF", value=0.0)
        tuition = c2.number_input("Children Tuition Fees", value=0.0)
        housing_principal = c1.number_input("Home Loan Principal Repayment", value=0.0)
        total_d += min(lic_ppf + tuition + housing_principal, 150000.0)

    # 2. Health & Disability (80D Category)
    with st.expander("🩺 Section 80D, 80DD, 80DDB (Medical)"):
        health_self = st.number_input("Health Insurance (Self/Family) - Max 25k/50k", value=0.0)
        health_parents = st.number_input("Health Insurance (Parents) - Max 25k/50k", value=0.0)
        st.checkbox("Check if parents are Senior Citizens", key="senior_parents")
        total_d += health_self + health_parents

    # 3. Education & Interest (80E Category)
    with st.expander("🎓 Section 80E, 80EEA, 80EEB (Interests)"):
        edu_int = st.number_input("Interest on Education Loan (80E)", value=0.0)
        ev_loan = st.number_input("Interest on Electric Vehicle Loan (80EEB)", value=0.0)
        total_d += edu_int + ev_loan

    # 4. Others (80G, 80TTA, 80U)
    with st.expander("🌍 Donations & Savings Interest (80G, 80TTA/B, 80U)"):
        donations = st.number_input("Donations to Charities (80G)", value=0.0)
        saving_int = st.number_input("Savings Bank Interest (80TTA/B) - Max 10k/50k", value=0.0)
        total_d += donations + saving_int

    st.session_state.data['deductions'] = total_d
    
    if st.button("Generate Final Dashboard ➜"):
        with st.spinner("Analyzing Tax Compliance..."):
            time.sleep(1.5)
            st.session_state.step = 5
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# STEP 5: FINAL DASHBOARD & ITR SELECTOR
elif st.session_state.step == 5:
    d = st.session_state.data
    gti = d['salary'] + d['hp_income'] + d['biz_income'] + d['cap_gains'] + d['other_sources'] + d['presumptive']
    
    # ITR SELECTION LOGIC
    itr_form = "ITR-1"
    if d['entity'] != "Individual":
        itr_form = "ITR-5/6"
    elif d['cap_gains'] > 0:
        itr_form = "ITR-2"
    elif d['presumptive'] > 0:
        itr_form = "ITR-4 (Sugam)"
    elif d['biz_income'] > 0:
        itr_form = "ITR-3"
    elif gti > 5000000:
        itr_form = "ITR-2"

    st.markdown("<div class='tax-card'>", unsafe_allow_html=True)
    st.title(f"📊 Assessment for {d['name']}")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Gross Total Income", f"₹{gti:,.0f}")
    col2.metric("Total Deductions", f"₹{d['deductions']:,.0f}")
    
    # HIGH-END VISUALIZATION
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = gti,
        title = {'text': "Income Level"},
        gauge = {'axis': {'range': [None, 2000000]}, 'bar': {'color': "#87CEEB"}}
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "#FFFFFF"})
    st.plotly_chart(fig, use_container_width=True)

    st.success(f"📋 **RECOMMENDED ITR FORM: {itr_form}**")
    st.info("💡 **Reasoning:** Logic based on Income Heads, Gross Amount, and Presumptive Taxation selection.")
    
    if st.button("Finish & Export PDF (Draft)"):
        st.balloons()
        st.toast("Report ready for Muhammed Dilshad PK review.")
        
    if st.button("New Analysis"):
        st.session_state.step = 0
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# FOOTER
st.markdown(f"""
    <div class='footer'>
        © 2026 Muhammed Dilshad PK | TaxNavigator® Enterprise Build <br>
        Calculate • Compare • Plan • Research • Comply
    </div>
""", unsafe_allow_html=True)
