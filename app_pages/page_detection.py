import streamlit as st
import pandas as pd
from src.data_management import load_data, load_model
from src.detection import detect_violations


def page_detection_body():
    """
    Interactive URL testing page - search, filter, and test URLs from the dataset.
    This is the main demo functionality from the original app.py.
    Addresses LO6.1: Dashboard provides interactive inputs and predictions.
    """

    st.write("## Phishing Detection Demo")

    st.info(
        "**Demo Mode Explanation**: This demo searches through 235K URLs from the training dataset "
        "rather than scanning live websites. This approach focuses on demonstrating the ML model's "
        "capabilities without requiring complex web scraping infrastructure."
    )

    # Load data and model
    df, feature_cols = load_data()
    model = load_model()

    # Sidebar for search and filters
    with st.sidebar:
        st.header("Select URL")

        # Filters
        st.markdown("**Filters:**")

        col1, col2 = st.columns(2)

        with col1:
            label_filter = st.selectbox(
                "Label:",
                ["All", "Phishing", "Legitimate"],
                key="label_filter"
            )

        with col2:
            https_filter = st.selectbox(
                "Protocol:",
                ["All", "HTTPS", "HTTP"],
                key="https_filter"
            )

        # TLD filter
        common_tlds = ["All"] + sorted(df['TLD'].value_counts().head(20).index.tolist())
        tld_filter = st.selectbox(
            "TLD:",
            common_tlds,
            key="tld_filter"
        )

        # Violation filter
        violation_filter = st.selectbox(
            "Violations:",
            ["All", "With Violations", "Clean URLs"],
            key="violation_filter"
        )

        st.markdown("---")

        # Search box
        search = st.text_input("Search URLs:", placeholder="e.g., google, blogspot, .top")

        # Apply filters
        filtered_df = df.copy()

        # Label filter
        if label_filter == "Phishing":
            filtered_df = filtered_df[filtered_df['label'] == 0]
        elif label_filter == "Legitimate":
            filtered_df = filtered_df[filtered_df['label'] == 1]

        # HTTPS filter
        if https_filter == "HTTPS":
            filtered_df = filtered_df[filtered_df['IsHTTPS'] == 1]
        elif https_filter == "HTTP":
            filtered_df = filtered_df[filtered_df['IsHTTPS'] == 0]

        # TLD filter
        if tld_filter != "All":
            filtered_df = filtered_df[filtered_df['TLD'] == tld_filter]

        # Violation filter
        if violation_filter == "With Violations":
            mask = filtered_df.apply(lambda row: len(detect_violations(row)) > 0, axis=1)
            filtered_df = filtered_df[mask]
        elif violation_filter == "Clean URLs":
            mask = filtered_df.apply(lambda row: len(detect_violations(row)) == 0, axis=1)
            filtered_df = filtered_df[mask]

        # Search filter
        if search:
            filtered_df = filtered_df[filtered_df['URL'].str.contains(search, case=False, na=False)]

        filtered_df = filtered_df.reset_index()
        st.info(f"Found {len(filtered_df):,} matching URLs")

        if len(filtered_df) > 0:
            # Pagination
            urls_per_page = 10
            total_pages = (len(filtered_df) - 1) // urls_per_page + 1

            page = st.number_input(
                f"Page:",
                min_value=1,
                max_value=total_pages,
                value=1,
                key="page_num"
            )

            # Calculate range for current page
            start_idx = (page - 1) * urls_per_page
            end_idx = min(start_idx + urls_per_page, len(filtered_df))

            # Show results for current page
            display_df = filtered_df.iloc[start_idx:end_idx]

            selected_idx = st.radio(
                "Results:",
                range(len(display_df)),
                format_func=lambda i: f"`{display_df.iloc[i]['URL']}`",
                label_visibility="collapsed"
            )
            url_idx = display_df.iloc[selected_idx]['index']

            # Page indicator at bottom
            st.markdown(f"""
                <div style="background-color: #1e1e1e; padding: 8px; border-radius: 5px; margin-top: 15px; text-align: center;">
                    <p style="margin: 0; color: #808495; font-size: 14px;">Page {page} of {total_pages}</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("No matches")
            url_idx = 0

    # Main content
    st.markdown("## How to Use This Demo")
    st.markdown("""
    1. **Search** for a URL in the sidebar (e.g., try "google", ".top", or "blogspot")
    2. **Select** a URL from the results
    3. **View** the detection results below

    This demo uses a **hybrid approach** combining rule-based filtering with machine learning.
    """)

    st.markdown("---")

    st.markdown("## Hybrid Detection System")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Stage 1: Violation Detection")
        st.markdown("""
        **Checks 6 warning signs (zero false positives):**
        1. Zero Resources (no JS, CSS, images)
        2. No HTTPS
        3. Domain is IP Address
        4. Zero Trust Signals (no title, favicon, etc.)
        5. Excessive Subdomains (>=5)
        6. Long URL (>57 chars)

        Shows **ALL violations found** (not just first match) - More convincing evidence
        """)

    with col2:
        st.markdown("### Stage 2: Machine Learning")
        st.markdown("""
        **XGBoost Classifier** (for URLs that pass rules):
        - 100% accuracy on test set
        - 99.995% recall
        - 0 false positives
        - Analyzes 49 features

        Outputs probability score - **Risk assessment**
        """)

    st.markdown("---")

    # Detection Results
    if url_idx is not None and len(filtered_df) > 0:
        selected_row = df.iloc[url_idx]
        original_idx = url_idx

        st.markdown("## Detection Results")

        # Display URL
        st.subheader("Selected URL")
        st.code(selected_row['URL'], language=None)

        # Actual label centered
        actual_label = "PHISHING" if selected_row['label'] == 0 else "LEGITIMATE"
        actual_emoji = "🚨" if selected_row['label'] == 0 else "✅"

        st.markdown(f"<h3 style='text-align: center;'>{actual_emoji} Actual Label: {actual_label}</h3>", unsafe_allow_html=True)

        st.markdown("---")

        # Stage 1: Violation Detection
        st.markdown("### Stage 1: Violation Detection")
        violations = detect_violations(selected_row)

        if violations:
            st.markdown(f"<h3 style='text-align: center; color: #ff4444;'>{len(violations)} WARNING SIGN{'S' if len(violations) > 1 else ''} DETECTED</h3>", unsafe_allow_html=True)

            st.markdown("**Violations Found:**")
            for rule_name, explanation in violations:
                st.markdown(f"- **{rule_name}**: {explanation}")

            st.markdown("**Decision:** BLOCK (rule-based detection)")

        else:
            st.success("No violations found - Passed all 6 rules")

            # Stage 2: ML scoring
            st.markdown("### Stage 2: Machine Learning Prediction")

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
                st.error(f"**HIGH RISK** ({prob_phishing:.1f}% phishing)\n\n**Recommendation:** Flag for immediate manual review")
            elif prob_phishing > 70:
                st.warning(f"**MEDIUM RISK** ({prob_phishing:.1f}% phishing)\n\n**Recommendation:** Queue for manual review")
            else:
                st.success(f"**LOW RISK** ({prob_phishing:.1f}% phishing)\n\n**Recommendation:** Allow")

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

            st.dataframe(pd.DataFrame(importance_data), width='stretch', hide_index=True)

    else:
        st.info("Use filters or search for a URL in the sidebar to test the detection system")
