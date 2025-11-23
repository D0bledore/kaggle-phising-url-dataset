import streamlit as st
import pandas as pd
import pickle
import numpy as np

# Page config
st.set_page_config(page_title="Phishing Detection Demo", page_icon="🔒", layout="wide")

# Load data and model
@st.cache_data
def load_data():
    df = pd.read_csv('data/dataset4.csv')
    features_to_exclude = ['URLSimilarityIndex', 'FILENAME', 'URL', 'Domain', 'TLD', 'Title', 'label']
    feature_cols = [col for col in df.columns if col not in features_to_exclude]
    return df, feature_cols

@st.cache_resource
def load_model():
    with open('models/xgb_model.pkl', 'rb') as f:
        return pickle.load(f)

df, feature_cols = load_data()
model = load_model()

# Rule function
def apply_rules(row):
    """Apply 7 perfect rules from notebook 2"""

    # Rule 1: Zero Resources
    if row['NoOfJS'] == 0 and row['NoOfCSS'] == 0 and row['NoOfImage'] == 0:
        return (True, "Rule 1: Zero Resources", "Site has no JavaScript, CSS, or images - typical of lazy phishing")

    # Rule 2: No HTTPS
    if row['IsHTTPS'] == 0:
        return (True, "Rule 2: No HTTPS", "Site uses HTTP instead of HTTPS - no encryption")

    # Rule 3: Domain is IP
    if row['IsDomainIP'] == 1:
        return (True, "Rule 3: Domain is IP Address", "Domain is an IP address instead of proper domain name")

    # Rule 4: Zero Trust Signals
    if (row['HasTitle'] == 0 and row['HasFavicon'] == 0 and
        row['HasDescription'] == 0 and row['HasCopyrightInfo'] == 0):
        return (True, "Rule 4: Zero Trust Signals", "No title, favicon, description, or copyright - minimal effort site")

    # Rule 5: No References
    if (row['NoOfExternalRef'] == 0 and row['NoOfSelfRef'] == 0 and
        row['NoOfEmptyRef'] == 0):
        return (True, "Rule 5: No References", "Site has no internal or external links - isolated page")

    # Rule 6: Many Subdomains
    if row['NoOfSubDomain'] >= 5:
        return (True, "Rule 6: Excessive Subdomains", f"URL has {int(row['NoOfSubDomain'])} subdomains - suspicious structure")

    # Rule 7: Long URL
    if row['URLLength'] > 57:
        return (True, "Rule 7: Long URL", f"URL is {int(row['URLLength'])} characters - obfuscation technique")

    # No rule triggered
    return (False, None, None)

# Header
st.title("🔒 Phishing Detection System")
st.markdown("### Hybrid Approach: Rule-Based + Machine Learning")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Demo Controls")

    # Filter options
    filter_type = st.radio("Filter URLs:", ["All", "Phishing Only", "Legitimate Only"])

    if filter_type == "Phishing Only":
        filtered_df = df[df['label'] == 0].reset_index(drop=True)
    elif filter_type == "Legitimate Only":
        filtered_df = df[df['label'] == 1].reset_index(drop=True)
    else:
        filtered_df = df.reset_index(drop=True)

    st.info(f"Showing {len(filtered_df):,} URLs")

    # URL selection
    url_idx = st.selectbox(
        "Select URL to analyze:",
        range(len(filtered_df)),
        format_func=lambda i: f"#{i+1}: {filtered_df.iloc[i]['URL'][:50]}..."
    )

    st.markdown("---")

    # Edge cases
    st.subheader("Notable Edge Cases")

    edge_cases = {
        "seedjfly.top (Ultimate)": "https://www.seedjfly.top",
        "rariblies.blogspot.com": "https://rariblies.blogspot.com/",
        "pha.xujmno.xyz": "https://pha.xujmno.xyz/logi/",
        "nubakk.000webhostapp": "https://nubakk.000webhostapp.com/",
        "byil.blogspot.com": "https://byil.blogspot.com/"
    }

    for name, url in edge_cases.items():
        if st.button(name, use_container_width=True):
            idx = df[df['URL'] == url].index
            if len(idx) > 0:
                st.session_state['selected_url'] = idx[0]

# Main content
selected_row = filtered_df.iloc[url_idx]
original_idx = selected_row.name if filter_type == "All" else df[df['URL'] == selected_row['URL']].index[0]

# Display URL
st.subheader("📍 Selected URL")
st.code(selected_row['URL'], language=None)

col1, col2 = st.columns(2)

with col1:
    actual_label = "🚨 PHISHING" if selected_row['label'] == 0 else "✅ LEGITIMATE"
    st.metric("Actual Label", actual_label)

# Stage 1: Rule-based filtering
st.markdown("### 🎯 Stage 1: Rule-Based Filter")
caught, rule_name, rule_explanation = apply_rules(selected_row)

if caught:
    st.error(f"**BLOCKED** by {rule_name}")
    st.info(rule_explanation)
    st.markdown("**Decision:** Block immediately (no ML needed)")

else:
    st.success("✓ Passed all 7 rules → Proceed to ML scoring")

    # Stage 2: ML scoring
    st.markdown("### 🤖 Stage 2: Machine Learning Prediction")

    # Get features and predict
    features = df[feature_cols].iloc[[original_idx]]
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]

    prob_phishing = probabilities[0] * 100
    prob_legitimate = probabilities[1] * 100

    # Display prediction
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Phishing Probability", f"{prob_phishing:.2f}%")

    with col2:
        st.metric("Legitimate Probability", f"{prob_legitimate:.2f}%")

    # Risk assessment
    st.markdown("#### Risk Assessment")

    if prob_phishing > 90:
        st.error(f"🔴 **HIGH RISK** ({prob_phishing:.1f}% phishing)\n\n**Recommendation:** Flag for immediate manual review")
    elif prob_phishing > 70:
        st.warning(f"🟡 **MEDIUM RISK** ({prob_phishing:.1f}% phishing)\n\n**Recommendation:** Queue for manual review")
    else:
        st.success(f"🟢 **LOW RISK** ({prob_phishing:.1f}% phishing)\n\n**Recommendation:** Allow")

    # Feature importance for this prediction
    st.markdown("#### Top Contributing Features")

    feature_values = selected_row[feature_cols]
    importance_data = []

    # Show key features
    key_features = ['LineOfCode', 'NoOfSelfRef', 'NoOfExternalRef', 'NoOfImage',
                    'NoOfJS', 'NoOfCSS', 'IsHTTPS', 'HasSocialNet', 'Robots', 'IsResponsive']

    for feat in key_features:
        if feat in feature_cols:
            importance_data.append({
                'Feature': feat,
                'Value': feature_values[feat]
            })

    st.dataframe(pd.DataFrame(importance_data), use_container_width=True, hide_index=True)

# Performance stats
st.markdown("---")
st.markdown("### 📊 System Performance")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("XGBoost Accuracy", "100.00%")

with col2:
    st.metric("Recall", "99.995%")

with col3:
    st.metric("False Positives", "0")

with col4:
    st.metric("Rules Coverage", "88.2%")

st.caption("Performance metrics from notebook 3 evaluation on 47,159 test URLs")
