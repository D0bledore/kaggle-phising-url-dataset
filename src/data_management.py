import streamlit as st
import pandas as pd
import pickle


@st.cache_data
def load_data():
    """
    Load the phishing URL dataset and extract feature columns.

    Returns:
        df (DataFrame): Full dataset (235,795 URLs × 56 features)
        feature_cols (list): Column names for ML features (49 features)
    """
    df = pd.read_csv('data/dataset4.csv')
    features_to_exclude = ['URLSimilarityIndex', 'FILENAME', 'URL', 'Domain', 'TLD', 'Title', 'label']
    feature_cols = [col for col in df.columns if col not in features_to_exclude]
    return df, feature_cols


@st.cache_resource
def load_model():
    """
    Load the trained XGBoost model.

    Returns:
        model: XGBoost classifier (99.995% recall, 100% precision)
    """
    with open('models/xgb_model.pkl', 'rb') as f:
        return pickle.load(f)
