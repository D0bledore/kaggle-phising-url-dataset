import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.data_management import load_data, load_model


def page_performance_body():
    """
    Display model performance metrics, confusion matrix, and feature importance.
    Addresses LO6.2: Dashboard shows plots with interpretation and model performance.
    """

    st.write("## ML Model Performance")

    st.info(
        "This page presents the XGBoost model's performance metrics from Notebook 3. "
        "The model was trained on an 80/20 split, then retrained on the full dataset for deployment."
    )

    # Load model
    model = load_model()
    df, feature_cols = load_data()

    st.write("---")

    st.write("### Model Selection: XGBoost vs Random Forest")

    st.write(
        "I compared two gradient boosting algorithms on the test set (20% holdout, 47,159 URLs):"
    )

    comparison_df = pd.DataFrame({
        'Model': ['Random Forest', 'XGBoost'],
        'Recall': ['99.975%', '99.995%'],
        'Precision': ['100.00%', '100.00%'],
        'False Positives': [0, 0],
        'Missed Phishing': [5, 1],
        'Selected': ['No', 'Yes']
    })

    st.dataframe(comparison_df, hide_index=True, use_container_width=True)

    st.write(
        "**Interpretation**: XGBoost was selected for deployment because it achieved higher recall "
        "(99.995% vs 99.975%) while maintaining zero false positives. Missing only 1 phishing URL instead "
        "of 5 represents a meaningful improvement when scaled to millions of URLs in production."
    )

    st.write("---")

    st.write("### Confusion Matrix (Test Set)")

    st.write(
        "Performance on the 20% test set (47,159 URLs) before final training on full dataset:"
    )

    # Confusion matrix values from Notebook 3
    tn = 26970  # True Negatives (legitimate correctly identified)
    fp = 0      # False Positives (legitimate incorrectly flagged)
    fn = 1      # False Negatives (phishing missed)
    tp = 20188  # True Positives (phishing correctly caught)

    # Create confusion matrix visualization
    fig, ax = plt.subplots(figsize=(8, 6))
    cm = [[tn, fp], [fn, tp]]
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
                xticklabels=['Predicted Legitimate', 'Predicted Phishing'],
                yticklabels=['Actual Legitimate', 'Actual Phishing'],
                ax=ax, annot_kws={'size': 16})
    ax.set_title('Confusion Matrix - XGBoost Test Set Performance', fontsize=14, pad=20)
    plt.tight_layout()
    st.pyplot(fig)

    st.write(
        f"**Interpretation**:\n"
        f"* **True Positives (TP)**: {tp:,} phishing correctly detected\n"
        f"* **False Negatives (FN)**: {fn} phishing missed (0.005% miss rate)\n"
        f"* **True Negatives (TN)**: {tn:,} legitimate correctly allowed\n"
        f"* **False Positives (FP)**: {fp} legitimate incorrectly blocked (0% - meets business requirement!)\n\n"
        "The zero false positives is critical - blocking legitimate sites would harm user trust and adoption."
    )

    st.write("---")

    st.write("### Performance Metrics")

    # Calculate metrics
    recall = tp / (tp + fn) * 100
    precision = tp / (tp + fp) * 100 if (tp + fp) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall)
    accuracy = (tp + tn) / (tp + tn + fp + fn) * 100

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Recall", f"{recall:.3f}%")
    with col2:
        st.metric("Precision", f"{precision:.2f}%")
    with col3:
        st.metric("F1 Score", f"{f1_score:.3f}%")
    with col4:
        st.metric("Accuracy", f"{accuracy:.3f}%")

    st.write(
        "**Interpretation**:\n"
        f"* **Recall ({recall:.3f}%)**: Catches {tp:,} out of {tp+fn:,} phishing cases - only {fn} slipped through\n"
        f"* **Precision ({precision:.2f}%)**: Every flagged URL is actually phishing - zero false alarms\n"
        f"* **F1 Score ({f1_score:.3f}%)**: Harmonic mean of precision and recall - indicates excellent balance\n"
        f"* **Accuracy ({accuracy:.3f}%)**: Overall correctness across both classes\n\n"
        "The model exceeds the business requirement of 99%+ recall with zero false positives."
    )

    st.write("---")

    st.write("### Top 10 Most Important Features")

    st.write(
        "XGBoost's feature importance scores show which features contribute most to predictions:"
    )

    # Feature importance from the model
    feature_importance = pd.DataFrame({
        'Feature': feature_cols,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False).head(10)

    # Plot feature importance
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=feature_importance, y='Feature', x='Importance', palette='viridis', ax=ax)
    ax.set_title('Top 10 Feature Importance Scores', fontsize=14, pad=20)
    ax.set_xlabel('Importance Score', fontsize=12)
    ax.set_ylabel('Feature', fontsize=12)
    plt.tight_layout()
    st.pyplot(fig)

    # Show the table as well
    st.dataframe(feature_importance, hide_index=True, use_container_width=True)

    st.write(
        "**Interpretation**:\n"
        "* **LineOfCode**: Most important feature - phishing sites often have minimal code\n"
        "* **NoOfSelfRef**: Self-references (internal links) indicate site depth and complexity\n"
        "* **NoOfExternalRef**: External references suggest legitimate business connections\n"
        "* **Resource counts (NoOfImage, NoOfJS, NoOfCSS)**: Correlate with site effort/quality\n\n"
        "These features align with our hypotheses - phishing sites show low-effort characteristics "
        "that the model learned to recognize."
    )

    st.write("---")

    st.write("### Edge Cases: The One That Got Away")

    st.warning(
        "**Analysis of the Single Misclassified URL**\n\n"
        "XGBoost missed only 1 phishing URL out of 20,189 test phishing (99.995% recall). This represents "
        "the ultimate edge case - a sophisticated phishing site that perfectly mimicked legitimate patterns "
        "across all 49 features.\n\n"
        "**Context from Notebook 3**: Random Forest initially missed 5 phishing URLs. XGBoost's advanced "
        "gradient boosting (focusing on fixing mistakes) successfully caught 4 of those 5, leaving just "
        "1 URL that even XGBoost couldn't distinguish from legitimate sites.\n\n"
        "**Key Insight**: This single edge case demonstrates the fundamental challenge of perfect detection - "
        "some sophisticated phishing is indistinguishable from legitimate sites using behavioral feature "
        "analysis alone. Future improvements could include:\n"
        "* Content analysis (page text, forms requesting credentials)\n"
        "* Domain reputation scoring\n"
        "* Behavioral analysis (site age, traffic patterns)\n\n"
        "However, 99.995% recall with zero false positives exceeds industry standards and meets our business requirements."
    )

    st.write("---")

    st.write("### Hybrid System Performance")

    st.success(
        "**Overall Detection Performance**:\n\n"
        "* **Rule-Based Coverage**: 86.4% of phishing (87,205 / 100,945) caught instantly\n"
        "* **ML Coverage**: 13.6% of phishing (13,740 / 100,945) require deep analysis\n"
        "* **ML Success Rate**: 99.995% of sophisticated phishing detected\n"
        "* **Total System Recall**: ~99.99% (combining both stages)\n"
        "* **False Positive Rate**: 0.00% (zero false positives from both stages)\n\n"
        "The hybrid approach delivers both high performance and efficiency while maintaining exceptional accuracy."
    )
