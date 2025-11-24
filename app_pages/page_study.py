import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.data_management import load_data


def page_study_body():
    """
    Display data analysis and rule discovery findings.
    Addresses LO6.2: Dashboard shows plots with interpretation.
    """

    st.write("## Data Analysis & Rule Discovery")

    st.info(
        "This page presents findings from Notebooks 1 and 2: dataset exploration and rule development. "
        "The analysis identified key phishing patterns that informed the 6 perfect-precision rules."
    )

    # Load data
    df, feature_cols = load_data()

    st.write("### Dataset Distribution")

    # Class balance
    phishing_count = len(df[df['label'] == 0])
    legitimate_count = len(df[df['label'] == 1])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total URLs", f"{len(df):,}")
    with col2:
        st.metric("Phishing", f"{phishing_count:,}")
    with col3:
        st.metric("Legitimate", f"{legitimate_count:,}")

    st.write(
        f"**Interpretation**: Dataset has {phishing_count:,} phishing ({phishing_count/len(df)*100:.1f}%) "
        f"and {legitimate_count:,} legitimate ({legitimate_count/len(df)*100:.1f}%) URLs. "
        "This 43/57 split is reasonably balanced for ML training - not severely imbalanced."
    )

    st.write("---")

    st.write("### Key Pattern Discovery: HTTPS Adoption")

    # HTTPS rates by label
    phishing_https = df[df['label'] == 0]['IsHTTPS'].mean() * 100
    legitimate_https = df[df['label'] == 1]['IsHTTPS'].mean() * 100

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Phishing HTTPS Rate", f"{phishing_https:.1f}%")
    with col2:
        st.metric("Legitimate HTTPS Rate", f"{legitimate_https:.1f}%")

    st.write(
        f"**Interpretation**: Only {phishing_https:.1f}% of phishing sites use HTTPS vs {legitimate_https:.1f}% "
        "of legitimate sites. This massive gap led to Rule 2 (No HTTPS). However, the fact that some phishing "
        "sites DO use HTTPS shows why rules alone aren't sufficient - ML is needed for sophisticated cases."
    )

    st.write("---")

    st.write("### The 6 Perfect-Precision Rules")

    st.write(
        "Through feature investigation in Notebook 1 and validation in Notebook 2, "
        "I developed 6 rules with 100% precision (zero false positives):"
    )

    rules_df = pd.DataFrame({
        'Rule': [
            '1. Zero Resources',
            '2. No HTTPS',
            '3. Domain is IP',
            '4. Zero Trust Signals',
            '5. Excessive Subdomains',
            '6. Long URL'
        ],
        'Criteria': [
            'NoOfJS=0, NoOfCSS=0, NoOfImage=0',
            'IsHTTPS=0',
            'IsDomainIP=1',
            'HasTitle=0, HasFavicon=0, HasDescription=0, HasCopyrightInfo=0',
            'NoOfSubDomain >= 5',
            'URLLength > 57'
        ],
        'Phishing Caught': [
            f"{len(df[(df['label']==0) & (df['NoOfJS']==0) & (df['NoOfCSS']==0) & (df['NoOfImage']==0)]):,}",
            f"{len(df[(df['label']==0) & (df['IsHTTPS']==0)]):,}",
            f"{len(df[(df['label']==0) & (df['IsDomainIP']==1)]):,}",
            f"{len(df[(df['label']==0) & (df['HasTitle']==0) & (df['HasFavicon']==0) & (df['HasDescription']==0) & (df['HasCopyrightInfo']==0)]):,}",
            f"{len(df[(df['label']==0) & (df['NoOfSubDomain']>=5)]):,}",
            f"{len(df[(df['label']==0) & (df['URLLength']>57)]):,}"
        ]
    })

    st.dataframe(rules_df, hide_index=True, use_container_width=True)

    st.write(
        "**Interpretation**: These 6 rules collectively catch 86.4% of phishing (87,205 / 100,945 URLs) "
        "with zero false positives. The remaining 13.6% (13,740 URLs) are sophisticated phishing that "
        "mimics legitimate sites - this is where ML becomes essential."
    )

    st.write("---")

    st.write("### Coverage Analysis")

    st.write(
        "The hybrid approach efficiently divides detection work:\n\n"
        "* **Rule-Based (86.4%)**: Fast, deterministic filtering for obvious phishing\n"
        "* **ML-Based (13.6%)**: Deep feature analysis for sophisticated phishing\n\n"
        "This allows efficient processing - rules handle the majority instantly, while ML provides "
        "deep analysis for sophisticated cases, maintaining 99.995% recall."
    )
