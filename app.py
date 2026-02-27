import streamlit as st
import numpy as np
from scipy.stats import t
from statistics import stdev

st.set_page_config(page_title="Two Sample t-Test", layout="centered")

def san(a, b, alt):
    alpha = 0.05

    if len(a) < 2 or len(b) < 2:
        return {"error": "Each sample must contain at least two values"}

    n1 = len(a)
    n2 = len(b)

    x1 = np.mean(a)
    x2 = np.mean(b)

    sd1 = stdev(a)
    sd2 = stdev(b)

    df = n1 + n2 - 2
    mu = 0

    se = np.sqrt((sd1**2 / n1) + (sd2**2 / n2))
    tcal = ((x1 - x2) - mu) / se

    p_value = (1 - t.cdf(abs(tcal), df)) * 2

    result = {
        "t_calculated": tcal,
        "p_value": p_value,
        "df": df
    }

    if alt == "two-sided":
        alpha = alpha / 2
        t_pos = t.ppf(1 - alpha, df)
        t_neg = t.ppf(alpha, df)
        result["t_critical"] = (t_neg, t_pos)
        result["confidence_interval"] = (
            mu + t_neg * se,
            mu + t_pos * se
        )

    elif alt == "greater":
        t_pos = t.ppf(1 - alpha, df)
        result["t_critical"] = t_pos
        result["confidence_interval"] = mu + t_pos * se

    elif alt == "less":
        t_neg = t.ppf(alpha, df)
        result["t_critical"] = t_neg
        result["confidence_interval"] = mu + t_neg * se

    return result


st.title("Two Sample t-Test")

st.write("Enter sample values separated by commas")

a_input = st.text_input("Sample A", "10,12,14,15")
b_input = st.text_input("Sample B", "9,11,13,14")

alt = st.selectbox(
    "Alternative Hypothesis",
    ("two-sided", "greater", "less")
)

if st.button("Run Test"):
    try:
        a = [float(x.strip()) for x in a_input.split(",") if x.strip() != ""]
        b = [float(x.strip()) for x in b_input.split(",") if x.strip() != ""]

        output = san(a, b, alt)

        if "error" in output:
            st.error(output["error"])
        else:
            st.subheader("Results")
            st.write("t calculated:", output["t_calculated"])
            st.write("degrees of freedom:", output["df"])
            st.write("p-value:", output["p_value"])
            st.write("t critical:", output["t_critical"])
            st.write("confidence interval:", output["confidence_interval"])

    except Exception as e:
        st.error(f"Invalid input: {e}")