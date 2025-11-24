import streamlit as st


def page_summary_body():
    """
    Display project summary page with business requirements, dataset overview, and project terms.
    Addresses LO6.1: Dashboard describes project outcomes and business requirements.
    """

    st.write("## Quick Project Summary")

    st.info(
        "**Project Background**\n\n"
        "Phishing attacks remain one of the most prevalent cyber threats, with attackers creating "
        "fraudulent websites to steal credentials and sensitive information. Traditional blacklist-based "
        "detection systems struggle to keep pace with new phishing sites appearing daily.\n\n"
        "This project develops a hybrid phishing detection system combining rule-based filtering "
        "(for obvious cases) with machine learning (for sophisticated attacks)."
    )

    st.write("### Business Requirements")

    st.success(
        "The project has 3 core business requirements:\n\n"
        "1. **Identify Key Phishing Indicators**: Analyze URL features to determine which patterns "
        "reliably distinguish phishing from legitimate sites\n\n"
        "2. **Build Hybrid Detection System**: Develop perfect-precision rules for obvious phishing, "
        "then use ML for sophisticated cases that bypass rules\n\n"
        "3. **Achieve High Recall with Zero False Positives**: Catch 99%+ of phishing while never "
        "blocking legitimate sites (false positives harm user trust)"
    )

    st.write("### Dataset Overview")

    st.write(
        "* **Source**: Kaggle dataset by Md Sultanul Islam Ovi\n"
        "* **Size**: 235,795 URLs (100,932 phishing, 134,863 legitimate)\n"
        "* **Features**: 56 total (49 used for ML after excluding URL strings, labels, etc.)\n"
        "* **Feature Types**: Structural (URL length, subdomains), behavioral (HTTPS, resources), "
        "content (title, favicon, copyright)\n"
        "* **Quality**: Selected from 6 available datasets for completeness and accuracy"
    )

    st.write("### Project Terms & Jargon")

    st.info(
        "**Phishing**: Fraudulent websites designed to steal credentials or sensitive information\n\n"
        "**False Positive (FP)**: Legitimate site incorrectly flagged as phishing (harmful to user experience)\n\n"
        "**Recall**: Percentage of phishing sites successfully detected (target: 99%+)\n\n"
        "**Precision**: Percentage of flagged sites that are actually phishing (target: 100%)\n\n"
        "**Rule-Based Detection**: Perfect-precision filters checking obvious warning signs "
        "(Zero Resources, No HTTPS, IP domains, etc.)\n\n"
        "**Hybrid Approach**: Rule-based filtering (86.4% coverage) + ML for remaining 13.6%\n\n"
        "**XGBoost**: Gradient boosting ML algorithm achieving 99.995% recall with 100% precision"
    )
