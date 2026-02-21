import streamlit as st
from integration import integrate_risk_data
import pandas as pd

st.set_page_config(
    page_title="Integrated GRC Risk Governance Dashboard",
    layout="wide"
)

st.title("Integrated GRC Risk Governance Dashboard")
st.subheader("COBIT-aligned Cyber Risk Overview")

# Load integrated data
results = integrate_risk_data()

if not results:
    st.warning("No risk data available.")
    st.stop()

df = pd.DataFrame(results)

# Governance-level metrics
high_risk = df[df["risk_level"] == "High"].shape[0]
medium_risk = df[df["risk_level"] == "Medium"].shape[0]
low_risk = df[df["risk_level"] == "Low"].shape[0]

col1, col2, col3 = st.columns(3)
col1.metric("High Risk Issues", high_risk)
col2.metric("Medium Risk Issues", medium_risk)
col3.metric("Low Risk Issues", low_risk)

# Risk distribution
st.subheader("Risk Distribution")

# ✅ Define the widget BEFORE using it
chart_type = st.selectbox(
    "Select Risk Distribution View",
    ["Bar Chart", "Pie Chart"]
)

risk_counts = df["risk_level"].value_counts()

if chart_type == "Bar Chart":
    st.bar_chart(risk_counts)
else:
    st.pyplot(
        risk_counts.plot.pie(
            autopct="%1.1f%%",
            ylabel=""
        ).figure
    )

# Risk register
st.subheader("Integrated Risk Register")

st.dataframe(
    df[["cve_id", "cvss_score", "risk_level"]],
    use_container_width=True
)

# Governance statement
st.info(
    "This dashboard presents cyber risk insights derived from public vulnerability data, "
    "evaluated using rule-based logic and aligned with COBIT governance objectives. "
    "The system supports governance review but does not automate decision-making."
)
