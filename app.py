import streamlit as st
from app_pages.page_summary import page_summary_body
from app_pages.page_study import page_study_body
from app_pages.page_detection import page_detection_body
from app_pages.page_hypothesis import page_hypothesis_body
from app_pages.page_performance import page_performance_body


# Page configuration
st.set_page_config(
    page_title="Phishing Detection System",
    page_icon="🔒",
    layout="wide"
)


# Multi-page navigation
class MultiPage:
    """
    Multi-page Streamlit application orchestrator.
    Manages navigation between different dashboard pages.
    """

    def __init__(self, app_name):
        self.pages = []
        self.app_name = app_name

    def add_page(self, title, func):
        """Add a new page to the app"""
        self.pages.append({"title": title, "function": func})

    def run(self):
        """Run the multi-page application"""
        st.title(self.app_name)

        # Navigation menu in sidebar
        page = st.sidebar.radio(
            "Navigation",
            self.pages,
            format_func=lambda page: page['title']
        )

        # Display project info in sidebar
        st.sidebar.markdown("---")
        st.sidebar.info(
            "**Phishing Detection System**\n\n"
            "Hybrid ML approach combining rule-based filtering "
            "with XGBoost for sophisticated phishing detection.\n\n"
            "**Dataset**: 235K URLs, 56 features\n\n"
            "**Performance**: 99.995% recall, 0% false positives"
        )

        # Run the selected page
        page['function']()


# Create app instance
app = MultiPage(app_name="🔒 Phishing Detection System")

# Add pages
app.add_page("Project Summary", page_summary_body)
app.add_page("Data Study", page_study_body)
app.add_page("Hypothesis & Validation", page_hypothesis_body)
app.add_page("ML Performance", page_performance_body)
app.add_page("Detection Demo", page_detection_body)

# Run the app
app.run()
