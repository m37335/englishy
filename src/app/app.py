"""
Main Streamlit application for Englishy.
"""

import os
from pathlib import Path

import dotenv
import streamlit as st
import sys
with open("/tmp/pythonpath.log", "w") as f:
    f.write(str(sys.path))

dotenv.load_dotenv()

st.set_page_config(
    page_title="Englishy - English Learning Research Tool",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize report manager
# import sys
# import os
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# from utils.report_manager import ReportManager
# report_manager = ReportManager()

# Load existing reports
# reports = report_manager.load_reports()
reports = []

# Create pages dictionary with lazy imports
def get_pages():
    """Get pages with lazy imports to avoid circular imports."""
    from config import create_config_page
    from report import create_report_page
    from research import create_research_page
    
    pages = {
        "New Research": [st.Page(create_research_page, title="New Research", url_path="new", icon=":material/edit_square:")],
        "Config": [st.Page(create_config_page, title="Config", url_path="config", icon=":material/settings:")],
    }
    
    # Add report pages if reports exist
    if reports:
        for i, report in enumerate(reports):
            report_id = report.get('id', f'report_{i}')
            title = report.get('title', 'Untitled Report')
            pages[f"Report_{i+1}"] = [st.Page(create_report_page, title=title, url_path=report_id)]
    
    return pages

# Create navigation
pages = get_pages()
pg = st.navigation(pages, expanded=True)

# Run the navigation
pg.run() 