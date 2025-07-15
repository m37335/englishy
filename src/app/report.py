"""
Report page for Englishy.
"""

import streamlit as st
import json
import os
from datetime import datetime
import sys

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# from utils.report_manager import ReportManager
from utils.mindmap_utils import draw_mindmap


def create_report_page(report=None):
    """Create the report page function."""
    
    if report is None:
        # Show all reports
        st.title("📊 Reports")
        st.markdown("View and manage your English learning reports")
        
        # report_manager = ReportManager()
        
        # Load reports
        # reports = report_manager.load_reports()
        
        # Display statistics
        # stats = report_manager.get_report_statistics()
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Reports", "N/A")
        
        with col2:
            if "N/A":
                latest_date = datetime.fromisoformat("N/A".replace('Z', '+00:00'))
                st.metric("Latest Report", latest_date.strftime("%Y-%m-%d"))
            else:
                st.metric("Latest Report", "None")
        
        with col3:
            st.metric("Avg Length", "N/A")
        
        # Search functionality
        st.subheader("🔍 Search Reports")
        search_query = st.text_input(
            "Search reports by title, query, or content",
            placeholder="Enter search terms..."
        )
        
        if search_query:
            # matching_reports = report_manager.search_reports(search_query)
            st.info(f"Found 0 matching reports")
            # reports = matching_reports
        
        # Display reports
        if not "reports":
            st.info("No reports found. Start a new research to generate reports.")
            return
        
        st.subheader("📄 Your Reports")
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            sort_by = st.selectbox(
                "Sort by",
                ["Date (Newest)", "Date (Oldest)", "Title", "Query"],
                index=0
            )
        
        with col2:
            show_count = st.selectbox(
                "Show",
                ["All", "5", "10", "20"],
                index=0
            )
        
        # Sort reports
        if sort_by == "Date (Newest)":
            # reports.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            pass
        elif sort_by == "Date (Oldest)":
            # reports.sort(key=lambda x: x.get('timestamp', ''))
            pass
        elif sort_by == "Title":
            # reports.sort(key=lambda x: x.get('title', ''))
            pass
        elif sort_by == "Query":
            # reports.sort(key=lambda x: x.get('query', ''))
            pass
        
        # Limit display
        if show_count != "All":
            # reports = reports[:int(show_count)]
            pass
        
        # Display each report
        for i, report in enumerate("reports"):
            _display_report_card(report, i, "report_manager")
    else:
        # Show specific report
        _view_report(report)


def _display_report_card(report, index, report_manager):
    """Display a single report card."""
    report_id = report.get('id', f'report_{index}')
    title = report.get('title', 'Untitled Report')
    query = report.get('query', 'No query')
    timestamp = report.get('timestamp', 'Unknown')
    
    # Format timestamp
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        formatted_date = dt.strftime("%Y-%m-%d %H:%M")
    except:
        formatted_date = timestamp
    
    # Create expandable card
    with st.expander(f"📄 {title} - {formatted_date}", expanded=False):
        st.markdown(f"**Query:** {query}")
        st.markdown(f"**Generated:** {formatted_date}")
        
        # Display settings if available
        settings = report.get('settings', {})
        if settings:
            st.markdown("**Settings:**")
            settings_text = f"Web Search: {settings.get('web_search', 'N/A')}, "
            settings_text += f"Mindmap: {settings.get('mindmap', 'N/A')}, "
            settings_text += f"Depth: {settings.get('depth', 'N/A')}, "
            settings_text += f"Style: {settings.get('style', 'N/A')}"
            st.markdown(settings_text)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button(f"View Report", key=f"view_{report_id}"):
                _view_report(report)
        
        with col2:
            if st.button(f"Download", key=f"download_{report_id}"):
                _download_report(report)
        
        with col3:
            if st.button(f"Delete", key=f"delete_{report_id}"):
                # if report_manager.delete_report(report_id):
                st.success("Report deleted!")
                st.rerun()
                # else:
                #     st.error("Failed to delete report")


def _view_report(report):
    """View a specific report."""
    st.subheader("📄 Report Details")
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Report", "🗺️ Mindmap", "🔍 Search Results", "📊 Statistics"])
    
    with tab1:
        # Display report content
        content = report.get('content', '')
        if content:
            st.markdown("### Generated Report")
            st.markdown(content)
            
            # Download button for report
            if st.button("📥 Download Report"):
                st.download_button(
                    label="Download Report as Markdown",
                    data=content,
                    file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown"
                )
        else:
            st.info("No report content available.")
    
    with tab2:
        # Display mindmap
        mindmap_content = report.get('mindmap', '')
        if mindmap_content:
            st.markdown("### Mind Map")
            draw_mindmap(mindmap_content)
            
            # Download buttons for mindmap
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📥 Download Mindmap"):
                    st.download_button(
                        label="Download Mindmap as Markdown",
                        data=mindmap_content,
                        file_name=f"mindmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )
            with col2:
                if st.button("📊 Mindmap Statistics"):
                    _show_mindmap_stats(mindmap_content)
        else:
            st.info("No mind map available.")
    
    with tab3:
        # Display search results
        search_results = report.get('search_results', [])
        if search_results:
            st.markdown("### Search Results")
            for i, result in enumerate(search_results, 1):
                with st.expander(f"Result {i}: {result.get('title', 'No title')}"):
                    st.markdown(f"**URL:** {result.get('url', 'No URL')}")
                    st.markdown(f"**Snippet:** {result.get('snippet', 'No snippet')}")
        else:
            st.info("No search results available.")
    
    with tab4:
        # Display statistics
        st.markdown("### Report Statistics")
        
        # Basic stats
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Report Length", f"{len(report.get('content', ''))} chars")
            st.metric("Mindmap Nodes", _count_mindmap_nodes(report.get('mindmap', '')))
        with col2:
            st.metric("Search Results", len(report.get('search_results', [])))
            st.metric("Processing Time", f"{report.get('processing_time', 0):.2f}s")
        
        # Detailed stats
        if report.get('search_stats'):
            st.markdown("#### Search Statistics")
            search_stats = report['search_stats']
            st.metric("Total Searches", search_stats.get('total_searches', 0))
            st.metric("Web Results", search_stats.get('web_results', 0))
            st.metric("Avg Relevance", f"{search_stats.get('avg_relevance', 0):.2f}")


def _download_report(report):
    """Download a report."""
    content = report.get('content', '')
    if content:
        st.download_button(
            label="Download Report",
            data=content,
            file_name=f"englishy_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )


def _show_mindmap_stats(mindmap_text):
    """Show mindmap statistics."""
    if not mindmap_text:
        st.info("No mindmap available for statistics.")
        return
    
    def count_nodes(mindmap_text):
        """Count the number of nodes in the mindmap."""
        lines = mindmap_text.split('\n')
        return len([line for line in lines if line.strip().startswith('#')])
    
    def get_max_depth(mindmap_text):
        """Get the maximum depth of the mindmap."""
        lines = mindmap_text.split('\n')
        max_depth = 0
        for line in lines:
            if line.strip().startswith('#'):
                depth = len(line) - len(line.lstrip('#'))
                max_depth = max(max_depth, depth)
        return max_depth
    
    def get_main_categories(mindmap_text):
        """Get the main categories (## headers) from the mindmap."""
        lines = mindmap_text.split('\n')
        categories = []
        for line in lines:
            if line.strip().startswith('## '):
                categories.append(line.strip()[3:])
        return categories
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Nodes", count_nodes(mindmap_text))
    with col2:
        st.metric("Max Depth", get_max_depth(mindmap_text))
    with col3:
        st.metric("Main Categories", len(get_main_categories(mindmap_text)))
    
    # Show main categories
    categories = get_main_categories(mindmap_text)
    if categories:
        st.markdown("#### Main Categories")
        for category in categories:
            st.markdown(f"- {category}")


def _count_mindmap_nodes(mindmap_text):
    """Count nodes in mindmap text."""
    if not mindmap_text:
        return 0
    lines = mindmap_text.split('\n')
    return len([line for line in lines if line.strip().startswith('#')]) 